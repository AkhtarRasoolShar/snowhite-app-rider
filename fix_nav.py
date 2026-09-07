with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# We will replace the MainAppScreen NavigationBar block with the requested one
new_nav = """NavigationBar(containerColor = Color.White) {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.LocationSearching, contentDescription = "Radar") },
                    label = { Text("Radar") },
                    selected = currentRoute == "radar",
                    onClick = { navController.navigate("radar") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
                NavigationBarItem(
                    icon = { Icon(Icons.AutoMirrored.Filled.List, contentDescription = "History") },
                    label = { Text("History") },
                    selected = currentRoute == "history",
                    onClick = { navController.navigate("history") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                    label = { Text("Profile") },
                    selected = currentRoute == "profile",
                    onClick = { navController.navigate("profile") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
            }"""

start = content.find("NavigationBar(containerColor = Color.White, tonalElevation = 8.dp) {")
if start != -1:
    end = content.find("}\n            }", start) + 1
    content = content[:start] + new_nav + content[end:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
