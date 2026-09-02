import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

start_marker = "fun RadarScreen(viewModel: RiderViewModel) {"
end_marker = "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun HistoryScreen"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    radar_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val orders by viewModel.availableOrders.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }

    val infiniteTransition = rememberInfiniteTransition()
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulsingDot"
    )

    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1545060894-7b57f0f6c271?q=80&w=1000",
            contentDescription = "Laundry Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.85f)))
        
        Column(modifier = Modifier.fillMaxSize()) {
            // Glassmorphism Header
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
            }
            
            if (isLoading && orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            } else if (orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.Search, 
                            contentDescription = "Empty", 
                            tint = Color.Gray.copy(alpha = 0.5f), 
                            modifier = Modifier.size(80.dp)
                        )
                        Spacer(Modifier.height(16.dp))
                        Text(
                            "No new orders right now.\\nKeep your radar on!", 
                            color = Color.DarkGray, 
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium,
                            textAlign = TextAlign.Center
                        )
                        Spacer(Modifier.height(24.dp))
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(orders) { order ->
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().height(IntrinsicSize.Min)) {
                                // Subtle Left Border
                                Box(
                                    modifier = Modifier
                                        .width(6.dp)
                                        .fillMaxHeight()
                                        .background(Color(0xFF03045E))
                                )
                                Column(modifier = Modifier.padding(16.dp).weight(1f)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            "Order #${order.order_id}",
                                            fontWeight = FontWeight.ExtraBold,
                                            color = Color(0xFF03045E),
                                            fontSize = 18.sp
                                        )
                                        Text(
                                            "PKR ${order.total_amount ?: "0"}",
                                            color = Color(0xFF00B4D8),
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 18.sp
                                        )
                                    }
                                    Spacer(Modifier.height(12.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(
                                            Icons.Default.DateRange,
                                            contentDescription = "Date",
                                            tint = Color.Gray,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Spacer(Modifier.width(8.dp))
                                        Text(
                                            order.date ?: "Just now",
                                            color = Color.DarkGray,
                                            fontSize = 14.sp
                                        )
                                    }
                                    Spacer(Modifier.height(6.dp))
                                    Row(verticalAlignment = Alignment.Top) {
                                        Icon(
                                            Icons.Default.LocationOn,
                                            contentDescription = "Location",
                                            tint = Color.Gray,
                                            modifier = Modifier.size(16.dp).padding(top = 2.dp)
                                        )
                                        Spacer(Modifier.width(8.dp))
                                        Text(
                                            order.pickup_address ?: "N/A",
                                            color = Color.DarkGray,
                                            fontSize = 14.sp,
                                            lineHeight = 20.sp
                                        )
                                    }
                                    Spacer(Modifier.height(16.dp))
                                    Button(
                                        onClick = { selectedOrderForReview = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(12.dp),
                                        modifier = Modifier.fillMaxWidth(),
                                        contentPadding = PaddingValues(vertical = 14.dp)
                                    ) {
                                        Text("REVIEW ORDER", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        if (selectedOrderForReview != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForReview = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
                    Text("Order #${selectedOrderForReview!!.order_id}", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                    Spacer(Modifier.height(8.dp))
                    Text("Total Amount: PKR ${selectedOrderForReview!!.total_amount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(24.dp))
                    
                    val orderItems = selectedOrderForReview!!.items
                    if (!orderItems.isNullOrEmpty()) {
                        Text("Order Items", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                        Spacer(Modifier.height(8.dp))
                        LazyColumn(
                            modifier = Modifier.fillMaxWidth().heightIn(max = 250.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(orderItems) { item ->
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
                            }
                        }
                        Spacer(Modifier.height(24.dp))
                    } else {
                        Text("No items listed.", color = Color.Gray)
                        Spacer(Modifier.height(24.dp))
                    }
                    
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        Button(
                            onClick = { 
                                val orderId = selectedOrderForReview!!.order_id
                                if (orderId != null) {
                                    viewModel.rejectOrder(orderId, context)
                                }
                                selectedOrderForReview = null
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                            border = BorderStroke(1.dp, Color.Red),
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp),
                            contentPadding = PaddingValues(vertical = 14.dp)
                        ) {
                            Text("REJECT", color = Color.Red, fontWeight = FontWeight.Bold)
                        }
                        
                        Button(
                            onClick = { 
                                val orderIdStr = selectedOrderForReview!!.order_id?.toString() ?: ""
                                viewModel.acceptOrder(orderIdStr, context)
                                selectedOrderForReview = null
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp),
                            contentPadding = PaddingValues(vertical = 14.dp)
                        ) {
                            Text("ACCEPT", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}

"""
    new_content = content[:start_idx] + radar_screen + content[end_idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(new_content)
else:
    print("Markers not found")

