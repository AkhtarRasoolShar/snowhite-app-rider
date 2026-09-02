#!/bin/bash
cat << 'INNER_EOF' > /app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt
package com.example.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.model.CartItem
import com.example.model.Garment
import com.example.model.GarmentCategory
import com.example.model.LaundryServiceType
import com.example.network.LaundryItemRequest
import com.example.network.LaundryOrderRequest
import com.example.network.OrderResponse
import com.example.network.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class SnowWhiteViewModel : ViewModel() {

    private val _garments = MutableStateFlow<List<Garment>>(emptyList())
    val garments: StateFlow<List<Garment>> = _garments.asStateFlow()

    private val _cartItems = MutableStateFlow<List<CartItem>>(emptyList())
    val cartItems: StateFlow<List<CartItem>> = _cartItems.asStateFlow()

    private val _activeServiceType = MutableStateFlow(LaundryServiceType.WASH_IRON)
    val activeServiceType: StateFlow<LaundryServiceType> = _activeServiceType.asStateFlow()

    private val _orders = MutableStateFlow<List<OrderResponse>>(emptyList())
    val orders: StateFlow<List<OrderResponse>> = _orders.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()
    
    private val _orderSuccess = MutableStateFlow(false)
    val orderSuccess: StateFlow<Boolean> = _orderSuccess.asStateFlow()

    init {
        loadGarments()
    }

    private fun loadGarments() {
        _garments.value = listOf(
            Garment("m1", GarmentCategory.MEN, "Cotton Shirt", "Crisp fold & hanger", 80),
            Garment("m2", GarmentCategory.MEN, "Trousers/Pants", "Crease-free finish", 100),
            Garment("m3", GarmentCategory.MEN, "2-Piece Suit", "Premium dry cleaning", 350),
            Garment("m4", GarmentCategory.MEN, "Kurta", "Gentle wash & fold", 120),
            Garment("w1", GarmentCategory.WOMEN, "Kurti", "Stain removal & care", 100),
            Garment("w2", GarmentCategory.WOMEN, "3-Piece Lawn Suit", "Delicate fabric handling", 250),
            Garment("w3", GarmentCategory.WOMEN, "Formal Gown", "Specialized treatment", 500),
            Garment("h1", GarmentCategory.HOUSEHOLD, "Bed Sheet Set", "Fresh scent & folded", 200),
            Garment("h2", GarmentCategory.HOUSEHOLD, "Heavy Blanket / Quilt", "Deep clean & sanitize", 450),
            Garment("h3", GarmentCategory.HOUSEHOLD, "Curtains", "Dust removal & press", 300)
        )
    }

    fun setActiveServiceType(type: LaundryServiceType) {
        _activeServiceType.value = type
    }

    fun getQuantityFor(garment: Garment, serviceType: LaundryServiceType): Int {
        return _cartItems.value.find { it.garment.id == garment.id && it.serviceType == serviceType }?.quantity ?: 0
    }

    fun updateCartQuantity(garment: Garment, serviceType: LaundryServiceType, newQuantity: Int) {
        if (newQuantity < 0) return
        _cartItems.update { currentCart ->
            val existingItem = currentCart.find { it.garment.id == garment.id && it.serviceType == serviceType }
            if (existingItem != null) {
                if (newQuantity == 0) {
                    currentCart.filterNot { it.garment.id == garment.id && it.serviceType == serviceType }
                } else {
                    currentCart.map {
                        if (it.garment.id == garment.id && it.serviceType == serviceType) {
                            it.copy(quantity = newQuantity)
                        } else {
                            it
                        }
                    }
                }
            } else {
                if (newQuantity > 0) {
                    currentCart + CartItem(garment, serviceType, newQuantity)
                } else {
                    currentCart
                }
            }
        }
    }

    fun getEstimatedTotal(): Int {
        return _cartItems.value.sumOf { (it.garment.basePrice * it.serviceType.priceMultiplier * it.quantity).toInt() }
    }

    fun getTotalItems(): Int {
        return _cartItems.value.sumOf { it.quantity }
    }

    fun scheduleLaundryPickup(
        pickupSlot: String,
        address: String,
        detergentPref: String,
        starchLevel: String,
        specialNotes: String
    ) {
        val request = LaundryOrderRequest(
            items = _cartItems.value.map { LaundryItemRequest(it.garment.id, it.quantity, it.serviceType.name) },
            pickup_slot = pickupSlot,
            pickup_address = address,
            detergent_pref = detergentPref,
            starch_level = starchLevel,
            special_notes = specialNotes,
            estimated_total = getEstimatedTotal()
        )
        
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null
            _orderSuccess.value = false
            try {
                val response = RetrofitClient.apiService.createLaundryOrder(request)
                if (response.isSuccessful) {
                    _cartItems.value = emptyList() // clear cart
                    _orderSuccess.value = true
                } else {
                    _errorMessage.value = "Failed to create order: ${response.code()}"
                }
            } catch (e: Exception) {
                _errorMessage.value = "Network error: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun fetchOrders() {
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null
            try {
                val response = RetrofitClient.apiService.getCustomerOrders(customerId = 1)
                if (response.status == "success") {
                    _orders.value = response.data
                } else {
                    _errorMessage.value = "Failed to fetch orders: ${response.status}"
                }
            } catch (e: Exception) {
                _errorMessage.value = "Network error: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun clearError() {
        _errorMessage.value = null
    }
    
    fun clearSuccess() {
        _orderSuccess.value = false
    }
}
INNER_EOF
