import re

with open("/app/applet/app/src/main/java/com/example/ui/screens/RiderScreens.kt", "r") as f:
    content = f.read()

content = content.replace(
    '''fun RiderDashboardScreen(viewModel: RiderViewModel, onTaskClick: (RiderTask) -> Unit, onLogout: () -> Unit) {''',
    '''fun RiderDashboardScreen(viewModel: RiderViewModel, onTaskClick: (RiderTask) -> Unit, onLogout: () -> Unit, onNavigateToEarnings: () -> Unit = {}) {'''
)

content = content.replace(
    '''IconButton(onClick = onLogout) {
                        Icon(Icons.Default.ExitToApp, contentDescription = "Logout", tint = Color.White)
                    }''',
    '''IconButton(onClick = onNavigateToEarnings) {
                        Icon(Icons.Default.AccountBalanceWallet, contentDescription = "Earnings", tint = Color.White)
                    }
                    IconButton(onClick = onLogout) {
                        Icon(Icons.Default.ExitToApp, contentDescription = "Logout", tint = Color.White)
                    }'''
)

with open("/app/applet/app/src/main/java/com/example/ui/screens/RiderScreens.kt", "w") as f:
    f.write(content)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    main_content = f.read()

main_content = main_content.replace(
    '''onLogout = {
                                        riderViewModel.logout()
                                        navController.navigate("rider_login") { popUpTo("rider_dashboard") { inclusive = true } }
                                    }''',
    '''onLogout = {
                                        riderViewModel.logout()
                                        navController.navigate("rider_login") { popUpTo("rider_dashboard") { inclusive = true } }
                                    },
                                    onNavigateToEarnings = {
                                        navController.navigate("rider_earnings")
                                    }'''
)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(main_content)
