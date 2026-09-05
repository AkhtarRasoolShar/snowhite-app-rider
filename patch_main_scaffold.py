import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace RadarScreen entirely
match_start = content.find("fun RadarScreen(viewModel: RiderViewModel) {")
if match_start == -1:
    print("Could not find RadarScreen")
    exit(1)

match_end = content.find("fun StatusBadge(", match_start)
if match_end == -1:
    print("Could not find end of RadarScreen")
    exit(1)

end_index = content.rfind("}", match_start, match_end)

new_radar = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions(),
        onResult = { permissions: Map<String, Boolean> ->
            if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
                viewModel.fetchAvailableOrders(context)
            }
        }
    )
    
    LaunchedEffect(Unit) {
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
        }
    }

    val orders by viewModel.availableOrders.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }
    val radarSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var sortOption by remember { mutableStateOf("Newest") }
    var expandedSortMenu by remember { mutableStateOf(false) }
    
    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
            "Proximity" -> orders.sortedBy { it.distanceInMeters ?: Float.MAX_VALUE }
            "Hub" -> orders.sortedBy { it.zone ?: "" }
            else -> orders.sortedByDescending { it.orderId?.toIntOrNull() ?: 0 }
        }
    }

    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }

    // Clean Layout Hierarchy: No Overlapping Full-Size Boxes
    Column(modifier = Modifier.fillMaxSize().background(Color(0xFFF5F6FA))) {
        // Premium Delivery Header
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
                    Text(
                        "Radar Active",
                        color = Color.LightGray,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
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
        }
        
        if (orders.isEmpty() && !isLoading) {
            Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
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
                }
            }
        } else if (!isLoading) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "${sortedOrders.size} Available",
                    fontWeight = FontWeight.Bold,
                    color = Color.DarkGray,
                    fontSize = 16.sp
                )
                Box {
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = Color.White,
                        shadowElevation = 2.dp,
                        modifier = Modifier.clickable { expandedSortMenu = true }
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.FilterList, contentDescription = "Sort", tint = Color(0xFF03045E), modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(6.dp))
                            Text(sortOption, color = Color(0xFF03045E), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        }
                    }
                    DropdownMenu(
                        expanded = expandedSortMenu,
                        onDismissRequest = { expandedSortMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Newest") },
                            onClick = { sortOption = "Newest"; expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Total Amount") },
                            onClick = { sortOption = "Total Amount"; expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Proximity") },
                            onClick = { sortOption = "Proximity"; expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Hub (Zone)") },
                            onClick = { sortOption = "Hub"; expandedSortMenu = false }
                        )
                    }
                }
            }
            
            // Clean 2-column Grid Layout
            androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
                columns = androidx.compose.foundation.lazy.grid.GridCells.Fixed(2),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
                modifier = Modifier.weight(1f).fillMaxWidth()
            ) {
                androidx.compose.foundation.lazy.grid.items(
                    items = sortedOrders,
                    key = { it.orderId ?: 0 }
                ) { order ->
                    Card(
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                    ) {
                        Column(modifier = Modifier.padding(12.dp).fillMaxWidth()) {
                            Text(
                                "Order #${order.orderId}",
                                fontWeight = FontWeight.ExtraBold,
                                color = Color(0xFF03045E),
                                fontSize = 14.sp
                            )
                            Spacer(Modifier.height(4.dp))
                            Text(
                                "PKR ${order.totalAmount ?: "0"}",
                                color = Color(0xFF00B4D8),
                                fontWeight = FontWeight.ExtraBold,
                                fontSize = 14.sp
                            )
                            Spacer(Modifier.height(8.dp))
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.DateRange, contentDescription = "Date", tint = Color.Gray, modifier = Modifier.size(12.dp))
                                Spacer(Modifier.width(4.dp))
                                Text(order.date ?: "Just now", color = Color.DarkGray, fontSize = 11.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            }
                            Spacer(Modifier.height(4.dp))
                            Row(verticalAlignment = Alignment.Top) {
                                Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(12.dp).padding(top = 2.dp))
                                Spacer(Modifier.width(4.dp))
                                Text(order.pickupAddress ?: "N/A", color = Color.DarkGray, fontSize = 11.sp, maxLines = 2, overflow = TextOverflow.Ellipsis)
                            }
                            Spacer(Modifier.height(12.dp))
                            Button(
                                onClick = { selectedOrderForReview = order },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                shape = RoundedCornerShape(8.dp),
                                modifier = Modifier.fillMaxWidth(),
                                contentPadding = PaddingValues(vertical = 8.dp)
                            ) {
                                Text("REVIEW", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            }
                        }
                    }
                }
            }
        }
    }

    if (selectedOrderForReview != null) {
        ModalBottomSheet(
            onDismissRequest = { selectedOrderForReview = null },
            sheetState = radarSheetState,
            containerColor = Color.White,
            modifier = Modifier.fillMaxHeight(0.9f)
        ) {
            OrderDetailsSheetContent(
                order = selectedOrderForReview!!,
                isHistory = false,
                onAccept = {
                    viewModel.acceptOrder(selectedOrderForReview!!.orderId.toString(), context)
                    selectedOrderForReview = null
                },
                onReject = {
                    viewModel.rejectOrder(selectedOrderForReview!!.orderId ?: "", context)
                    selectedOrderForReview = null
                }
            )
        }
    }
}
"""

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content[:match_start] + new_radar + "\n" + content[end_index+1:])

