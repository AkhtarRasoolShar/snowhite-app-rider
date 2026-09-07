import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                NavigationBar(containerColor = Color.White, tonalElevation = 8.dp) {
                    
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Radar, contentDescription = "Radar") },
                    label = { Text("Radar") },
                    selected = currentRoute == "radar",
                    onClick = { navController.navigate("radar") { launchSingleTop = true } },
                    colors = NavigationBarItemDefaults.colors(selectedIconColor = TealAccent, selectedTextColor = TealAccent)
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.List, contentDescription = "History") },
                    label = { Text("History") },
                    selected = currentRoute == "history",
                    onClick = { navController.navigate("history") { launchSingleTop = true } },
                    colors = NavigationBarItemDefaults.colors(selectedIconColor = TealAccent, selectedTextColor = TealAccent)
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                    label = { Text("Profile") },
                    selected = currentRoute == "profile",
                    onClick = { navController.navigate("profile") { launchSingleTop = true } },
                    colors = NavigationBarItemDefaults.colors(selectedIconColor = TealAccent, selectedTextColor = TealAccent)
                )
            }"""

replacement = """                NavigationBar(containerColor = Color.White) {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.LocationSearching, "Radar") },
                        label = { Text("Radar") },
                        selected = currentRoute == "radar",
                        onClick = { navController.navigate("radar") { launchSingleTop = true } },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Color(0xFF00B4D8), 
                            selectedTextColor = Color(0xFF00B4D8), 
                            indicatorColor = Color(0xFFE0F7FA),
                            unselectedIconColor = Color.Gray,
                            unselectedTextColor = Color.Gray
                        )
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.AutoMirrored.Filled.List, "History") },
                        label = { Text("History") },
                        selected = currentRoute == "history",
                        onClick = { navController.navigate("history") { launchSingleTop = true } },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Color(0xFF00B4D8), 
                            selectedTextColor = Color(0xFF00B4D8), 
                            indicatorColor = Color(0xFFE0F7FA),
                            unselectedIconColor = Color.Gray,
                            unselectedTextColor = Color.Gray
                        )
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Person, "Profile") },
                        label = { Text("Profile") },
                        selected = currentRoute == "profile",
                        onClick = { navController.navigate("profile") { launchSingleTop = true } },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Color(0xFF00B4D8), 
                            selectedTextColor = Color(0xFF00B4D8), 
                            indicatorColor = Color(0xFFE0F7FA),
                            unselectedIconColor = Color.Gray,
                            unselectedTextColor = Color.Gray
                        )
                    )
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
