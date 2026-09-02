import re
with open("/app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt", "r") as f:
    content = f.read()

# Fix login
login_old = """            result.onSuccess { data ->
                repository.saveSession(data.customer_id ?: 1, data.name ?: "Customer", data.phone ?: phone)
                _isLoggedIn.value = true
                _customerName.value = data.name ?: "Customer"
                _customerPhone.value = data.phone ?: phone
                onSuccess()
            }.onFailure {
                // Demo fallback
                repository.saveSession(1, "Demo User", phone)
                _isLoggedIn.value = true
                _customerName.value = "Demo User"
                _customerPhone.value = phone
                onSuccess()
            }"""

login_new = """            result.onSuccess { data ->
                repository.saveSession(data.customer_id ?: 1, data.name ?: "Customer", data.phone ?: phone)
                _isLoggedIn.value = true
                _customerName.value = data.name ?: "Customer"
                _customerPhone.value = data.phone ?: phone
                onSuccess()
            }.onFailure {
                onError(it.message ?: "Login failed")
            }"""
content = content.replace(login_old, login_new)

# Fix register
register_old = """            result.onSuccess { data ->
                repository.saveSession(data.customer_id ?: 1, data.name ?: name, data.phone ?: phone)
                _isLoggedIn.value = true
                _customerName.value = data.name ?: name
                _customerPhone.value = data.phone ?: phone
                onSuccess()
            }.onFailure {
                // Demo fallback
                repository.saveSession(1, name, phone)
                _isLoggedIn.value = true
                _customerName.value = name
                _customerPhone.value = phone
                onSuccess()
            }"""

register_new = """            result.onSuccess { data ->
                repository.saveSession(data.customer_id ?: 1, data.name ?: name, data.phone ?: phone)
                _isLoggedIn.value = true
                _customerName.value = data.name ?: name
                _customerPhone.value = data.phone ?: phone
                onSuccess()
            }.onFailure {
                onError(it.message ?: "Registration failed")
            }"""
content = content.replace(register_old, register_new)

# Fix fetchOrders
fetch_old = """                result.onSuccess { orders ->
                    _orderHistory.value = orders
                }.onFailure {
                    // Demo fallback
                    _orderHistory.value = listOf(
                        OrderResponse(order_id = "ORD-001", date = "2026-08-31", status = "Washing", total_amount = 1200)
                    )
                }"""

fetch_new = """                result.onSuccess { orders ->
                    _orderHistory.value = orders
                }.onFailure {
                    _errorMessage.value = "Failed to load orders"
                    _orderHistory.value = emptyList()
                }"""
content = content.replace(fetch_old, fetch_new)

# Fix scheduleLaundryPickup
schedule_old = """            val result = repository.createOrder(req)
            
            // Clear cart and show success (demo continuity)
            clearCart()
            _orderSuccess.value = true
            _isLoading.value = false"""

schedule_new = """            val result = repository.createOrder(req)
            result.onSuccess {
                clearCart()
                _orderSuccess.value = true
            }.onFailure {
                _errorMessage.value = it.message ?: "Failed to place order"
            }
            _isLoading.value = false"""
content = content.replace(schedule_old, schedule_new)

with open("/app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt", "w") as f:
    f.write(content)
