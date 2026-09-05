import re

with open('app/src/main/java/com/example/RiderUI.kt', 'r') as f:
    content = f.read()

# 1. Add Pickup Address Section
old_customer_section_end = """                }
            }
        }
        Spacer(Modifier.height(24.dp))
        
        Text("Total Amount: PKR ${order.totalAmount ?: "0"}", color = Color(0xFF2E7D32), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)"""

new_pickup_address_section = """                }
            }
        }
        Spacer(Modifier.height(16.dp))
        
        // Pickup Address Section
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF8F9FA)),
            elevation = CardDefaults.cardElevation(0.dp),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Pickup Address", fontSize = 14.sp, color = Color.Gray)
                Spacer(Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color(0xFF03045E), modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(order.pickupAddress ?: "Unknown Location", fontWeight = FontWeight.Medium, fontSize = 16.sp, color = Color(0xFF03045E))
                }
            }
        }
        Spacer(Modifier.height(24.dp))
        
        Text("Total Amount: PKR ${order.totalAmount ?: "0"}", color = Color(0xFF2E7D32), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)"""

if old_customer_section_end in content:
    content = content.replace(old_customer_section_end, new_pickup_address_section)
else:
    print("Could not find old customer section end")


# 2. Fix Garments breakdown UI
old_garments_ui = """                items(orderItems) { item ->
                    ListItem(
                        colors = ListItemDefaults.colors(containerColor = Color(0xFFF8F9FA)),
                        headlineContent = { Text(item.name ?: "Unknown Item", fontWeight = FontWeight.Medium, color = Color(0xFF03045E)) },
                        leadingContent = { 
                            Box(
                                modifier = Modifier.background(Color(0xFF00B4D8).copy(alpha = 0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 12.dp, vertical = 6.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("${item.quantity ?: 1}x", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                            }
                        }
                    )
                }"""

new_garments_ui = """                items(orderItems) { item ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFFF8F9FA), RoundedCornerShape(8.dp))
                            .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(text = "${item.quantity ?: 1}x", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                        Text(text = item.name ?: "Laundry Garment", color = Color(0xFF03045E), modifier = Modifier.padding(start = 8.dp))
                    }
                }"""

if old_garments_ui in content:
    content = content.replace(old_garments_ui, new_garments_ui)
else:
    print("Could not find old garments ui")

with open('app/src/main/java/com/example/RiderUI.kt', 'w') as f:
    f.write(content)

