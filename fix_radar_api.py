with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_get_orders = """    @GET("routes.php?action=get_available_orders")
    suspend fun getAvailableOrders(@Query("zone") zone: String): Response<GenericResponse<List<RiderOrder>>>"""
new_get_orders = """    @GET("routes.php?action=get_available_orders")
    suspend fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: Int): Response<GenericResponse<List<RiderOrder>>>
    
    @POST("routes.php?action=reject_order")
    suspend fun rejectOrder(@Body request: Map<String, Int>): Response<GenericResponse<Unit>>"""
content = content.replace(old_get_orders, new_get_orders)

old_fetch = """    fun fetchAvailableOrders(context: Context) {
        val zone = _riderZone.value
        if (zone.isEmpty()) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.getAvailableOrders(zone)"""
new_fetch = """    fun fetchAvailableOrders(context: Context) {
        val zone = _riderZone.value
        val riderId = _riderId.value
        if (zone.isEmpty() || riderId == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.getAvailableOrders(zone, riderId)"""
content = content.replace(old_fetch, new_fetch)

old_accept = """    fun acceptOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.acceptOrder(AcceptOrderRequest(orderId, id))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Accepted!", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to accept order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }"""
new_accept = """    fun acceptOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.acceptOrder(AcceptOrderRequest(orderId, id))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Accepted!", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to accept order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun rejectOrder(orderId: Int, context: Context) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val request = mapOf("order_id" to orderId, "rider_id" to id)
                val response = RetrofitClient.apiService.rejectOrder(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Rejected", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to reject order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }"""
content = content.replace(old_accept, new_accept)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
