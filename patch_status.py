with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. API Models
target_api = """data class UpdateStatusRequest(val rider_id: Int, val status: String)"""
replace_api = """data class UpdateStatusRequest(val rider_id: Int, val status: String)
data class UpdateOrderStatusRequest(val order_id: String, val status: String)"""
content = content.replace(target_api, replace_api)

# 2. API Endpoint
target_endpoint = """    @PATCH("routes.php?action=update_status")
    suspend fun updateStatus(@Body request: UpdateStatusRequest): Response<GenericResponse<Unit>>
}"""
replace_endpoint = """    @PATCH("routes.php?action=update_status")
    suspend fun updateStatus(@Body request: UpdateStatusRequest): Response<GenericResponse<Unit>>

    @POST("routes.php?action=update_order_status")
    suspend fun updateOrderStatus(@Body request: UpdateOrderStatusRequest): Response<GenericResponse<Unit>>
}"""
content = content.replace(target_endpoint, replace_endpoint)

# 3. ViewModel function
target_vm = """    fun acceptOrder(order: RiderOrderResponse, context: Context) {"""
replace_vm = """    fun updateOrderStatus(orderId: String, newStatus: String, context: Context) {
        val currentList = _acceptedOrders.value.toMutableList()
        val index = currentList.indexOfFirst { it.order_id == orderId }
        if (index != -1) {
            currentList[index] = currentList[index].copy(status = newStatus)
            _acceptedOrders.value = currentList
            Toast.makeText(context, "Order status updated to $newStatus", Toast.LENGTH_SHORT).show()
            
            viewModelScope.launch {
                try {
                    RetrofitClient.apiService.updateOrderStatus(UpdateOrderStatusRequest(orderId, newStatus))
                } catch (e: Exception) {
                    // Fail silently in background
                }
            }
        }
    }

    fun acceptOrder(order: RiderOrderResponse, context: Context) {"""
content = content.replace(target_vm, replace_vm)

# 4. History Screen UI
target_ui = """                            Column {
                                Text("Order #${order.order_id}", fontWeight = FontWeight.Bold, color = DarkBlue, fontSize = 16.sp)
                                Spacer(Modifier.height(4.dp))
                                Text("PKR ${order.total_amount ?: 0}", color = TealAccent, fontWeight = FontWeight.Bold)
                                Spacer(Modifier.height(4.dp))
                                Text("Status: Processing", color = Color.Gray, fontSize = 12.sp)
                            }"""
replace_ui = """                            Column {
                                Text("Order #${order.order_id}", fontWeight = FontWeight.Bold, color = DarkBlue, fontSize = 16.sp)
                                Spacer(Modifier.height(4.dp))
                                Text("PKR ${order.total_amount ?: 0}", color = TealAccent, fontWeight = FontWeight.Bold)
                                Spacer(Modifier.height(8.dp))
                                
                                var expandedStatus by remember { mutableStateOf(false) }
                                val statuses = listOf("Pending Pickup", "Picked Up", "In Washing", "Out for Delivery", "Delivered")
                                val currentStatus = order.status ?: "Pending Pickup"
                                
                                Box {
                                    Row(
                                        modifier = Modifier
                                            .background(TealAccent.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                                            .clickable { expandedStatus = true }
                                            .padding(horizontal = 8.dp, vertical = 6.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(currentStatus, color = TealAccent, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                        Spacer(Modifier.width(4.dp))
                                        Icon(Icons.Default.ArrowDropDown, contentDescription = "Change Status", tint = TealAccent, modifier = Modifier.size(16.dp))
                                    }
                                    DropdownMenu(expanded = expandedStatus, onDismissRequest = { expandedStatus = false }) {
                                        statuses.forEach { st ->
                                            DropdownMenuItem(
                                                text = { Text(st) },
                                                onClick = { 
                                                    viewModel.updateOrderStatus(order.order_id, st, context)
                                                    expandedStatus = false 
                                                }
                                            )
                                        }
                                    }
                                }
                            }"""
content = content.replace(target_ui, replace_ui)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
