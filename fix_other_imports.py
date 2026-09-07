with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """
import java.util.Locale
import androidx.compose.ui.text.style.TextAlign
"""

content = content.replace("package com.example\n", "package com.example\n" + imports)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
