with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Let's ensure IME handling is configured
import re
target = """class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {"""

replacement = """class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        androidx.core.view.WindowCompat.setDecorFitsSystemWindows(window, false)"""

if target in content and "setDecorFitsSystemWindows" not in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Added WindowCompat.setDecorFitsSystemWindows")
else:
    print("Already exists or pattern not found")

