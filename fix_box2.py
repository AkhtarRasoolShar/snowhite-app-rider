import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("clickable(enabled = false) {}", "pointerInput(Unit) { detectTapGestures { } }")

# ensure pointerInput and detectTapGestures are imported
if "import androidx.compose.ui.input.pointer.pointerInput" not in content:
    content = content.replace("import androidx.compose.foundation.clickable", "import androidx.compose.foundation.clickable\nimport androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.foundation.gestures.detectTapGestures")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
