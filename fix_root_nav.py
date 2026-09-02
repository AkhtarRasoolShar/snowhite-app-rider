import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace MainActivityContent to use NavHost
old_root = """                LaunchedEffect(Unit) {
                    viewModel.initSession(context)
                }
                
                val riderId by viewModel.riderId.collectAsState()
                
                if (riderId == -1) {
                    AuthFlow(viewModel)
                } else {
                    MainAppScreen(viewModel)
                }"""

new_root = """                val navController = rememberNavController()
                
                LaunchedEffect(Unit) {
                    viewModel.initSession(context)
                }
                val riderId by viewModel.riderId.collectAsState()
                
                LaunchedEffect(riderId) {
                    if (riderId != -1) {
                        navController.navigate("dashboard") { popUpTo(0) }
                    } else {
                        navController.navigate("auth") { popUpTo(0) }
                    }
                }
                
                NavHost(navController = navController, startDestination = "auth") {
                    composable("auth") {
                        AuthFlow(viewModel, navController)
                    }
                    composable("dashboard") {
                        MainAppScreen(viewModel)
                    }
                }"""
content = content.replace(old_root, new_root)

# Update AuthFlow
old_auth = "fun AuthFlow(viewModel: RiderViewModel) {"
new_auth = "fun AuthFlow(viewModel: RiderViewModel, navController: NavHostController) {"
content = content.replace(old_auth, new_auth)

old_login_call = "LoginScreen(viewModel, onNavigateToRegister = { isLogin = false })"
new_login_call = 'LoginScreen(viewModel, navController, onNavigateToRegister = { isLogin = false })'
content = content.replace(old_login_call, new_login_call)

# Update LoginScreen
old_login = "fun LoginScreen(viewModel: RiderViewModel, onNavigateToRegister: () -> Unit) {"
new_login = "fun LoginScreen(viewModel: RiderViewModel, navController: NavController, onNavigateToRegister: () -> Unit) {"
content = content.replace(old_login, new_login)

# Update login click
old_click = "viewModel.login(phone, password, context, onSuccess = { /* App state automatically switches based on riderId */ })"
new_click = 'viewModel.login(phone, password, context, onSuccess = { navController.navigate("dashboard") { popUpTo(0) } })'
content = content.replace(old_click, new_click)


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
