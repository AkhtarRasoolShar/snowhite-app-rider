with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

old_dashboard = r'''@Composable
fun RiderDashboardScreen\(viewModel: RiderViewModel, onNavigateToRadar: \(\) -> Unit\) \{
    val riderName by viewModel\.riderName\.collectAsState\(\)
    val myOrders by viewModel\.myOrders\.collectAsState\(\)
    
    // Calculate simple stats from existing data
    val completedOrders = myOrders\.count \{ it\.status == "DELIVERED" \}
    val totalEarnings = myOrders\.filter \{ it\.status == "DELIVERED" \}\.sumOf \{ it\.totalAmount\?\.toDoubleOrNull\(\) \?: 0\.0 \}
    
    Column\(
        modifier = Modifier\.fillMaxSize\(\)\.background\(Color\(0xFFF8FAFC\)\)\.padding\(16\.dp\)
    \) \{
        // Header
        Row\(
            verticalAlignment = Alignment\.CenterVertically,
            modifier = Modifier\.fillMaxWidth\(\)\.padding\(top = 24\.dp, bottom = 24\.dp\)
        \) \{
            if \(\!viewModel\.appSettings\.logo_url\.isNullOrEmpty\(\)\) \{
                coil\.compose\.AsyncImage\(
                    model = viewModel\.appSettings\.logo_url,
                    contentDescription = "Logo",
                    modifier = Modifier\.size\(50\.dp\)
                \)
            \}
            Spacer\(modifier = Modifier\.width\(12\.dp\)\)
            Column \{
                Text\("Welcome back,", color = Color\.Gray, fontSize = 14\.sp\)
                Text\(text = riderName\.ifEmpty \{ "Captain" \}, fontSize = 22\.sp, fontWeight = FontWeight\.Bold, color = Color\(0xFF0F172A\)\)
            \}
        \}

        // Stats Cards
        Row\(modifier = Modifier\.fillMaxWidth\(\), horizontalArrangement = Arrangement\.spacedBy\(12\.dp\)\) \{
            // Earnings Card
            Card\(
                modifier = Modifier\.weight\(1f\)\.height\(120\.dp\),
                colors = CardDefaults\.cardColors\(containerColor = Color\(0xFF0EA5E9\)\),
                shape = RoundedCornerShape\(16\.dp\)
            \) \{
                Column\(modifier = Modifier\.fillMaxSize\(\)\.padding\(16\.dp\), verticalArrangement = Arrangement\.Center\) \{
                    Icon\(Icons\.Default\.AccountBalanceWallet, contentDescription = null, tint = Color\.White\.copy\(alpha = 0\.8f\)\)
                    Spacer\(modifier = Modifier\.height\(8\.dp\)\)
                    Text\("Total Earnings", color = Color\.White\.copy\(alpha = 0\.8f\), fontSize = 12\.sp\)
                    Text\("PKR \$totalEarnings", color = Color\.White, fontSize = 18\.sp, fontWeight = FontWeight\.Bold\)
                \}
            \}

            // Completed Orders Card
            Card\(
                modifier = Modifier\.weight\(1f\)\.height\(120\.dp\),
                colors = CardDefaults\.cardColors\(containerColor = Color\.White\),
                elevation = CardDefaults\.cardElevation\(defaultElevation = 2\.dp\),
                shape = RoundedCornerShape\(16\.dp\)
            \) \{
                Column\(modifier = Modifier\.fillMaxSize\(\)\.padding\(16\.dp\), verticalArrangement = Arrangement\.Center\) \{
                    Icon\(Icons\.Default\.CheckCircle, contentDescription = null, tint = Color\(0xFF10B981\)\)
                    Spacer\(modifier = Modifier\.height\(8\.dp\)\)
                    Text\("Completed Orders", color = Color\.Gray, fontSize = 12\.sp\)
                    Text\("\$completedOrders", color = Color\(0xFF0F172A\), fontSize = 18\.sp, fontWeight = FontWeight\.Bold\)
                \}
            \}
        \}
        
        Spacer\(modifier = Modifier\.height\(32\.dp\)\)
        
        Text\("Quick Actions", fontSize = 18\.sp, fontWeight = FontWeight\.Bold, color = Color\(0xFF0F172A\)\)
        Spacer\(modifier = Modifier\.height\(16\.dp\)\)
        
        Button\(
            onClick = onNavigateToRadar,
            modifier = Modifier\.fillMaxWidth\(\)\.height\(60\.dp\),
            colors = ButtonDefaults\.buttonColors\(containerColor = Color\(0xFF03045E\)\),
            shape = RoundedCornerShape\(16\.dp\)
        \) \{
            Icon\(Icons\.Default\.LocationSearching, contentDescription = null, tint = Color\.White\)
            Spacer\(modifier = Modifier\.width\(12\.dp\)\)
            Text\("Go to Radar \(Find Orders\)", color = Color\.White, fontSize = 16\.sp, fontWeight = FontWeight\.Bold\)
        \}
    \}
\}'''

