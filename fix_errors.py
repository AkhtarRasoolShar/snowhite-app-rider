import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("Modifier.fillMaxSize()", "androidx.compose.ui.Modifier.fillMaxSize()")
content = content.replace("Modifier.padding(24.dp)", "androidx.compose.ui.Modifier.padding(24.dp)")
content = content.replace("Modifier.height(24.dp)", "androidx.compose.ui.Modifier.height(24.dp)")
content = content.replace("Modifier.fillMaxWidth()", "androidx.compose.ui.Modifier.fillMaxWidth()")
content = content.replace("Modifier.height(16.dp)", "androidx.compose.ui.Modifier.height(16.dp)")
content = content.replace("Modifier.height(32.dp)", "androidx.compose.ui.Modifier.height(32.dp)")
content = content.replace("Modifier.height(52.dp)", "androidx.compose.ui.Modifier.height(52.dp)")

content = content.replace("com.example.ui.theme.RiderTheme", "RiderTheme")
content = content.replace("androidx.activity.enableEdgeToEdge()", "enableEdgeToEdge()")
content = content.replace("androidx.activity.compose.setContent", "setContent")
content = content.replace("androidx.navigation.compose.composable", "composable")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
