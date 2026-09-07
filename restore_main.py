with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I need to remove the broken tail and append MainActivity and QuickRepliesScreen
# My python script replaced EVERYTHING from `ProfileScreen` with `new_profile` + content[-13:]
# So I'll find where ProfileScreen ends. My new ProfileScreen ends with:
#                     Spacer(Modifier.height(32.dp))
#                 }
#             }
#         }
#     }
# }

marker = "Spacer(Modifier.height(32.dp))\n                }\n            }\n        }\n    }\n}"
idx = content.find(marker)
if idx != -1:
    content = content[:idx + len(marker)]
else:
    print("Could not find marker")

# Now append QuickRepliesScreen and MainActivity
append_text = """

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuickRepliesScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = androidx.compose.ui.platform.LocalContext.current
    var reply1 by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(viewModel.quickReply1.value) }
    var reply2 by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(viewModel.quickReply2.value) }

    androidx.compose.foundation.layout.Box(modifier = androidx.compose.foundation.layout.Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        androidx.compose.foundation.layout.Column(modifier = androidx.compose.foundation.layout.Modifier.fillMaxSize().padding(24.dp)) {
            androidx.compose.material3.Text("Manage Quick Replies", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E293B))
            androidx.compose.foundation.layout.Spacer(androidx.compose.foundation.layout.Modifier.height(24.dp))
            
            androidx.compose.material3.OutlinedTextField(
                value = reply1,
                onValueChange = { reply1 = it },
                label = { androidx.compose.material3.Text("Quick Reply 1") },
                modifier = androidx.compose.foundation.layout.Modifier.fillMaxWidth()
            )
            androidx.compose.foundation.layout.Spacer(androidx.compose.foundation.layout.Modifier.height(16.dp))
            androidx.compose.material3.OutlinedTextField(
                value = reply2,
                onValueChange = { reply2 = it },
                label = { androidx.compose.material3.Text("Quick Reply 2") },
                modifier = androidx.compose.foundation.layout.Modifier.fillMaxWidth()
            )
            androidx.compose.foundation.layout.Spacer(androidx.compose.foundation.layout.Modifier.height(32.dp))
            
            androidx.compose.material3.Button(
                onClick = { 
                    viewModel.saveProfileDetails(context, viewModel.homeAddress.value, viewModel.bankName.value, viewModel.bankIban.value, reply1, reply2)
                    navController.popBackStack()
                },
                modifier = androidx.compose.foundation.layout.Modifier.fillMaxWidth().height(52.dp),
                colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
            ) {
                androidx.compose.material3.Text("SAVE REPLIES", color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
    }
}

// --- Main Activity ---
class MainActivity : androidx.activity.ComponentActivity() {
    override fun onCreate(savedInstanceState: android.os.Bundle?) {
        super.onCreate(savedInstanceState)
        
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.app.ActivityCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                androidx.core.app.ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }

        val workRequest = androidx.work.PeriodicWorkRequestBuilder<com.example.OrderPollingWorker>(15, java.util.concurrent.TimeUnit.MINUTES).build()
        androidx.work.WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "OrderPolling",
            androidx.work.ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )

        androidx.activity.enableEdgeToEdge()
        androidx.core.view.WindowCompat.setDecorFitsSystemWindows(window, false)
        androidx.activity.compose.setContent {
            com.example.ui.theme.RiderTheme {
                val viewModel: RiderViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
                val context = androidx.compose.ui.platform.LocalContext.current
                
                val navController = androidx.navigation.compose.rememberNavController()
                
                androidx.compose.runtime.LaunchedEffect(Unit) {
                    viewModel.initSession(context)
                }
                val riderId by viewModel.riderId.collectAsState()
                
                androidx.compose.runtime.LaunchedEffect(riderId) {
                    if (riderId != -1) {
                        navController.navigate("dashboard") { popUpTo(0) }
                    } else {
                        navController.navigate("auth") { popUpTo(0) }
                    }
                }
                
                androidx.navigation.compose.NavHost(navController = navController, startDestination = "auth") {
                    androidx.navigation.compose.composable("auth") {
                        AuthFlow(viewModel, navController)
                    }
                    androidx.navigation.compose.composable("dashboard") {
                        MainAppScreen(viewModel)
                    }
                }
            }
        }
    }
}
"""

content = content + append_text

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
