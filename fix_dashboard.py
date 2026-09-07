with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

old_dashboard = r'''@Composable
fun RiderDashboardScreen\(viewModel: RiderViewModel, onNavigateToRadar: \(\) -> Unit\) \{
    val riderName by viewModel\.riderName\.collectAsState\(\)
    
    // Calculate simple stats from existing data
    val completedOrders = viewModel\.riderOrders\.count \{ it\.status == "DELIVERED" \}
    val totalEarnings = viewModel\.riderOrders\.filter \{ it\.status == "DELIVERED" \}\.sumOf \{ it\.total_amount \?: 0\.0 \}
    
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
                    Text\("\$\{viewModel\.appSettings\.currency \?: "PKR"\} \$totalEarnings", color = Color\.White, fontSize = 18\.sp, fontWeight = FontWeight\.Bold\)
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
    
    // Calculate simple stats from existing data
    val completedOrders = myOrders.count { it.status == "DELIVERED" }
    val totalEarnings = myOrders.filter { it.status == "DELIVERED" }.sumOf { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
    
    Column(
        modifier = Modifier.fillMaxSize().background(Color(0xFFF8FAFC)).padding(16.dp)
    ) {
        // Header
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth().padding(top = 24.dp, bottom = 24.dp)
        ) {
            if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                coil.compose.AsyncImage(
                    model = viewModel.appSettings.logo_url,
                    contentDescription = "Logo",
                    modifier = Modifier.size(50.dp)
                )
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text("Welcome back,", color = Color.Gray, fontSize = 14.sp)
                Text(text = riderName.ifEmpty { "Captain" }, fontSize = 22.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
            }
        }

        // Stats Cards
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            // Earnings Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF0EA5E9)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.Center) {
                    Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White.copy(alpha = 0.8f))
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("Total Earnings", color = Color.White.copy(alpha = 0.8f), fontSize = 12.sp)
                    Text("PKR $totalEarnings", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                }
            }

            // Completed Orders Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.Center) {
                    Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF10B981))
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("Completed Orders", color = Color.Gray, fontSize = 12.sp)
                    Text("$completedOrders", color = Color(0xFF0F172A), fontSize = 18.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text("Quick Actions", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = onNavigateToRadar,
            modifier = Modifier.fillMaxWidth().height(60.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF03045E)),
            shape = RoundedCornerShape(16.dp)
        ) {
            Icon(Icons.Default.LocationSearching, contentDescription = null, tint = Color.White)
            Spacer(modifier = Modifier.width(12.dp))
            Text("Go to Radar (Find Orders)", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}'''

content = re.sub(old_dashboard, new_dashboard, content, flags=re.DOTALL)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
