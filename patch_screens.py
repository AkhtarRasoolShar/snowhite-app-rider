import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace RadarScreen
start = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun RadarScreen")
if start == -1:
    print("Could not find RadarScreen")
    exit(1)
    
end = content.find("fun StatusBadge", start)
if end == -1:
    end = content.find("@Composable\nfun StatusBadge", start)

if end == -1:
    print("Could not find end of RadarScreen")
    exit(1)

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
    val sortOption by viewModel.sortOption.collectAsState()
    var expandedSortMenu by remember { mutableStateOf(false) }
    
    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
            "Distance (Haversine)" -> orders.sortedBy { it.distanceInMeters ?: Float.MAX_VALUE }
            "Hub" -> orders.sortedBy { it.zone ?: "" }
            else -> orders.sortedByDescending { it.orderId?.toIntOrNull() ?: 0 }
        }
    }

    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }

    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Premium Header
            Surface(
                color = Color.White,
                shadowElevation = 2.dp,
                shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(24.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(10.dp).background(Color(0xFF00C853), CircleShape))
                                Spacer(Modifier.width(8.dp))
                                Text("Online & Searching", color = Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                            }
                            Spacer(Modifier.height(8.dp))
                            Text(zone.uppercase(), fontWeight = FontWeight.ExtraBold, fontSize = 22.sp, color = Color(0xFF1E293B))
                        }
                        IconButton(
                            onClick = { viewModel.fetchAvailableOrders(context) },
                            modifier = Modifier.background(Color(0xFFF1F5F9), CircleShape)
                        ) {
                            Icon(Icons.Default.Refresh, contentDescription = "Refresh", tint = Color(0xFF00B4D8))
                        }
                    }
                }
            }
            
            // Available & Sorting
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "${sortedOrders.size} Requests",
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF1E293B),
                    fontSize = 18.sp
                )
                Box {
                    Surface(
                        shape = RoundedCornerShape(20.dp),
                        color = Color.White,
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0)),
                        modifier = Modifier.clickable { expandedSortMenu = true }
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.Sort, contentDescription = "Sort", tint = Color(0xFF64748B), modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(6.dp))
                            Text(sortOption, color = Color(0xFF334155), fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                        }
                    }
                    DropdownMenu(
                        expanded = expandedSortMenu,
                        onDismissRequest = { expandedSortMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Newest") },
                            onClick = { viewModel.setSortOption("Newest"); expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Total Amount") },
                            onClick = { viewModel.setSortOption("Total Amount"); expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Distance (Haversine)") },
                            onClick = { viewModel.setSortOption("Distance (Haversine)"); expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Hub (Zone)") },
                            onClick = { viewModel.setSortOption("Hub"); expandedSortMenu = false }
                        )
                    }
                }
            }

            if (sortedOrders.isEmpty() && !isLoading) {
                Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.Radar, 
                            contentDescription = "Searching", 
                            tint = Color.LightGray, 
                            modifier = Modifier.size(64.dp)
                        )
                        Spacer(Modifier.height(16.dp))
                        Text(
                            "No new requests nearby", 
                            color = Color.Gray, 
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium
                        )
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 20.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.weight(1f).fillMaxWidth()
                ) {
                    items(
                        items = sortedOrders,
                        key = { it.orderId ?: 0 }
                    ) { order ->
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {
                            Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        "Order #${order.orderId}",
                                        fontWeight = FontWeight.Black,
                                        color = Color(0xFF0F172A),
                                        fontSize = 16.sp
                                    )
                                    Text(
                                        "PKR ${order.totalAmount ?: "0"}",
                                        color = Color(0xFF00B4D8),
                                        fontWeight = FontWeight.Black,
                                        fontSize = 16.sp
                                    )
                                }
                                Spacer(Modifier.height(8.dp))
                                
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.AccessTime, contentDescription = "Date", tint = Color(0xFF64748B), modifier = Modifier.size(14.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text(order.date ?: "Just now", color = Color(0xFF64748B), fontSize = 13.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                HorizontalDivider(color = Color(0xFFF1F5F9))
                                Spacer(Modifier.height(12.dp))
                                
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(Icons.Default.Place, contentDescription = "Location", tint = Color(0xFF64748B), modifier = Modifier.size(20.dp))
                                    Spacer(Modifier.width(12.dp))
                                    Text(
                                        text = order.pickupAddress ?: "N/A", 
                                        fontSize = 14.sp, 
                                        modifier = Modifier.weight(1f),
                                        color = Color(0xFF334155),
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
                                            .size(40.dp)
                                            .background(Color(0xFFE0F2FE), shape = CircleShape)
                                    ) {
                                        Icon(
                                            imageVector = Icons.Default.Directions,
                                            contentDescription = "Navigate",
                                            tint = Color(0xFF0284C7),
                                            modifier = Modifier.size(20.dp)
                                        )
                                    }
                                }
                                
                                Spacer(Modifier.height(16.dp))
                                Button(
                                    onClick = { selectedOrderForReview = order },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                    shape = RoundedCornerShape(12.dp),
                                    modifier = Modifier.fillMaxWidth().height(48.dp)
                                ) {
                                    Text("REVIEW & ACCEPT", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                }
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

@Composable
"""
content = content[:start] + new_radar + content[end+12:]

# Replace ProfileScreen
start2 = content.find("fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController)")
if start2 == -1:
    print("Could not find ProfileScreen")
    exit(1)
end2 = content.find("fun AuthFlow(viewModel: RiderViewModel, navController: NavHostController)", start2)
if end2 == -1:
    end2 = content.find("@Composable\nfun AuthFlow", start2)

new_profile = """fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
    val name by viewModel.riderName.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    
    var address by remember { mutableStateOf(viewModel.homeAddress.value) }
    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }
    var whatsapp by remember { mutableStateOf(if (viewModel.whatsappNumber.value.isNotEmpty()) viewModel.whatsappNumber.value else viewModel.riderPhone.value) }

    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Header
            Surface(
                color = Color.White,
                shadowElevation = 2.dp,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .background(Color(0xFFE0F2FE), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            if (name.isNotEmpty()) name.take(1).uppercase() else "U",
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF00B4D8)
                        )
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(name.ifEmpty { "Driver" }, fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = Color(0xFF1E293B))
                    Spacer(Modifier.height(4.dp))
                    Surface(color = Color(0xFFF1F5F9), shape = RoundedCornerShape(12.dp)) {
                        Text("Hub: ${zone.ifEmpty { "N/A" }}", modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp), color = Color(0xFF475569), fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                    }
                }
            }
            
            LazyColumn(
                contentPadding = PaddingValues(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                item {
                    Text("Account Details", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(Modifier.height(8.dp))
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            OutlinedTextField(
                                value = address,
                                onValueChange = { address = it },
                                label = { Text("Home Address") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                            Spacer(Modifier.height(12.dp))
                            OutlinedTextField(
                                value = whatsapp,
                                onValueChange = { whatsapp = it },
                                label = { Text("WhatsApp Number") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                        }
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    Text("Bank Information", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(Modifier.height(8.dp))
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            OutlinedTextField(
                                value = bankName,
                                onValueChange = { bankName = it },
                                label = { Text("Bank Name") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                            Spacer(Modifier.height(12.dp))
                            OutlinedTextField(
                                value = bankIban,
                                onValueChange = { bankIban = it },
                                label = { Text("IBAN / Account Number") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                        }
                    }
                    
                    Spacer(Modifier.height(32.dp))
                    Button(
                        onClick = { 
                            viewModel.saveProfileDetails(context, address, bankName, bankIban, viewModel.quickReply1.value, viewModel.quickReply2.value)
                            viewModel.updateWhatsApp(context, whatsapp) 
                        },
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text("SAVE CHANGES", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    Text("Preferences & Support", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(Modifier.height(8.dp))
                    
                    OutlinedButton(
                        onClick = { navController.navigate("quickReplies") },
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        shape = RoundedCornerShape(12.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0))
                    ) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = Color(0xFF334155), modifier = Modifier.size(20.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Manage Quick Replies", color = Color(0xFF334155), fontWeight = FontWeight.SemiBold)
                    }
                    
                    Spacer(Modifier.height(12.dp))
                    Button(
                        onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/923001234567"))
                            try { context.startActivity(intent) } catch (e: Exception) { Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show() }
                        },
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF25D366)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(Icons.Default.SupportAgent, contentDescription = "Help", tint = Color.White)
                        Spacer(Modifier.width(8.dp))
                        Text("Customer Support", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    TextButton(
                        onClick = { viewModel.logout(context) },
                        modifier = Modifier.fillMaxWidth().height(52.dp)
                    ) {
                        Icon(Icons.Default.PowerSettingsNew, contentDescription = "Logout", tint = Color(0xFFEF4444))
                        Spacer(Modifier.width(8.dp))
                        Text("Sign Out", color = Color(0xFFEF4444), fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.height(32.dp))
                }
            }
        }
    }
}

@Composable
"""
# Note: AuthFlow starts after ProfileScreen
content = content[:start2] + new_profile + content[end2-12:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
