import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure graphicsLayer is imported
if "import androidx.compose.ui.graphics.graphicsLayer" not in content:
    content = content.replace("import androidx.compose.ui.graphics.Color", "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.graphicsLayer")

old_items_block = """                    items(sortedOrders) { order ->
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {"""

new_items_block = """                    items(sortedOrders, key = { it.order_id ?: it.hashCode() }) { order ->
                        val alpha = remember { Animatable(0f) }
                        val translateY = remember { Animatable(50f) }
                        
                        LaunchedEffect(order.order_id) {
                            launch { alpha.animateTo(1f, animationSpec = tween(400)) }
                            launch { translateY.animateTo(0f, animationSpec = tween(400, easing = FastOutSlowInEasing)) }
                        }
                        
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .graphicsLayer {
                                    this.alpha = alpha.value
                                    this.translationY = translateY.value
                                }
                                .clickable { selectedOrderForReview = order }
                        ) {"""

content = content.replace(old_items_block, new_items_block)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
