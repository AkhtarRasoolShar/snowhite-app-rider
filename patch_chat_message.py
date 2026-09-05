import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """data class ChatMessage(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("order_id") val orderId: Int? = null,
    @SerializedName("sender_type") val senderType: String? = null,
    @SerializedName("sender_id") val senderId: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("status") var status: String? = null // e.g., sent, delivered, seen
)"""

replacement = """data class ChatMessage(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("order_id") val orderId: Int? = null,
    @SerializedName("sender_type") val senderType: String? = null,
    @SerializedName("sender_id") val senderId: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("status") var status: String? = null, // e.g., sent, delivered, seen
    @SerializedName("is_read") val isRead: String? = "0"
)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