new_dashboard = '''@Composable
fun RiderDashboardScreen(viewModel: RiderViewModel, onNavigateToRadar: () -> Unit) {
    val riderName by viewModel.riderName.collectAsState()
    val myOrders by viewModel.myOrders.collectAsState()
    
    val completedOrders = myOrders.count { it.status == "DELIVERED" }
    val totalEarnings = myOrders.filter { it.status == "DELIVERED" }.sumOf { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
    
    // Take the 5 most recent orders for the dashboard
    val recentOrders = myOrders.take(5)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF8FAFC)) 
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {
        // --- HEADER SECTION ---
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp, top = 8.dp)
        ) {
            Column {
                Text("Welcome back,", color = Color(0xFF64748B), fontSize = 14.sp)
                Text(text = riderName.ifEmpty { "Captain" }, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color(0xFF0F172A))
            }
        }

        // --- STATS CARDS SECTION ---
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            // Earnings Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF0EA5E9))
            ) {
                Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White)
                    Column {
                        Text("Total Earnings", color = Color.White.copy(alpha = 0.8f), fontSize = 12.sp)
                        Text("${viewModel.appSettings.currency ?: "PKR"} $totalEarnings", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            // Completed Orders Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF10B981))
                    Column {
                        Text("Completed Orders", color = Color.Gray, fontSize = 12.sp)
                        Text("$completedOrders", color = Color(0xFF0F172A), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // --- QUICK ACTION (RADAR) ---
        Text("Quick Actions", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A), modifier = Modifier.padding(bottom = 12.dp))
        Button(
            onClick = { onNavigateToRadar() },
            modifier = Modifier.fillMaxWidth().height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0B192C)),
            shape = RoundedCornerShape(12.dp)
        ) {
            Icon(Icons.Default.Radar, contentDescription = null, tint = Color.White)
            Spacer(modifier = Modifier.width(12.dp))
            Text("Go to Radar (Find Orders)", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }

        Spacer(modifier = Modifier.height(32.dp))

        // --- RECENT ORDERS (HISTORY) SECTION ---
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Recent Orders", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
        }

        if (recentOrders.isEmpty()) {
            Box(modifier = Modifier.fillMaxWidth().padding(top = 32.dp), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.ListAlt, contentDescription = null, modifier = Modifier.size(48.dp), tint = Color.LightGray)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("No recent orders found.", color = Color.Gray, fontSize = 14.sp)
                }
            }
        } else {
            recentOrders.forEach { order ->
                // Determine Status Colors dynamically
                val statusColor = when (order.status) {
                    "DELIVERED" -> Color(0xFF10B981) // Green
                    "PENDING", "COLLECTING" -> Color(0xFFF59E0B) // Orange
                    "RECEIVED_AT_HUB", "WASHING", "READY_FOR_DELIVERY" -> Color(0xFF3B82F6) // Blue
                    else -> Color.Gray
                }

                val statusText = order.status?.replace("_", " ") ?: "UNKNOWN"

                Card(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Order #${order.orderId}", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color(0xFF0F172A))
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(order.date ?: "", fontSize = 12.sp, color = Color.Gray)
                        }
                        
                        Column(horizontalAlignment = Alignment.End) {
                            Text(
                                text = "${viewModel.appSettings.currency ?: "PKR"} ${order.totalAmount}", 
                                fontWeight = FontWeight.ExtraBold, 
                                fontSize = 16.sp, 
                                color = Color(0xFF0F172A)
                            )
                            Spacer(modifier = Modifier.height(6.dp))
                            
                            // Status Badge
                            Text(
                                text = statusText, 
                                fontSize = 10.sp, 
                                color = statusColor, 
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier
                                    .background(statusColor.copy(alpha = 0.15f), RoundedCornerShape(6.dp))
                                    .padding(horizontal = 8.dp, vertical = 4.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}'''

content = re.sub(old_dashboard, new_dashboard, content, flags=re.DOTALL)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
