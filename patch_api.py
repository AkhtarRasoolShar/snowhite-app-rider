with open("/app/applet/app/src/main/java/com/example/network/ApiService.kt", "w") as f:
    f.write("""package com.example.network

import com.google.gson.annotations.SerializedName
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

data class ApiResponseWrapper<T>(
    val status: String? = null,
    val data: T? = null
)

data class LoginRequest(
    val phone: String? = null,
    val password: String? = null
)

data class RegisterRequest(
    val name: String? = null,
    val phone: String? = null,
    val password: String? = null
)

data class AuthResponse(
    val customer_id: Int? = null,
    val name: String? = null,
    val phone: String? = null
)

data class LaundryOrderRequest(
    val customer_id: Int? = null,
    val customer_name: String? = null,
    val customer_phone: String? = null,
    val items: List<LaundryItemRequest>? = null,
    val pickup_slot: String? = null,
    val pickup_address: String? = null,
    val detergent_pref: String? = null,
    val starch_level: String? = null,
    val special_notes: String? = null,
    val estimated_total: Int? = null
)

data class LaundryItemRequest(
    val garment_id: String? = null,
    val quantity: Int? = null,
    val service_type: String? = null
)

data class OrderItemResponse(
    val item: String? = null,
    val qty: Int? = null,
    val price: Int? = null
)

data class OrderResponse(
    val order_id: String? = null,
    @SerializedName("created_at") val date: String? = null,
    val total_amount: Int? = null,
    val status: String? = null,
    val pickup_slot: String? = null,
    val items: List<OrderItemResponse>? = null
)

interface ApiService {
    @POST("routes.php?action=login")
    suspend fun login(@Body request: LoginRequest): Response<ApiResponseWrapper<AuthResponse>>

    @POST("routes.php?action=register")
    suspend fun register(@Body request: RegisterRequest): Response<ApiResponseWrapper<AuthResponse>>

    @POST("routes.php?action=create_laundry_order")
    suspend fun createLaundryOrder(@Body request: LaundryOrderRequest): Response<Unit>

    @GET("routes.php?action=get_customer_orders")
    suspend fun getCustomerOrders(@Query("customer_id") customerId: Int?): ApiResponseWrapper<List<OrderResponse>>
}
""")
