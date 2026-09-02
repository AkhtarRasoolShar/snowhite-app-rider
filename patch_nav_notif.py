with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Imports
target_imports = """import retrofit2.http.PATCH"""
replace_imports = """import retrofit2.http.PATCH
import java.util.concurrent.TimeUnit
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts"""
content = content.replace(target_imports, replace_imports)

# 2. Worker class (append before EOF)
worker_code = """
class OrderCheckWorker(appContext: Context, params: WorkerParameters) : CoroutineWorker(appContext, params) {
    override suspend fun doWork(): Result {
        val prefs = applicationContext.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        val isOnline = prefs.getBoolean("is_online", false)
        val zone = prefs.getString("rider_zones", "") ?: ""

        if (!isOnline || zone.isEmpty()) return Result.success()

        try {
            val response = RetrofitClient.apiService.getAvailableOrders(zone)
            if (response.isSuccessful && response.body()?.status == "success") {
                val orders = response.body()?.data ?: emptyList()
                if (orders.isNotEmpty()) {
                    showNotification(orders.size)
                }
            }
        } catch (e: Exception) {}
        return Result.success()
    }

    private fun showNotification(count: Int) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU && 
            ContextCompat.checkSelfPermission(applicationContext, android.Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) return

        val notification = NotificationCompat.Builder(applicationContext, "orders_channel")
            .setSmallIcon(android.R.drawable.ic_dialog_map)
            .setContentTitle("New Orders Available!")
            .setContentText("There are $count orders waiting in your zone.")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        NotificationManagerCompat.from(applicationContext).notify(1001, notification)
    }
}
"""
content = content + "\n" + worker_code

# 3. Notification Channel in MainActivity
target_oncreate = """        val viewModel = RiderViewModel()
        viewModel.initSession(this)"""
replace_oncreate = """        val viewModel = RiderViewModel()
        viewModel.initSession(this)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("orders_channel", "New Orders", NotificationManager.IMPORTANCE_HIGH)
            getSystemService(NotificationManager::class.java)?.createNotificationChannel(channel)
        }"""
content = content.replace(target_oncreate, replace_oncreate)

# 4. toggleOnlineStatus -> schedule work
target_toggle = """        _isOnline.value = online
        
        viewModelScope.launch {"""
replace_toggle = """        _isOnline.value = online
        
        val workManager = WorkManager.getInstance(context)
        if (online) {
            val workRequest = PeriodicWorkRequestBuilder<OrderCheckWorker>(15, TimeUnit.MINUTES).build()
            workManager.enqueueUniquePeriodicWork("OrderCheck", ExistingPeriodicWorkPolicy.KEEP, workRequest)
        } else {
            workManager.cancelUniqueWork("OrderCheck")
        }
        
        viewModelScope.launch {"""
content = content.replace(target_toggle, replace_toggle)

# 5. Permission request in RadarScreen
target_radar_start = """    LaunchedEffect(Unit) {
        viewModel.fetchOrders()
    }"""
replace_radar_start = """    LaunchedEffect(Unit) {
        viewModel.fetchOrders()
    }
    
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        val permissionLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { }
        LaunchedEffect(Unit) {
            permissionLauncher.launch(android.Manifest.permission.POST_NOTIFICATIONS)
        }
    }"""
content = content.replace(target_radar_start, replace_radar_start)

# 6. Navigation button in HistoryScreen
target_history_card = """                            IconButton(
                                onClick = { 
                                    Toast.makeText(context, "Connecting to Bluetooth Printer...", Toast.LENGTH_SHORT).show() 
                                },
                                modifier = Modifier.background(SoftWhite, RoundedCornerShape(8.dp))
                            ) {
                                Icon(Icons.Default.Print, contentDescription = "Print", tint = DarkBlue)
                            }
                        }
                    }"""
replace_history_card = """                            IconButton(
                                onClick = { 
                                    Toast.makeText(context, "Connecting to Bluetooth Printer...", Toast.LENGTH_SHORT).show() 
                                },
                                modifier = Modifier.background(SoftWhite, RoundedCornerShape(8.dp))
                            ) {
                                Icon(Icons.Default.Print, contentDescription = "Print", tint = DarkBlue)
                            }
                        }
                        
                        Spacer(Modifier.height(8.dp))
                        
                        Button(
                            onClick = {
                                val gmmIntentUri = Uri.parse("google.navigation:q=${Uri.encode(order.address ?: "Karachi")}")
                                val mapIntent = Intent(Intent.ACTION_VIEW, gmmIntentUri)
                                mapIntent.setPackage("com.google.android.apps.maps")
                                try {
                                    context.startActivity(mapIntent)
                                } catch (e: Exception) {
                                    Toast.makeText(context, "Google Maps not installed", Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.fillMaxWidth().height(48.dp).padding(horizontal = 16.dp, vertical = 4.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = DarkBlue),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Icon(Icons.Default.Navigation, contentDescription = "Navigate", tint = Color.White)
                            Spacer(Modifier.width(8.dp))
                            Text("NAVIGATE TO DESTINATION", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                        Spacer(Modifier.height(8.dp))
                    }"""
content = content.replace(target_history_card, replace_history_card)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
