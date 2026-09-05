import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            composable("profile") { ProfileScreen(viewModel) }
        }"""

replacement = """            composable("profile") { ProfileScreen(viewModel, navController) }
            composable("quickReplies") { QuickRepliesScreen(viewModel, navController) }
        }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
