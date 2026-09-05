with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

old_send = """data class ChatSendRequest(
    val order_id: Int,
    val sender_type: String,
    val sender_id: Int,
    val message: String
)"""

new_send = """data class ChatSendRequest(
    @SerializedName("order_id") val order_id: Int,
    @SerializedName("sender_type") val sender_type: String,
    @SerializedName("sender_id") val sender_id: Int,
    @SerializedName("message") val message: String
)"""

main = main.replace(old_send, new_send)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)

