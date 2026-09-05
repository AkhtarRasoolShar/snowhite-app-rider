import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add customer_name and customer_phone to RiderOrder
old_order = """data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = null,
    @SerializedName("zone") val zone: String? = null,
    var distanceInMeters: Float? = null
)"""
new_order = """data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = null,
    @SerializedName("zone") val zone: String? = null,
    @SerializedName("customer_name") val customer_name: String? = null,
    @SerializedName("customer_phone") val customer_phone: String? = null,
    var distanceInMeters: Float? = null
)"""
content = content.replace(old_order, new_order)

# Add status to ChatMessage
old_chat = """data class ChatMessage(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("sender_type") val sender_type: String? = null,
    @SerializedName("sender_id") val sender_id: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val created_at: String? = null
)"""
new_chat = """data class ChatMessage(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("sender_type") val sender_type: String? = null,
    @SerializedName("sender_id") val sender_id: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val created_at: String? = null,
    @SerializedName("status") val status: String? = null // e.g., sent, delivered, seen
)"""
content = content.replace(old_chat, new_chat)

# Add typing status response
typing_models = """
data class TypingStatus(
    @SerializedName("is_typing") val is_typing: Boolean
)
"""
if "data class TypingStatus" not in content:
    content = content.replace("data class ChatMessage(", typing_models + "\ndata class ChatMessage(")

# Add typing endpoints
api_endpoints = """
    @GET("routes.php?action=get_typing_status")
    suspend fun getTypingStatus(@Query("order_id") orderId: Int, @Query("sender_type") senderType: String): retrofit2.Response<GenericResponse<TypingStatus>>

    @POST("routes.php?action=update_typing_status")
    suspend fun updateTypingStatus(@Body request: Map<String, String>): retrofit2.Response<GenericResponse<Unit>>
"""
if "getTypingStatus" not in content:
    content = content.replace("suspend fun sendChatMessage", api_endpoints + "\n    suspend fun sendChatMessage")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
