import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Schedule ChatWorker in startPolling
old_start_polling = """        val workRequest = PeriodicWorkRequestBuilder<OrderPollingWorker>(15, java.util.concurrent.TimeUnit.MINUTES)
            .build()
        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            "OrderPolling",
            ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )"""

new_start_polling = """        val workRequest = PeriodicWorkRequestBuilder<OrderPollingWorker>(15, java.util.concurrent.TimeUnit.MINUTES)
            .build()
        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            "OrderPolling",
            ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )
        
        val chatRequest = PeriodicWorkRequestBuilder<ChatWorker>(15, java.util.concurrent.TimeUnit.MINUTES).build()
        WorkManager.getInstance(context).enqueueUniquePeriodicWork("ChatPolling", ExistingPeriodicWorkPolicy.KEEP, chatRequest)"""

if old_start_polling in content:
    content = content.replace(old_start_polling, new_start_polling)

# Add wallet screen navigation
if 'composable("wallet") { WalletScreen(viewModel) }' not in content:
    content = content.replace(
        'composable("history") { HistoryScreen(viewModel) }',
        'composable("history") { HistoryScreen(viewModel) }\n            composable("wallet") { WalletScreen(viewModel) }'
    )

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
