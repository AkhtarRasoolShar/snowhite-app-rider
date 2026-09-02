import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add imports
if "import androidx.compose.ui.graphics.graphicsLayer" not in content:
    content = content.replace("import androidx.compose.ui.graphics.Color", "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.graphics.StrokeCap")

old_loading_block = """            if (isLoading && orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            }"""

new_loading_block = """            if (isLoading && orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    SophisticatedLoadingIndicator()
                }
            }"""

content = content.replace(old_loading_block, new_loading_block)

sophisticated_loading_code = """
@Composable
fun SophisticatedLoadingIndicator() {
    val infiniteTransition = rememberInfiniteTransition(label = "loading")
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotation"
    )
    val scale by infiniteTransition.animateFloat(
        initialValue = 0.8f,
        targetValue = 1.2f,
        animationSpec = infiniteRepeatable(
            animation = tween(800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "scale"
    )

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.size(80.dp)) {
            // Outer rotating ring
            CircularProgressIndicator(
                modifier = Modifier.fillMaxSize().graphicsLayer { rotationZ = rotation },
                color = Color(0xFF00B4D8),
                strokeWidth = 3.dp,
                trackColor = Color(0xFF03045E).copy(alpha = 0.1f)
            )
            // Inner rotating ring (opposite direction)
            CircularProgressIndicator(
                modifier = Modifier.size(50.dp).graphicsLayer { rotationZ = -rotation },
                color = Color(0xFF03045E),
                strokeWidth = 4.dp,
                strokeCap = StrokeCap.Round
            )
            // Center pulsing icon
            Icon(
                Icons.Default.LocationOn,
                contentDescription = null,
                tint = Color(0xFF00B4D8),
                modifier = Modifier.size(24.dp).graphicsLayer {
                    scaleX = scale
                    scaleY = scale
                }
            )
        }
        Spacer(Modifier.height(24.dp))
        Text(
            "Scanning for orders...",
            color = Color(0xFF03045E),
            fontWeight = FontWeight.SemiBold,
            fontSize = 16.sp,
            modifier = Modifier.graphicsLayer { alpha = if (scale < 1f) scale else 2f - scale }
        )
    }
}
"""

if "fun SophisticatedLoadingIndicator" not in content:
    content = content + "\n" + sophisticated_loading_code

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
