package com.example

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat

class ChatWorker(appContext: Context, workerParams: WorkerParameters) :
    CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        val prefs = applicationContext.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        val riderId = prefs.getInt("rider_id", -1)
        if (riderId == -1) return Result.success()
        
        // In a real app we would get the currently active order ID, or poll recent orders
        // Here we can fetch rider's active orders and check messages
        try {
            val response = RetrofitClient.apiService.getRiderOrders(riderId)
            if (response.isSuccessful) {
                val orders = response.body()?.data ?: emptyList()
                for (order in orders.filter { it.status == "Accepted" || it.status == "Collecting" }) {
                    val orderId = order.orderId ?: continue
                    val chatResp = RetrofitClient.apiService.getChatMessages(orderId.toIntOrNull() ?: 0)
                    if (chatResp.isSuccessful) {
                        val messages = chatResp.body()?.data ?: emptyList()
                        val unseenCount = messages.count { it.senderType != "rider" && it.status != "seen" }
                        if (unseenCount > 0) {
                            showNotification(orderId.toIntOrNull() ?: 0, "New message from Customer ($unseenCount)")
                        }
                    }
                }
            }
        } catch (e: Exception) {
            return Result.retry()
        }

        return Result.success()
    }

    private fun showNotification(orderId: Int, message: String) {
        val channelId = "chat_notifications"
        val manager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, "Chat Notifications", NotificationManager.IMPORTANCE_DEFAULT)
            manager.createNotificationChannel(channel)
        }

        val intent = Intent(applicationContext, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            applicationContext, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(applicationContext, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_email)
            .setContentTitle("Order #$orderId")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        manager.notify(orderId, notification)
    }
}
