import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

content = content.replace("@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.layout.ExperimentalLayoutApi::class)")

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
