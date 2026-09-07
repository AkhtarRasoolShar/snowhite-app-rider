import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            Row(verticalAlignment = Alignment.Top) {
                                Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(12.dp).padding(top = 2.dp))
                                Spacer(Modifier.width(4.dp))
                                Text(order.pickupAddress ?: "N/A", color = Color.DarkGray, fontSize = 11.sp, maxLines = 2, overflow = TextOverflow.Ellipsis)
                            }"""

replacement = """                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(12.dp))
                                Spacer(Modifier.width(4.dp))
                                Text(
                                    text = order.pickupAddress ?: "N/A", 
                                    fontSize = 11.sp, 
                                    modifier = Modifier.weight(1f),
                                    color = Color.DarkGray,
                                    maxLines = 2,
                                    overflow = TextOverflow.Ellipsis
                                )
                                
                                IconButton(
                                    onClick = {
                                        try {
                                            val gmmIntentUri = android.net.Uri.parse("geo:0,0?q=${android.net.Uri.encode(order.pickupAddress ?: "")}")
                                            val mapIntent = android.content.Intent(android.content.Intent.ACTION_VIEW, gmmIntentUri)
                                            mapIntent.setPackage("com.google.android.apps.maps")
                                            context.startActivity(mapIntent)
                                        } catch (e: Exception) {
                                            android.widget.Toast.makeText(context, "Google Maps is not installed", android.widget.Toast.LENGTH_SHORT).show()
                                        }
                                    },
                                    modifier = Modifier
                                        .size(32.dp)
                                        .background(Color(0xFFE0F2FE), shape = androidx.compose.foundation.shape.CircleShape)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Place,
                                        contentDescription = "Navigate",
                                        tint = Color(0xFF0284C7),
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
