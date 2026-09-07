package com.example


import android.app.NotificationChannel

import android.app.NotificationManager

import android.content.Context

import android.content.pm.PackageManager

import android.os.Build

import androidx.core.app.ActivityCompat

import androidx.core.app.NotificationCompat

import androidx.core.app.NotificationManagerCompat

import androidx.work.CoroutineWorker

import androidx.work.WorkerParameters

import retrofit2.Response

class OrderPollingWorker(
    private val context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        val zone = prefs.getString("rider_zones", "") ?: ""
        val riderId = prefs.getInt("rider_id", -1)

        if (zone.isEmpty() || riderId == -1) {
            return Result.success()
        }

        try {
            val response = RetrofitClient.apiService.getAvailableOrders(zone, riderId)
            if (response.isSuccessful && response.body()?.status == "success") {
                val orders = response.body()?.data ?: emptyList()
                val previousOrderCount = prefs.getInt("last_order_count", 0)

                if (orders.size > previousOrderCount) {
                    showNotification(context, orders.size, zone)
                }
                
                prefs.edit().putInt("last_order_count", orders.size).apply()
            }
        } catch (e: Exception) {
            // Suppress error in background
        }

        return Result.success()
    }

    private fun showNotification(context: Context, orderCount: Int, zone: String) {
        val channelId = "radar_channel"
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "Radar Notifications"
            val descriptionText = "Notifications for new orders on radar"
            val importance = NotificationManager.IMPORTANCE_HIGH
            val channel = NotificationChannel(channelId, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_map)
            .setContentTitle("New Orders on Radar!")
            .setContentText("There are now $orderCount orders available in $zone.")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)

        with(NotificationManagerCompat.from(context)) {
            if (ActivityCompat.checkSelfPermission(
                    context,
                    android.Manifest.permission.POST_NOTIFICATIONS
                ) == PackageManager.PERMISSION_GRANTED
            ) {
                notify(1001, builder.build())
            }
        }
    }
}
