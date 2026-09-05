import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.foundation.lazy.grid.items(", "items(")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
