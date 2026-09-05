import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route"""

content = content.replace(target, "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
