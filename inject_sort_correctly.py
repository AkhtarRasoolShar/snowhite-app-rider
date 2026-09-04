import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure DropdownMenu, DropdownMenuItem are imported
imports = """import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
"""
if "import androidx.compose.material3.DropdownMenu" not in content:
    content = content.replace("import androidx.compose.material3.Text", imports + "import androidx.compose.material3.Text")

# 1. Inject state into RadarScreen
# Use a specific anchor for RadarScreen
radar_anchor = """    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }"""
radar_state = """    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }
    var sortOption by remember { mutableStateOf("Newest") }
    var expandedSortMenu by remember { mutableStateOf(false) }
    
    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.total_amount?.toDoubleOrNull() ?: 0.0 }
            else -> orders.sortedByDescending { it.order_id ?: 0 }
        }
    }"""
content = content.replace(radar_anchor, radar_state, 1)

# 2. Inject UI and change items(orders) in RadarScreen
# The LazyColumn in RadarScreen
old_lazy_column = """            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(orders) { order ->"""

new_lazy_column = """            } else {
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
                            color = Color(0xFFF0F4F8),
                            modifier = Modifier.clickable { expandedSortMenu = true }
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Default.FilterList, contentDescription = "Sort", tint = Color(0xFF03045E), modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(6.dp))
                                Text(sortOption, color = Color(0xFF03045E), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Spacer(Modifier.width(4.dp))
                                Icon(Icons.Default.ArrowDropDown, contentDescription = "Drop", tint = Color(0xFF03045E))
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
                        }
                    }
                }
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(sortedOrders) { order ->"""

content = content.replace(old_lazy_column, new_lazy_column, 1)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
