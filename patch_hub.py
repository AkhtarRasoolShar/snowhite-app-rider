with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add updateRiderZone to ViewModel
target_1 = """    fun saveBankDetails(context: Context, bName: String, bIban: String) {"""
replace_1 = """    fun updateRiderZone(context: Context, newZone: String) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().putString("rider_zones", newZone).apply()
        _riderZone.value = newZone
        Toast.makeText(context, "Operating Hub updated to $newZone", Toast.LENGTH_SHORT).show()
        fetchOrders()
    }

    fun saveBankDetails(context: Context, bName: String, bIban: String) {"""
content = content.replace(target_1, replace_1)


# 2. Add variables for the dropdown in ProfileScreen
target_2 = """    var inputAddress by remember { mutableStateOf(riderAddress) }"""
replace_2 = """    var inputAddress by remember { mutableStateOf(riderAddress) }
    var expandedZone by remember { mutableStateOf(false) }
    val zones = listOf("Clifton", "Tariq Road", "DHA", "Gulshan")"""
content = content.replace(target_2, replace_2)


# 3. Add the Hub Selector Card in ProfileScreen
target_3 = """            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Home Address","""
replace_3 = """            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Operating Hub", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.padding(bottom = 12.dp))
                        ExposedDropdownMenuBox(expanded = expandedZone, onExpandedChange = { expandedZone = !expandedZone }) {
                            OutlinedTextField(
                                value = zone,
                                onValueChange = {},
                                readOnly = true,
                                label = { Text("Select Active Hub") },
                                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedZone) },
                                modifier = Modifier.menuAnchor().fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                            ExposedDropdownMenu(expanded = expandedZone, onDismissRequest = { expandedZone = false }) {
                                zones.forEach { selectionOption ->
                                    DropdownMenuItem(
                                        text = { Text(selectionOption) },
                                        onClick = {
                                            viewModel.updateRiderZone(context, selectionOption)
                                            expandedZone = false
                                        }
                                    )
                                }
                            }
                        }
                    }
                }
                Spacer(Modifier.height(24.dp))
            }

            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Home Address","""
content = content.replace(target_3, replace_3)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
