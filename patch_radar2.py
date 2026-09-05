import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

radar_screen_pattern = r'(fun RadarScreen\(.*?\).*?items\(sortedOrders, key = \{ it\.order_id \?: it\.hashCode\(\) \}\) \{ order ->).*?(} // End items\s*})'
# wait, finding the end of the item block is hard with regex. 
# let's just find the start of the LazyColumn in RadarScreen and replace the whole thing.

start_str = "items(sortedOrders, key = { it.order_id ?: it.hashCode() }) { order ->"
end_str = "                }\n                Spacer(Modifier.height(80.dp))" # end of LazyColumn

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    old_items_block = content[start_idx:end_idx]
    
    new_items_block = """items(sortedOrders, key = { it.order_id ?: it.hashCode() }) { order ->
                        val alpha = remember { Animatable(0f) }
                        val translateY = remember { Animatable(50f) }
                        
                        LaunchedEffect(order.order_id) {
                            launch { alpha.animateTo(1f, animationSpec = tween(400)) }
                            launch { translateY.animateTo(0f, animationSpec = tween(400, easing = FastOutSlowInEasing)) }
                        }
                        
                        Box(modifier = Modifier.graphicsLayer(alpha = alpha.value, translationY = translateY.value)) {
                            ModernOrderCard(
                                order = order,
                                onAccept = { viewModel.acceptOrder(order.order_id.toString(), context) },
                                onReject = { viewModel.rejectOrder(order.order_id ?: 0, context) },
                                onViewDetails = { selectedOrderForReview = order; showReviewSheet = true }
                            )
                        }
                    }
"""
    content = content[:start_idx] + new_items_block + content[end_idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Replaced items block")
else:
    print("Could not find start or end")

