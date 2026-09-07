import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add sortOption state and haversine method to RiderViewModel
target_viewmodel = """    private val _pendingApproval = MutableStateFlow(false)"""
replacement_viewmodel = """    private val _pendingApproval = MutableStateFlow(false)
    
    private val _sortOption = MutableStateFlow("Newest")
    val sortOption: StateFlow<String> = _sortOption

    fun setSortOption(option: String) {
        _sortOption.value = option
    }

    private fun calculateHaversineDistance(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Float {
        val R = 6371e3 // Earth radius in meters
        val phi1 = Math.toRadians(lat1)
        val phi2 = Math.toRadians(lat2)
        val deltaPhi = Math.toRadians(lat2 - lat1)
        val deltaLambda = Math.toRadians(lon2 - lon1)
        val a = kotlin.math.sin(deltaPhi / 2) * kotlin.math.sin(deltaPhi / 2) +
                kotlin.math.cos(phi1) * kotlin.math.cos(phi2) *
                kotlin.math.sin(deltaLambda / 2) * kotlin.math.sin(deltaLambda / 2)
        val c = 2 * kotlin.math.atan2(kotlin.math.sqrt(a), kotlin.math.sqrt(1 - a))
        return (R * c).toFloat()
    }"""
content = content.replace(target_viewmodel, replacement_viewmodel)

# Update calculateDistances in RiderViewModel
target_calc = """                                    val resultsArray = FloatArray(1)
                                    Location.distanceBetween(
                                        location.latitude, location.longitude,
                                        loc.latitude, loc.longitude,
                                        resultsArray
                                    )
                                    order.copy(distanceInMeters = resultsArray[0])"""
replacement_calc = """                                    val distance = calculateHaversineDistance(
                                        location.latitude, location.longitude,
                                        loc.latitude, loc.longitude
                                    )
                                    order.copy(distanceInMeters = distance)"""
content = content.replace(target_calc, replacement_calc)

# Update UI states in RadarScreen
target_ui_state = """    var sortOption by remember { mutableStateOf("Newest") }
    var expandedSortMenu by remember { mutableStateOf(false) }
    
    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
            "Proximity" -> orders.sortedBy { it.distanceInMeters ?: Float.MAX_VALUE }
            "Hub" -> orders.sortedBy { it.zone ?: "" }
            else -> orders.sortedByDescending { it.orderId?.toIntOrNull() ?: 0 }
        }
    }"""
replacement_ui_state = """    val sortOption by viewModel.sortOption.collectAsState()
    var expandedSortMenu by remember { mutableStateOf(false) }
    
    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
            "Distance (Haversine)" -> orders.sortedBy { it.distanceInMeters ?: Float.MAX_VALUE }
            "Hub" -> orders.sortedBy { it.zone ?: "" }
            else -> orders.sortedByDescending { it.orderId?.toIntOrNull() ?: 0 }
        }
    }"""
content = content.replace(target_ui_state, replacement_ui_state)

# Update Dropdown Menu in RadarScreen
target_dropdown = """                    DropdownMenu(
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
replacement_dropdown = """                    DropdownMenu(
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
                    }"""
content = content.replace(target_dropdown, replacement_dropdown)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
