import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# find RiderViewModel
start = content.find('class RiderViewModel : ViewModel() {')
end = content.find('// --- Theme ---')

if start == -1 or end == -1:
    print("Could not find ViewModel")
    exit(1)

vm_content = content[start:end]

# Now, I will replace all the broken methods with the right methods using python regexes.
# Actually, I have the correct methods. I will just completely replace the viewmodel.

new_vm = """class RiderViewModel : ViewModel() {
    private val _riderId = MutableStateFlow<Int>(-1)
    val riderId: StateFlow<Int> = _riderId
    
    private val _riderName = MutableStateFlow("")
    val riderName: StateFlow<String> = _riderName
    
    private val _riderPhone = MutableStateFlow("")
    val riderPhone: StateFlow<String> = _riderPhone
    
    private val _whatsappNumber = MutableStateFlow("")
    val whatsappNumber: StateFlow<String> = _whatsappNumber
    
    private val _riderZone = MutableStateFlow("")
    val riderZone: StateFlow<String> = _riderZone
    
    private val _homeAddress = MutableStateFlow("")
    val homeAddress: StateFlow<String> = _homeAddress
    
    private val _bankName = MutableStateFlow("")
    val bankName: StateFlow<String> = _bankName
    
    private val _bankIban = MutableStateFlow("")
    val bankIban: StateFlow<String> = _bankIban
    
    private val _quickReply1 = MutableStateFlow("I am on my way!")
    val quickReply1: StateFlow<String> = _quickReply1
    
    private val _quickReply2 = MutableStateFlow("I have arrived at the pickup location.")
    val quickReply2: StateFlow<String> = _quickReply2

    private val _availableOrders = MutableStateFlow<List<RiderOrder>>(emptyList())
    val availableOrders: StateFlow<List<RiderOrder>> = _availableOrders
    
    private val _myOrders = MutableStateFlow<List<RiderOrder>>(emptyList())
    val myOrders: StateFlow<List<RiderOrder>> = _myOrders

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading
    
    private val _authError = MutableStateFlow<String?>(null)
    val authError: StateFlow<String?> = _authError

    private val _pendingApproval = MutableStateFlow(false)
    val pendingApproval: StateFlow<Boolean> = _pendingApproval
    
    private val pendingActions = mutableListOf<PendingAction>()

    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: ""
        _bankName.value = prefs.getString("bank_name", "") ?: ""
        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
        _quickReply1.value = prefs.getString("quick_reply_1", "I am on my way!") ?: "I am on my way!"
        _quickReply2.value = prefs.getString("quick_reply_2", "I have arrived at the pickup location.") ?: "I have arrived at the pickup location."
        
        try {
            val connectivityManager = context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
            val request = android.net.NetworkRequest.Builder()
                .addCapability(android.net.NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .build()
            connectivityManager.registerNetworkCallback(request, object : android.net.ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: android.net.Network) {
                    retryPendingActions(context)
                }
            })
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun retryPendingActions(context: Context) {
        val actionsToRetry = pendingActions.toList()
        pendingActions.clear()
        actionsToRetry.forEach { action ->
            when (action) {
                is PendingAction.AcceptOrder -> acceptOrder(action.orderId, context)
                is PendingAction.RejectOrder -> rejectOrder(action.orderId, context)
                is PendingAction.UpdateOrderStatus -> updateOrderStatus(action.orderId, action.newStatus, context)
            }
        }
    }

    fun updateWhatsApp(context: Context, whatsapp: String) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val request = mapOf("rider_id" to id.toString(), "whatsapp_number" to whatsapp)
                val response = RetrofitClient.apiService.updateProfile(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
                    prefs.edit().putString("whatsapp_number", whatsapp).apply()
                    _whatsappNumber.value = whatsapp
                    Toast.makeText(context, "Profile Updated!", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update profile", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun clearError() {
        _authError.value = null
    }

    fun login(phone: String, pass: String, context: Context, onSuccess: () -> Unit) {
        viewModelScope.launch {
            SessionManager.logout(context)
            _riderId.value = -1
            _authError.value = null
            try {
                _isLoading.value = true
                val res = RetrofitClient.apiService.login(RiderLoginRequest(phone, pass))
                android.util.Log.d("API_RESPONSE", "Response: $res")
                if (res.isSuccessful) {
                    val body = res.body()
                    android.util.Log.d("API_RESPONSE", "Body: $body")
                    if (body?.status == "success" && body.data != null) {
                        SessionManager.saveUser(context, body.data)
                        // Trigger initialization to load the session state in ViewModel
                        initSession(context)
                        onSuccess()
                    } else {
                        _authError.value = body?.message ?: "Invalid Credentials"
                    }
                } else {
                    _authError.value = "Server error. Try again."
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                _authError.value = "Network Error. Please check connection."
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun register(name: String, phone: String, pass: String, zone: String, context: Context) {
        viewModelScope.launch {
            _authError.value = null
            _pendingApproval.value = false
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.register(RiderRegisterRequest(name, phone, pass, zone))
                if (response.isSuccessful) {
                    val body = response.body()
                    if (body?.status == "success" && body.data != null) {
                        _pendingApproval.value = true
                        _authError.value = "Registration Successful. Awaiting Admin Approval."
                    } else {
                        _authError.value = body?.message ?: "Registration Failed."
                    }
                } else {
                    _authError.value = "Server error. Try again."
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                _authError.value = "Network Error. Please check connection."
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun fetchAvailableOrders(context: Context) {
        val zone = _riderZone.value
        val riderId = _riderId.value
        if (zone.isEmpty() || riderId == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.getAvailableOrders(zone, riderId)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val newOrders = response.body()?.data ?: emptyList()
                    _availableOrders.value = newOrders
                    calculateDistances(context, newOrders)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch orders", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    private fun calculateDistances(context: Context, orders: List<RiderOrder>) {
        if (orders.isEmpty()) return
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return
        
        val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
        fusedLocationClient.lastLocation.addOnSuccessListener { location ->
            if (location != null) {
                viewModelScope.launch(Dispatchers.IO) {
                    val geocoder = Geocoder(context, Locale.getDefault())
                    val updatedOrders = orders.map { order ->
                        val address = order.pickupAddress
                        if (!address.isNullOrEmpty()) {
                            try {
                                val results = geocoder.getFromLocationName(address, 1)
                                if (!results.isNullOrEmpty()) {
                                    val loc = results[0]
                                    val resultsArray = FloatArray(1)
                                    Location.distanceBetween(
                                        location.latitude, location.longitude,
                                        loc.latitude, loc.longitude,
                                        resultsArray
                                    )
                                    order.copy(distanceInMeters = resultsArray[0])
                                } else order
                            } catch (e: Exception) { order }
                        } else order
                    }
                    withContext(Dispatchers.Main) {
                        _availableOrders.value = updatedOrders
                    }
                }
            }
        }
    }

    fun fetchMyOrders(context: Context) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.getRiderOrders(id)
                if (response.isSuccessful && response.body()?.status == "success") {
                    _myOrders.value = response.body()?.data ?: emptyList()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch history", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun acceptOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.acceptOrder(AcceptOrderRequest(orderId, id.toString()))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Accepted!", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to accept order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Order acceptance queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.AcceptOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun rejectOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val request = mapOf("order_id" to orderId.toString(), "rider_id" to id.toString())
                val response = RetrofitClient.apiService.rejectOrder(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Rejected", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to reject order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Order rejection queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.RejectOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun updateOrderStatus(orderId: String, newStatus: String, context: Context) {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.updateOrderStatus(UpdateOrderStatusRequest(orderId, newStatus))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Status updated to $newStatus", Toast.LENGTH_SHORT).show()
                    fetchMyOrders(context) // Refresh
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update status", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Status update queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.UpdateOrderStatus(orderId, newStatus)
                if (!pendingActions.contains(action)) pendingActions.add(action)
            } finally {
                _isLoading.value = false
            }
        }
    }
}
"""

content = content[:start] + new_vm + "\n" + content[end:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
