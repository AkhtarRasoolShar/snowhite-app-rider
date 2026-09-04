import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure permissions launcher is imported
imports = """import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
"""
if "import androidx.activity.compose.rememberLauncherForActivityResult" not in content:
    content = content.replace("import androidx.compose.material3.Text", imports + "import androidx.compose.material3.Text")

# Update sortedOrders logic
old_sort_logic = """    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.total_amount?.toDoubleOrNull() ?: 0.0 }
            else -> orders.sortedByDescending { it.order_id ?: 0 }
        }
    }"""

new_sort_logic = """    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.total_amount?.toDoubleOrNull() ?: 0.0 }
            "Proximity" -> orders.sortedBy { it.distanceInMeters ?: Float.MAX_VALUE }
            "Hub" -> orders.sortedBy { it.zone ?: "" }
            else -> orders.sortedByDescending { it.order_id ?: 0 }
        }
    }"""

content = content.replace(old_sort_logic, new_sort_logic)

# Update dropdown menu items
old_dropdown = """                        DropdownMenu(
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
                        }"""

new_dropdown = """                        DropdownMenu(
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
                        }"""

content = content.replace(old_dropdown, new_dropdown)

# Add Permission Launcher to RadarScreen
radar_start = """fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current"""

radar_start_new = """fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
            viewModel.fetchAvailableOrders(context)
        }
    }
    
    LaunchedEffect(Unit) {
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
        }
    }
"""

if "permissionLauncher.launch" not in content:
    content = content.replace(radar_start, radar_start_new)

# Update the distance UI inside the order card (only in RadarScreen)
# Add it near the order amount or status.
# Let's find: `Text("PKR ${order.total_amount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)`
old_order_ui = """                                        Text(
                                            "PKR ${order.total_amount ?: "0"}",
                                            color = Color(0xFF00B4D8),
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 18.sp
                                        )
                                    }
                                    Spacer(Modifier.height(8.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) {"""

new_order_ui = """                                        Text(
                                            "PKR ${order.total_amount ?: "0"}",
                                            color = Color(0xFF00B4D8),
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 18.sp
                                        )
                                    }
                                    Spacer(Modifier.height(4.dp))
                                    if (order.distanceInMeters != null) {
                                        Text(
                                            String.format("%.1f km away", order.distanceInMeters!! / 1000f),
                                            color = Color.Gray,
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.SemiBold
                                        )
                                    }
                                    if (order.zone != null) {
                                        Text(
                                            "Hub: ${order.zone}",
                                            color = Color.Gray,
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.SemiBold
                                        )
                                    }
                                    Spacer(Modifier.height(8.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) {"""

content = content.replace(old_order_ui, new_order_ui)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
