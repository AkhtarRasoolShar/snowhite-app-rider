import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Insert StatusBadge before HistoryScreen
status_badge_code = """@Composable
fun StatusBadge(status: String) {
    val formattedStatus = status.replace("_", " ")
        .lowercase()
        .split(" ")
        .joinToString(" ") { it.replaceFirstChar { char -> char.uppercase() } }
    
    val (bgColor, textColor) = when (status.uppercase()) {
        "DELIVERED" -> Color(0xFFE8F5E9) to Color(0xFF2E7D32)
        "OUT_FOR_DELIVERY" -> Color(0xFFE3F2FD) to Color(0xFF1565C0)
        "IN_WASHING", "RECEIVED_AT_HUB" -> Color(0xFFFFF3E0) to Color(0xFFEF6C00)
        "COLLECTING", "PENDING" -> Color(0xFFEDE7F6) to Color(0xFF4527A0)
        else -> Color(0xFFF5F5F5) to Color(0xFF616161)
    }

    Box(
        modifier = Modifier
            .background(bgColor, RoundedCornerShape(8.dp))
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(
            text = formattedStatus,
            color = textColor,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen"""

if "fun StatusBadge(" not in content:
    content = content.replace("""@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen""", status_badge_code)


# 2. Replace the Card block in items(orders)
old_card_pattern = r"Card\(\s*elevation = CardDefaults\.cardElevation\(defaultElevation = 2\.dp\),.*?Row\(modifier = Modifier\.fillMaxWidth\(\)\.padding\(16\.dp\).*?Text\(\"Update\", fontSize = 12\.sp, color = Color\.White\)\s*\}\s*\}\s*\}\s*\}"
# Wait, let's use exact string replacement for safety, since we read the exact code earlier.

old_card = """                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp), 
                            colors = CardDefaults.cardColors(containerColor = Color.White), 
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.clickable { selectedOrderForUpdate = order }
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text("Order #${order.orderId}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E), fontSize = 16.sp)
                                    Spacer(Modifier.height(4.dp))
                                    Text("PKR ${order.totalAmount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                                    Spacer(Modifier.height(8.dp))
                                    Text("Status: $currentStatus", color = Color.Gray, fontSize = 14.sp)
                                }
                                Column(horizontalAlignment = Alignment.End) {
                                    IconButton(
                                        onClick = { printReceipt(context, order) },
                                        modifier = Modifier.background(SoftWhite, RoundedCornerShape(8.dp))
                                    ) {
                                        Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print", tint = Color(0xFF03045E))
                                    }
                                    Spacer(Modifier.height(12.dp))
                                    Button(
                                        onClick = { showStatusDialogForOrder = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(8.dp),
                                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                                    ) {
                                        Text("Update", fontSize = 12.sp, color = Color.White)
                                    }
                                }
                            }
                        }"""

new_card = """                        androidx.compose.material3.ElevatedCard(
                            elevation = CardDefaults.elevatedCardElevation(defaultElevation = 4.dp), 
                            colors = CardDefaults.elevatedCardColors(containerColor = Color.White), 
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForUpdate = order }
                        ) {
                            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Top) {
                                    Column {
                                        Text("Order #${order.orderId}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E), fontSize = 16.sp)
                                        Spacer(Modifier.height(4.dp))
                                        Text(order.date ?: "N/A", color = Color.Gray, fontSize = 12.sp)
                                    }
                                    Text("PKR ${order.totalAmount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.ExtraBold, fontSize = 16.sp)
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                StatusBadge(status = currentStatus)
                                Spacer(Modifier.height(16.dp))
                                
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Button(
                                            onClick = { showStatusDialogForOrder = order },
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                            shape = RoundedCornerShape(8.dp),
                                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                                        ) {
                                            Text("Update Status", fontSize = 12.sp, color = Color.White, fontWeight = FontWeight.Bold)
                                        }
                                        androidx.compose.material3.OutlinedButton(
                                            onClick = { selectedOrderForUpdate = order },
                                            shape = RoundedCornerShape(8.dp),
                                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                                        ) {
                                            Text("View Details", fontSize = 12.sp, color = Color(0xFF03045E))
                                        }
                                    }
                                    IconButton(
                                        onClick = { navController.navigate("chat/${order.orderId}") },
                                        modifier = Modifier.background(Color(0xFFE3F2FD), androidx.compose.foundation.shape.CircleShape).size(40.dp)
                                    ) {
                                        Icon(androidx.compose.material.icons.Icons.AutoMirrored.Filled.Message, contentDescription = "Chat", tint = Color(0xFF1565C0), modifier = Modifier.size(20.dp))
                                    }
                                }
                            }
                        }"""

content = content.replace(old_card, new_card)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

