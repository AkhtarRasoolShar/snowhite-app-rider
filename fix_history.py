import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

start_marker = "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun HistoryScreen"
end_marker = "fun ProfileScreen("

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    history_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val orders by viewModel.myOrders.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }

    LaunchedEffect(Unit) {
        viewModel.fetchMyOrders(context)
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.92f)))
        
        Column(modifier = Modifier.fillMaxSize()) {
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            } else if (orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Default.HourglassEmpty, contentDescription = "Empty", tint = Color.LightGray, modifier = Modifier.size(64.dp))
                        Spacer(Modifier.height(16.dp))
                        Text("No orders in your history.", color = Color.Gray)
                    }
                }
            } else {
                LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxSize()) {
                    items(orders) { order ->
                        val currentStatus = order.status ?: "Pending"
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp), 
                            colors = CardDefaults.cardColors(containerColor = Color.White), 
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.clickable { selectedOrderForUpdate = order }
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text("Order #${order.order_id}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E), fontSize = 16.sp)
                                    Spacer(Modifier.height(4.dp))
                                    Text("PKR ${order.total_amount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
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
                                        onClick = { selectedOrderForUpdate = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(8.dp),
                                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                                    ) {
                                        Text("Update", fontSize = 12.sp, color = Color.White)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        if (selectedOrderForUpdate != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForUpdate = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Column {
                            Text("Update Order Status", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                            Spacer(Modifier.height(8.dp))
                            Text("Order #${selectedOrderForUpdate!!.order_id}", color = Color.Gray)
                        }
                        IconButton(onClick = { printReceipt(context, selectedOrderForUpdate!!) }) {
                            Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print Receipt", tint = Color(0xFF00B4D8))
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                    
                    val orderItems = selectedOrderForUpdate!!.items
                    if (!orderItems.isNullOrEmpty()) {
                        Text("Order Items", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                        Spacer(Modifier.height(8.dp))
                        LazyColumn(
                            modifier = Modifier.fillMaxWidth().heightIn(max = 250.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(orderItems) { item ->
                                ListItem(
                                    colors = ListItemDefaults.colors(containerColor = SoftWhite),
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
                    }
                    
                    Text("Select New Status", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                    Spacer(Modifier.height(16.dp))
                    
                    val statuses = listOf("Pending", "Accepted", "Out for Pickup", "Picked Up", "Washing", "Ready for Delivery", "Out for Delivery", "Delivered")
                    var expandedStatus by remember { mutableStateOf(false) }
                    
                    ExposedDropdownMenuBox(
                        expanded = expandedStatus,
                        onExpandedChange = { expandedStatus = it }
                    ) {
                        OutlinedTextField(
                            value = selectedOrderForUpdate!!.status ?: "Pending",
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Status") },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedStatus) },
                            modifier = Modifier.menuAnchor().fillMaxWidth(),
                            colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Color(0xFF00B4D8))
                        )
                        ExposedDropdownMenu(
                            expanded = expandedStatus,
                            onDismissRequest = { expandedStatus = false }
                        ) {
                            statuses.forEach { st ->
                                DropdownMenuItem(
                                    text = { Text(st) },
                                    onClick = { 
                                        viewModel.updateOrderStatus(selectedOrderForUpdate!!.order_id?.toString() ?: "", st, context)
                                        expandedStatus = false
                                        selectedOrderForUpdate = null
                                    }
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
"""
    new_content = content[:start_idx] + history_screen + content[end_idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(new_content)
else:
    print("Could not find markers")
