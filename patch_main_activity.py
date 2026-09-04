import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add missing imports for permissions and WorkManager
imports = """import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.core.app.ActivityCompat
import android.content.pm.PackageManager
import android.os.Build
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.ExistingPeriodicWorkPolicy
import java.util.concurrent.TimeUnit
"""

if "import androidx.work.WorkManager" not in content:
    content = content.replace("import androidx.activity.ComponentActivity", imports)

old_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {"""

new_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }

        val workRequest = PeriodicWorkRequestBuilder<OrderPollingWorker>(15, TimeUnit.MINUTES).build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "OrderPolling",
            ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )

        enableEdgeToEdge()
        setContent {"""

if old_oncreate in content:
    content = content.replace(old_oncreate, new_oncreate)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
