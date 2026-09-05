with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

if "import androidx.compose.ui.platform.LocalContext" not in content:
    content = content.replace("import androidx.compose.ui.platform.LocalDensity", "import androidx.compose.ui.platform.LocalDensity\nimport androidx.compose.ui.platform.LocalContext\nimport android.content.Context")

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
