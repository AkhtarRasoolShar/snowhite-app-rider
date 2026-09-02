import re
with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'ProfileScreen(onOpenDrawer = { scope.launch { drawerState.open() } })',
    'ProfileScreen(viewModel = viewModel, onOpenDrawer = { scope.launch { drawerState.open() } }, onLogout = { scope.launch { drawerState.close() }; viewModel.logout(); navController.navigate("home") { popUpTo(0) } })'
)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
