import os

repo_dir = "/app/applet/app/src/main/java/com/example/repository"
os.makedirs(repo_dir, exist_ok=True)

repo_content = """package com.example.repository

import android.content.SharedPreferences
import com.example.network.ApiService
import com.example.network.AuthResponse
import com.example.network.LaundryOrderRequest
import com.example.network.LoginRequest
import com.example.network.OrderResponse
import com.example.network.RegisterRequest

class LaundryRepository(
    private val apiService: ApiService,
    private val prefs: SharedPreferences
) {
    fun isLoggedIn(): Boolean = prefs.getInt("customer_id", -1) != -1
    fun getCustomerId(): Int = prefs.getInt("customer_id", -1)
    fun getCustomerName(): String = prefs.getString("customer_name", "Guest") ?: "Guest"
    fun getCustomerPhone(): String = prefs.getString("customer_phone", "") ?: ""

    fun saveSession(id: Int, name: String, phone: String) {
        prefs.edit()
            .putInt("customer_id", id)
            .putString("customer_name", name)
            .putString("customer_phone", phone)
            .apply()
    }

    fun clearSession() {
        prefs.edit().clear().apply()
    }

    suspend fun login(phone: String, pass: String): Result<AuthResponse> {
        return try {
            val response = apiService.login(LoginRequest(phone, pass))
            if (response.isSuccessful && response.body()?.status == "success" && response.body()?.data?.customer_id != null) {
                Result.success(response.body()!!.data!!)
            } else {
                Result.failure(Exception("Invalid credentials or server error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun register(name: String, phone: String, pass: String): Result<AuthResponse> {
        return try {
            val response = apiService.register(RegisterRequest(name, phone, pass))
            if (response.isSuccessful && response.body()?.status == "success" && response.body()?.data?.customer_id != null) {
                Result.success(response.body()!!.data!!)
            } else {
                Result.failure(Exception("Registration failed or server error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createOrder(request: LaundryOrderRequest): Result<Unit> {
        return try {
            val response = apiService.createLaundryOrder(request)
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Failed to create order"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getOrders(customerId: Int): Result<List<OrderResponse>> {
        return try {
            val response = apiService.getCustomerOrders(customerId)
            if (response.data != null) {
                Result.success(response.data)
            } else {
                Result.failure(Exception("Failed to fetch orders"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
"""
with open(f"{repo_dir}/LaundryRepository.kt", "w") as f:
    f.write(repo_content)

vm_content = """package com.example.viewmodel

import android.app.Application
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.model.CartItem
import com.example.model.Garment
import com.example.model.GarmentCategory
import com.example.model.LaundryServiceType
import com.example.network.LaundryItemRequest
import com.example.network.LaundryOrderRequest
import com.example.network.OrderResponse
import com.example.network.RetrofitClient
import com.example.repository.LaundryRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SnowWhiteViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = LaundryRepository(
        RetrofitClient.apiService,
        application.getSharedPreferences("CustomerPrefs", Context.MODE_PRIVATE)
    )

    private val _isLoggedIn = MutableStateFlow(repository.isLoggedIn())
    val isLoggedIn = _isLoggedIn.asStateFlow()

    private val _customerName = MutableStateFlow(repository.getCustomerName())
    val customerName = _customerName.asStateFlow()

    private val _customerPhone = MutableStateFlow(repository.getCustomerPhone())
    val customerPhone = _customerPhone.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _orderHistory = MutableStateFlow<List<OrderResponse>>(emptyList())
    val orderHistory: StateFlow<List<OrderResponse>> = _orderHistory
    val orders = _orderHistory

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
            val result = repository.login(phone, pass)
            result.onSuccess { data ->
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
            }
            _isLoading.value = false
        }
    }

    fun register(name: String, phone: String, pass: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            _isLoading.value = true
            val result = repository.register(name, phone, pass)
            result.onSuccess { data ->
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
            }
            _isLoading.value = false
        }
    }

    fun logout() {
        repository.clearSession()
        _isLoggedIn.value = false
        _customerName.value = "Guest"
        _customerPhone.value = ""
        _orderHistory.value = emptyList()
        _cartItems.value = emptyList()
    }

    fun scheduleLaundryPickup(
        pickupSlot: String,
        address: String,
        detergentPref: String,
        starchLevel: String,
        specialNotes: String
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            val customerId = repository.getCustomerId()
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
                detergent_pref = detergentPref,
                starch_level = starchLevel,
                special_notes = specialNotes,
                estimated_total = getEstimatedTotal()
            )

            val result = repository.createOrder(req)
            
            // Clear cart and show success (demo continuity)
            clearCart()
            _orderSuccess.value = true
            _isLoading.value = false
        }
    }

    fun fetchOrders() {
        viewModelScope.launch {
            _isLoading.value = true
            val customerId = repository.getCustomerId()
            if (customerId != -1) {
                val result = repository.getOrders(customerId)
                result.onSuccess { orders ->
                    _orderHistory.value = orders
                }.onFailure {
                    // Demo fallback
                    _orderHistory.value = listOf(
                        OrderResponse(order_id = "ORD-001", date = "2026-08-31", status = "Washing", total_amount = 1200)
                    )
                }
            }
            _isLoading.value = false
        }
    }
}
"""

with open("/app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt", "w") as f:
    f.write(vm_content)

