import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure TextOverflow is imported
if "import androidx.compose.ui.text.style.TextOverflow" not in content:
    content = content.replace("import androidx.compose.ui.text.style.TextAlign", "import androidx.compose.ui.text.style.TextAlign\nimport androidx.compose.ui.text.style.TextOverflow")

old_header = """            // Glassmorphism Header
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                color = Color.White.copy(alpha = 0.6f),
                shape = RoundedCornerShape(24.dp),
                border = BorderStroke(1.dp, Color.White.copy(alpha = 0.8f)),
                shadowElevation = 0.dp
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.LocationOn,
                        contentDescription = "Radar",
                        tint = Color(0xFF00B4D8),
                        modifier = Modifier.size(28.dp)
                    )
                    Spacer(Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            "Searching in: ${zone.uppercase()}",
                            fontWeight = FontWeight.ExtraBold,
                            fontSize = 18.sp,
                            color = Color(0xFF03045E)
                        )
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(8.dp)
                                    .background(Color.Green.copy(alpha = alpha), CircleShape)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                "Live Radar Active",
                                color = Color.Gray,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                    IconButton(
                        onClick = { viewModel.fetchAvailableOrders(context) },
                        modifier = Modifier.background(Color.White, CircleShape).size(40.dp)
                    ) {
                        Icon(Icons.Default.Refresh, contentDescription = "Refresh", tint = Color(0xFF00B4D8))
                    }
                }
            }"""

new_header = """            // Premium Delivery Header
            Card(
                modifier = Modifier.fillMaxWidth(),
                elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF03045E)),
                shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
            ) {
                Row(
                    modifier = Modifier.padding(20.dp).fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(10.dp)
                                    .background(Color.Green.copy(alpha = alpha), CircleShape)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                "Radar Active",
                                color = Color.LightGray,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                        Spacer(Modifier.height(4.dp))
                        Text(
                            "Searching in:",
                            color = Color.LightGray,
                            fontSize = 12.sp
                        )
                        Text(
                            zone.uppercase(),
                            fontWeight = FontWeight.ExtraBold,
                            fontSize = 20.sp,
                            color = Color.White,
                            maxLines = 2,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    Spacer(Modifier.width(16.dp))
                    IconButton(
                        onClick = { viewModel.fetchAvailableOrders(context) },
                        modifier = Modifier.background(Color(0xFF00B4D8), CircleShape).size(48.dp)
                    ) {
                        Icon(Icons.Default.Refresh, contentDescription = "Refresh", tint = Color.White)
                    }
                }
            }"""

if old_header in content:
    content = content.replace(old_header, new_header)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Header successfully replaced.")
else:
    print("Old header not found! Trying a regex fallback.")
    # Fallback to regex or manual search
