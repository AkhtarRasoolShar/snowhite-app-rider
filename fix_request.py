with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_class = """data class SendMessageRequest(
    @SerializedName("order_id") val order_id: Int,
    @SerializedName("sender_type") val sender_type: String,
    @SerializedName("sender_id") val sender_id: Int,
    @SerializedName("message") val message: String
)"""

new_class = """data class SendMessageRequest(
    @SerializedName("order_id") val orderId: Int,
    @SerializedName("sender_type") val senderType: String,
    @SerializedName("sender_id") val senderId: Int,
    @SerializedName("message") val message: String
)"""

content = content.replace(old_class, new_class)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
