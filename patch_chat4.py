import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

target = "    Scaffold(\n        modifier = Modifier.imePadding(),"
replacement = "    Scaffold(\n        modifier = Modifier.fillMaxSize().imePadding(),"
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
