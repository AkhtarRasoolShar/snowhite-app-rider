with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

theme_code = """
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme

@Composable
fun MyApplicationTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = lightColorScheme(
            primary = DeepNavy,
            secondary = TealAccent,
            background = SoftWhite
        ),
        content = content
    )
}

class MainActivity : ComponentActivity() {
"""

content = content.replace("class MainActivity : ComponentActivity() {", theme_code)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
