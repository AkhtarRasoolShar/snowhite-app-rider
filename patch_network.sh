#!/bin/bash
cat << 'INNER_EOF' >> /app/applet/app/src/main/java/com/example/network/ApiService.kt

@JsonClass(generateAdapter = true)
data class RiderLoginRequest(
    val phone: String? = null,
    val password: String? = null
)

@JsonClass(generateAdapter = true)
data class RiderLoginResponse(
    val rider_id: String? = null,
    val name: String? = null,
    val token: String? = null
)

@JsonClass(generateAdapter = true)
data class RiderTask(
    val order_id: String? = null,
    val customer_name: String? = null,
    val customer_phone: String? = null,
    val pickup_address: String? = null,
    val status: String? = null,
    val total_amount: Int? = 0,
    val lat: Double? = null,
    val lng: Double? = null,
    @Json(name = "items") val items: List<OrderItemResponse>? = null
)

@JsonClass(generateAdapter = true)
data class IntakeScanRequest(
    val order_id: String? = null
)
INNER_EOF

# Now edit the interface ApiService
sed -i 's/interface ApiService {/interface ApiService {\n    @POST("routes.php?action=rider_login")\n    suspend fun riderLogin(@Body request: RiderLoginRequest): Response<ApiResponseWrapper<RiderLoginResponse>>\n\n    @GET("routes.php?action=rider_tasks")\n    suspend fun getRiderTasks(@Query("rider_id") riderId: String): Response<ApiResponseWrapper<List<RiderTask>>>\n\n    @POST("routes.php?action=intake_scan")\n    suspend fun intakeScan(@Body request: IntakeScanRequest): Response<Unit>\n\n    @GET("routes.php?action=update_order_status")\n    suspend fun updateOrderStatus(@Query("order_id") orderId: String, @Query("status") status: String): Response<Unit>\n/' /app/applet/app/src/main/java/com/example/network/ApiService.kt
