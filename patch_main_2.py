import re

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add RiderViewModel import
content = content.replace(
    'import com.example.viewmodel.SnowWhiteViewModel',
    'import com.example.viewmodel.SnowWhiteViewModel\nimport com.example.viewmodel.RiderViewModel\nimport com.example.network.RiderTask\nimport com.squareup.moshi.Moshi'
)

# Instantiate RiderViewModel
content = content.replace(
    'val viewModel: SnowWhiteViewModel = viewModel()',
    'val viewModel: SnowWhiteViewModel = viewModel()\n        val riderViewModel: RiderViewModel = viewModel()'
)

# Add rider routes to NavHost
rider_routes = """
                            composable("rider_splash") {
                                RiderSplashScreen(
                                    viewModel = riderViewModel,
                                    onNavigateToLogin = { navController.navigate("rider_login") { popUpTo("rider_splash") { inclusive = true } } },
                                    onNavigateToDashboard = { navController.navigate("rider_dashboard") { popUpTo("rider_splash") { inclusive = true } } }
                                )
                            }
                            composable("rider_login") {
                                RiderLoginScreen(
                                    viewModel = riderViewModel,
                                    onLoginSuccess = { navController.navigate("rider_dashboard") { popUpTo("rider_login") { inclusive = true } } }
                                )
                            }
                            composable("rider_dashboard") {
                                RiderDashboardScreen(
                                    viewModel = riderViewModel,
                                    onTaskClick = { task -> 
                                        navController.currentBackStackEntry?.savedStateHandle?.set("task", task)
                                        navController.navigate("rider_task_details")
                                    },
                                    onLogout = {
                                        riderViewModel.logout()
                                        navController.navigate("rider_login") { popUpTo("rider_dashboard") { inclusive = true } }
                                    }
                                )
                            }
                            composable("rider_task_details") {
                                val task = navController.previousBackStackEntry?.savedStateHandle?.get<RiderTask>("task")
                                if (task != null) {
                                    RiderTaskDetailsScreen(
                                        task = task,
                                        viewModel = riderViewModel,
                                        onBack = { navController.popBackStack() }
                                    )
                                } else {
                                    navController.popBackStack()
                                }
                            }
                            composable("rider_earnings") {
                                RiderEarningsScreen(onBack = { navController.popBackStack() })
                            }
"""

content = content.replace(
    'composable("support") { SupportScreen(onBack = { navController.popBackStack() }) }',
    'composable("support") { SupportScreen(onBack = { navController.popBackStack() }) }\n' + rider_routes
)

# Add Rider Portal button to Drawer
drawer_btn = """NavigationDrawerItem(
                                    label = { Text("Rider Portal (Staff)") },
                                    icon = { Icon(Icons.Default.Moped, null) },
                                    selected = false,
                                    onClick = { scope.launch { drawerState.close() }; navController.navigate("rider_splash") }
                                )"""

content = content.replace(
    'NavigationDrawerItem(\n                                    label = { Text("Customer Support")',
    drawer_btn + '\n                                ' + 'NavigationDrawerItem(\n                                    label = { Text("Customer Support")'
)


with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
