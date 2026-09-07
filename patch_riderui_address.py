import re

with open("app/src/main/java/com/example/RiderUI.kt", "r") as f:
    content = f.read()

target = """                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color(0xFF03045E), modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(order.pickupAddress ?: "Unknown Location", fontWeight = FontWeight.Medium, fontSize = 16.sp, color = Color(0xFF03045E))
                }"""

replacement = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = order.pickupAddress ?: "Unknown Location", 
                        fontSize = 14.sp, 
                        modifier = Modifier.weight(1f),
                        color = Color(0xFF1E293B)
                    )
                    
                    // NATIVE GOOGLE MAPS INTENT BUTTON
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
                            .size(40.dp)
                            .background(Color(0xFFE0F2FE), shape = androidx.compose.foundation.shape.CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Place, // Or Navigation icon
                            contentDescription = "Navigate",
                            tint = Color(0xFF0284C7)
                        )
                    }
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/RiderUI.kt", "w") as f:
    f.write(content)
