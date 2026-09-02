import sys

target = """                Text("Order #${selectedOrderForUpdate!!.order_id}", color = Color.Gray)
                Spacer(Modifier.height(16.dp))

                var expandedStatus by remember { mutableStateOf(false) }"""

replacement = """                Text("Order #${selectedOrderForUpdate!!.order_id}", color = Color.Gray)
                Spacer(Modifier.height(24.dp))
                
                val orderItems = selectedOrderForUpdate!!.items
                if (!orderItems.isNullOrEmpty()) {
                    Text("Order Items", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = DarkBlue)
                    Spacer(Modifier.height(8.dp))
                    LazyColumn(
                        modifier = Modifier.fillMaxWidth().heightIn(max = 250.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(orderItems) { item ->
                            ListItem(
                                colors = ListItemDefaults.colors(containerColor = SoftWhite),
                                headlineContent = { Text(item.name ?: "Unknown Item", fontWeight = FontWeight.Medium, color = DarkBlue) },
                                leadingContent = { 
                                    Box(
                                        modifier = Modifier.background(TealAccent.copy(alpha = 0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 12.dp, vertical = 6.dp),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text("${item.quantity ?: 1}x", color = TealAccent, fontWeight = FontWeight.Bold)
                                    }
                                }
                            )
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                }

                var expandedStatus by remember { mutableStateOf(false) }"""

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

new_content = content.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)

print("Replaced:", target in content)
