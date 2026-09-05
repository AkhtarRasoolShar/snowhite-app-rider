with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    "androidx.compose.material.icons.Icons.AutoMirrored.Filled.Message",
    "androidx.compose.material.icons.Icons.Default.Email"
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
