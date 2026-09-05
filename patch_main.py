import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Remove the one at the start of onCreate
content = content.replace("        androidx.core.view.WindowCompat.setDecorFitsSystemWindows(window, false)\n        super.onCreate(savedInstanceState)", "        super.onCreate(savedInstanceState)")

# Ensure import is present if not
if "import androidx.core.view.WindowCompat" not in content:
    content = content.replace("import androidx.activity.compose.setContent", "import androidx.activity.compose.setContent\nimport androidx.core.view.WindowCompat")

# Add right before setContent
if "WindowCompat.setDecorFitsSystemWindows(window, false)\n        setContent {" not in content:
    content = content.replace("        setContent {", "        WindowCompat.setDecorFitsSystemWindows(window, false)\n        setContent {")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
