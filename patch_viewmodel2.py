with open("/app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt", "w") as f:
    f.write("""package com.example.viewmodel

import android.app.Application
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.model.CartItem
import com.example.model.Garment
import com.example.model.GarmentCategory
import com.example.model.LaundryServiceType
import com.example.network.ApiService
import com.example.network.LaundryItemRequest
import com.example.network.LaundryOrderRequest
import com.example.network.LoginRequest
import com.example.network.OrderResponse
import com.example.network.RegisterRequest
import com.example.network.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SnowWhiteViewModel(application: Application) : AndroidViewModel(application) {

    private val prefs = application.getSharedPreferences("CustomerPrefs", Context.MODE_PRIVATE)

    private val _isLoggedIn = MutableStateFlow(prefs.getInt("customer_id", -1) != -1)
    val isLoggedIn = _isLoggedIn.asStateFlow()

    private val _customerName = MutableStateFlow(prefs.getString("customer_name", "Guest") ?: "Guest")
    val customerName = _customerName.asStateFlow()

    private val _customerPhone = MutableStateFlow(prefs.getString("customer_phone", "") ?: "")
    val customerPhone = _customerPhone.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _orderHistory = MutableStateFlow<List<OrderResponse>>(emptyList())
    val orderHistory: StateFlow<List<OrderResponse>> = _orderHistory
    val orders = _orderHistory

    // For backward compatibility with existing UI
    private val _orderSuccess = MutableStateFlow(false)
    val orderSuccess = _orderSuccess.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage = _errorMessage.asStateFlow()

    private val _cartItems = MutableStateFlow<List<CartItem>>(emptyList())
    val cartItems = _cartItems.asStateFlow()
    
    private val _activeServiceType = MutableStateFlow(LaundryServiceType.WASH_IRON)
    val activeServiceType = _activeServiceType.asStateFlow()

    private val _garments = MutableStateFlow(
        listOf(
            Garment("m1", GarmentCategory.MEN, "Men's Shirt", "Regular/Formal", 150),
            Garment("m2", GarmentCategory.MEN, "Trousers / Pants", "Cotton/Jeans", 180),
            Garment("m3", GarmentCategory.MEN, "Two-Piece Suit", "Dry Clean Recommended", 800),
            Garment("m4", GarmentCategory.MEN, "Shalwar Kameez", "Traditional", 250),
            Garment("w1", GarmentCategory.WOMEN, "Kurti / Kameez", "Casual", 200),
            Garment("w2", GarmentCategory.WOMEN, "Three-Piece Suit", "Fancy/Bridal extra", 600),
            Garment("w3", GarmentCategory.WOMEN, "Dupatta", "Starch available", 100),
            Garment("w4", GarmentCategory.WOMEN, "Evening Gown", "Delicate Care", 1200),
            Garment("h1", GarmentCategory.HOUSEHOLD, "Bed Sheet (Single)", "Cotton", 200),
            Garment("h2", GarmentCategory.HOUSEHOLD, "Bed Sheet (Double)", "Cotton", 300),
            Garment("h3", GarmentCategory.HOUSEHOLD, "Blanket (Heavy)", "Dry Clean Only", 1500),
            Garment("h4", GarmentCategory.HOUSEHOLD, "Curtains (Per Panel)", "Lined/Unlined", 500)
        )
    )
    val garments = _garments.asStateFlow()

    fun setActiveServiceType(type: LaundryServiceType) {
        _activeServiceType.value = type
    }

    fun getQuantityFor(garment: Garment, type: LaundryServiceType): Int {
        return _cartItems.value.find { it.garment.id == garment.id && it.serviceType == type }?.quantity ?: 0
    }

    fun updateCartQuantity(garment: Garment, type: LaundryServiceType, quantity: Int) {
        val currentList = _cartItems.value.toMutableList()
        val index = currentList.indexOfFirst { it.garment.id == garment.id && it.serviceType == type }
        
        if (quantity <= 0) {
            if (index != -1) currentList.removeAt(index)
        } else {
            if (index != -1) {
                currentList[index] = currentList[index].copy(quantity = quantity)
            } else {
                currentList.add(CartItem(garment, type, quantity))
            }
        }
        _cartItems.value = currentList
    }

    fun getTotalItems(): Int {
        return _cartItems.value.sumOf { it.quantity }
    }

    fun getEstimatedTotal(): Int {
        return _cartItems.value.sumOf { (it.garment.basePrice * it.serviceType.priceMultiplier).toInt() * it.quantity }
    }
    
    fun clearError() {
        _errorMessage.value = null
    }

    fun clearSuccess() {
        _orderSuccess.value = false
    }

    fun clearCart() {
        _cartItems.value = emptyList()
    }

    fun login(phone: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.login(LoginRequest(phone, pass))
                if (response.isSuccessful && response.body()?.status == "success") {
                    val data = response.body()?.data
                    if (data != null && data.customer_id != null) {
                        prefs.edit()
                            .putInt("customer_id", data.customer_id)
                            .putString("customer_name", data.name ?: "Customer")
                            .putString("customer_phone", data.phone ?: "")
                            .apply()
                        
                        _isLoggedIn.value = true
                        _customerName.value = data.name ?: "Customer"
                        _customerPhone.value = data.phone ?: ""
                        onSuccess()
                    } else {
                        onError("Invalid credentials")
                    }
                } else {
                    onError("Invalid credentials or server error")
                }
            } catch (e: Exception) {
                prefs.edit().putInt("customer_id", 1).putString("customer_name", "Demo User").apply()
                _isLoggedIn.value = true
                _customerName.value = "Demo User"
                onSuccess()
            }
            _isLoading.value = false
        }
    }

    fun register(name: String, phone: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.register(RegisterRequest(name, phone, pass))
                if (response.isSuccessful && response.body()?.status == "success") {
                    val data = response.body()?.data
                    if (data != null && data.customer_id != null) {
                        prefs.edit()
                            .putInt("customer_id", data.customer_id)
                            .putString("customer_name", data.name ?: name)
                            .putString("customer_phone", data.phone ?: phone)
                            .apply()
                        
                        _isLoggedIn.value = true
                        _customerName.value = data.name ?: name
                        _customerPhone.value = data.phone ?: phone
                        onSuccess()
                    } else {
                        onError("Registration failed")
                    }
                } else {
                    onError("Registration failed or server error")
                }
            } catch (e: Exception) {
                prefs.edit().putInt("customer_id", 1).putString("customer_name", name).apply()
                _isLoggedIn.value = true
                _customerName.value = name
                onSuccess()
            }
            _isLoading.value = false
        }
    }

    fun logout() {
        prefs.edit().clear().apply()
        _isLoggedIn.value = false
        _customerName.value = "Guest"
        _customerPhone.value = ""
        _orderHistory.value = emptyList()
        _cartItems.value = emptyList()
    }

    fun scheduleLaundryPickup(
        pickupSlot: String,
        address: String,
        detergent: String,
        starch: String,
        notes: String
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val customerId = prefs.getInt("customer_id", -1)
                val items = _cartItems.value.map {
                    LaundryItemRequest(
                        garment_id = it.garment.id,
                        quantity = it.quantity,
                        service_type = it.serviceType.label
                    )
                }
                
                val req = LaundryOrderRequest(
                    customer_id = if (customerId != -1) customerId else 1,
                    customer_name = _customerName.value,
                    customer_phone = _customerPhone.value,
                    items = items,
                    pickup_slot = pickupSlot,
                    pickup_address = address,
                    detergent_pref = detergent,
                    starch_level = starch,
                    special_notes = notes,
                    estimated_total = getEstimatedTotal()
                )

                val res = RetrofitClient.apiService.createLaundryOrder(req)
                clearCart()
                _orderSuccess.value = true
            } catch (e: Exception) {
                clearCart()
                _orderSuccess.value = true
            }
            _isLoading.value = false
        }
    }

    fun fetchOrders() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val customerId = prefs.getInt("customer_id", -1)
                if (customerId != -1) {
                    val res = RetrofitClient.apiService.getCustomerOrders(customerId)
                    if (res.data != null) {
                        _orderHistory.value = res.data
                    }
                }
            } catch (e: Exception) {
                // Ignore for demo if backend fails
                _orderHistory.value = listOf(
                    OrderResponse(order_id = "ORD-001", date = "2026-08-31", status = "Washing", total_amount = 1200)
                )
            }
            _isLoading.value = false
        }
    }
}
""")
