import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """        if (isLoading) {
            Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).pointerInput(Unit) { detectTapGestures { } }, contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFF00B4D8))
            }
        }"""

replacement = """        androidx.compose.animation.AnimatedVisibility(
            visible = isLoading,
            enter = androidx.compose.animation.fadeIn(),
            exit = androidx.compose.animation.fadeOut()
        ) {
            Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).pointerInput(Unit) { detectTapGestures { } }, contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFF00B4D8))
            }
        }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
    print("Patched MainActivity.kt")
else:
    print("Target not found in MainActivity.kt")
