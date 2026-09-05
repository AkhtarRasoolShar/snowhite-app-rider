import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# fetchAvailableOrders
fetch_available = """    fun fetchAvailableOrders(context: Context) {
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
    }"""
content = re.sub(r'    fun fetchAvailableOrders\(context: Context\) \{[\s\S]*?    \}', fetch_available, content, count=1, flags=re.MULTILINE)

# fetchMyOrders
fetch_my = """    fun fetchMyOrders(context: Context) {
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
    }"""
content = re.sub(r'    fun fetchMyOrders\(context: Context\) \{[\s\S]*?    \}', fetch_my, content, count=1, flags=re.MULTILINE)

# acceptOrder
accept_order = """    fun acceptOrder(orderId: String, context: Context) {
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
    }"""
content = re.sub(r'    fun acceptOrder\(orderId: String, context: Context\) \{[\s\S]*?    \}', accept_order, content, count=1, flags=re.MULTILINE)

# rejectOrder
reject_order = """    fun rejectOrder(orderId: String, context: Context) {
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
    }"""
content = re.sub(r'    fun rejectOrder\(orderId: String, context: Context\) \{[\s\S]*?    \}', reject_order, content, count=1, flags=re.MULTILINE)

# updateOrderStatus
update_order_status = """    fun updateOrderStatus(orderId: String, newStatus: String, context: Context) {
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
    }"""
content = re.sub(r'    fun updateOrderStatus\(orderId: String, newStatus: String, context: Context\) \{[\s\S]*?    \}', update_order_status, content, count=1, flags=re.MULTILINE)

# updateWhatsApp
update_whatsapp = """    fun updateWhatsApp(context: Context, whatsapp: String) {
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
    }"""
content = re.sub(r'    fun updateWhatsApp\(context: Context, whatsapp: String\) \{[\s\S]*?    \}', update_whatsapp, content, count=1, flags=re.MULTILINE)

# login
login = """    fun login(phone: String, pass: String, context: Context, onSuccess: () -> Unit) {
        viewModelScope.launch {
            SessionManager.logout(context)
            _riderId.value = -1
            _authError.value = null
            try {
                _isLoading.value = true
                val res = RetrofitClient.apiService.login(RiderLoginRequest(phone, pass))
                Log.d("API_RESPONSE", "Response: $res")
                if (res.isSuccessful) {
                    val body = res.body()
                    Log.d("API_RESPONSE", "Body: $body")
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
    }"""
content = re.sub(r'    fun login\(phone: String, pass: String, context: Context, onSuccess: \(\) -> Unit\) \{[\s\S]*?    \}', login, content, count=1, flags=re.MULTILINE)

# register
register = """    fun register(name: String, phone: String, pass: String, zone: String, context: Context) {
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
    }"""
content = re.sub(r'    fun register\(name: String, phone: String, pass: String, zone: String, context: Context\) \{[\s\S]*?    \}', register, content, count=1, flags=re.MULTILINE)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
