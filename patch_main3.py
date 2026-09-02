with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Remove RiderViewModel logic
content = re.sub(r'import com.example.viewmodel.RiderViewModel\n', '', content)
content = re.sub(r'import com.example.network.RiderTask\n', '', content)
content = re.sub(r'val riderViewModel: RiderViewModel = viewModel\(\)\n', '', content)
content = re.sub(r'import com.example.ui.screens.Rider[A-Za-z0-9_]*\n', '', content)
content = content.replace("import com.example.ui.screens.*", "import com.example.ui.screens.*\nimport com.example.ui.screens.CustomerSplashScreen\nimport com.example.ui.screens.LoginScreen\nimport com.example.ui.screens.RegisterScreen")

# Add isLoggedIn observing in MainActivity
content = content.replace(
    'val viewModel: SnowWhiteViewModel = viewModel()',
    'val viewModel: SnowWhiteViewModel = viewModel()\n        val isLoggedIn by viewModel.isLoggedIn.collectAsState()'
)

# Intercept navigation
content = content.replace(
    'onNavigateToSchedule = { navController.navigate("schedule_pickup") },',
    'onNavigateToSchedule = { if(isLoggedIn) navController.navigate("schedule_pickup") else navController.navigate("login") },'
)
content = content.replace(
    'onNavigateToOrders = { navController.navigate("orders") { popUpTo(navController.graph.startDestinationId) } },',
    'onNavigateToOrders = { if(isLoggedIn) navController.navigate("orders") { popUpTo(navController.graph.startDestinationId) } else navController.navigate("login") },'
)

# Add Auth routes and Splash
nav_block = """
                            composable("splash") {
                                CustomerSplashScreen(onNavigateToHome = { navController.navigate("home") { popUpTo("splash") { inclusive = true } } })
                            }
                            composable("login") {
                                LoginScreen(
                                    viewModel = viewModel,
                                    onNavigateToRegister = { navController.navigate("register") },
                                    onLoginSuccess = { navController.popBackStack() }
                                )
                            }
                            composable("register") {
                                RegisterScreen(
                                    viewModel = viewModel,
                                    onNavigateToLogin = { navController.popBackStack() },
                                    onRegisterSuccess = { navController.navigate("home") { popUpTo(0) } }
                                )
                            }
"""

content = content.replace('startDestination = "home"', 'startDestination = "splash"')
content = content.replace('composable("home") {', nav_block + 'composable("home") {')

# Remove Rider routes
content = re.sub(r'composable\("rider_splash"\) \{[\s\S]*?composable\("rider_earnings"\) \{[\s\S]*?\}', '', content)

# Remove Rider Portal from Drawer
content = re.sub(r'NavigationDrawerItem\(\s*label = \{ Text\("Rider Portal \(Staff\)"\) \},[\s\S]*?onClick = \{[^\}]*\}\s*\)\s*', '', content)

# Fix drawer user data
drawer_header = """
                    ModalDrawerSheet(
                        modifier = Modifier.width(280.dp),
                        drawerContainerColor = Color.White
                    ) {
                        val custName by viewModel.customerName.collectAsState()
                        val custPhone by viewModel.customerPhone.collectAsState()
                        Column(modifier = Modifier.padding(24.dp)) {
                            Text("Welcome,", color = Color.Gray, style = MaterialTheme.typography.bodyMedium)
                            Text(custName, color = DeepNavy, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                            if (custPhone.isNotBlank()) {
                                Text(custPhone, color = DeepNavy.copy(alpha = 0.7f), style = MaterialTheme.typography.bodySmall)
                            }
                        }
                        HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp))
"""

content = re.sub(r'ModalDrawerSheet\([\s\S]*?HorizontalDivider\(modifier = Modifier\.padding\(horizontal = 16\.dp\)\)', drawer_header, content)

logout_btn = """
                                NavigationDrawerItem(
                                    label = { Text("Customer Support") },
                                    icon = { Icon(Icons.Default.HeadsetMic, null) },
                                    selected = false,
                                    onClick = { scope.launch { drawerState.close() }; navController.navigate("support") }
                                )
                                if (isLoggedIn) {
                                    Spacer(modifier = Modifier.weight(1f))
                                    NavigationDrawerItem(
                                        label = { Text("Logout") },
                                        icon = { Icon(Icons.AutoMirrored.Filled.ExitToApp, null) },
                                        selected = false,
                                        onClick = { 
                                            scope.launch { drawerState.close() }
                                            viewModel.logout()
                                            navController.navigate("home") { popUpTo(0) }
                                        }
                                    )
                                    Spacer(modifier = Modifier.height(24.dp))
                                }
"""

content = re.sub(r'NavigationDrawerItem\(\s*label = \{ Text\("Customer Support"\) \},[\s\S]*?\}\s*\)', logout_btn, content)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
