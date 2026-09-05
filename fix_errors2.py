import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

# Fix repeated annotation
main = main.replace('@SerializedName("is_typing") @SerializedName("is_typing")', '@SerializedName("is_typing")')

# Fix fetchOrders and getRiderOrders and getAvailableOrders
main = main.replace('fun fetchOrders(riderId: Int)', 'fun fetchOrders(riderId: String)')
main = main.replace('fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: Int)', 'fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: String)')
main = main.replace('fun getRiderOrders(@Query("rider_id") riderId: Int)', 'fun getRiderOrders(@Query("rider_id") riderId: String)')
main = main.replace('fun getChatMessages(@Query("order_id") orderId: Int)', 'fun getChatMessages(@Query("order_id") orderId: String)')

# Fix rejectOrder Retrofit map
main = main.replace('fun rejectOrder(@Body request: Map<String, Int>)', 'fun rejectOrder(@Body request: Map<String, String>)')
main = main.replace('val request = mapOf("order_id" to orderId, "rider_id" to id)', 'val request = mapOf("order_id" to orderId.toString(), "rider_id" to id.toString())')

# Fix RejectOrder Action
main = main.replace('data class RejectOrder(val orderId: Int)', 'data class RejectOrder(val orderId: String)')
main = main.replace('rejectOrder(selectedOrderForReview!!.orderId?.toIntOrNull() ?: 0, context)', 'rejectOrder(selectedOrderForReview!!.orderId ?: "", context)')

# authData.id is String?, so we can pass it to fetchOrders if we do authData.id ?: ""
main = main.replace('fetchOrders(authData.id)', 'fetchOrders(authData.id ?: "")')
main = main.replace('val id: Int = sharedPreferences.getInt', 'val id = sharedPreferences.getString("rider_id", "") ?: ""')
main = main.replace('getInt("rider_id", 0)', 'getString("rider_id", "")')

# AcceptOrderRequest rider_id needs to be String
main = main.replace('val rider_id: Int', 'val rider_id: String')
main = main.replace('AcceptOrderRequest(orderId, id)', 'AcceptOrderRequest(orderId, id.toString())')

# authData saving
main = main.replace('putInt("rider_id", it.id)', 'putString("rider_id", it.id.toString())')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)


with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chat = f.read()

# Fix ChatUI.kt
chat = chat.replace('fun OrderChatScreen(orderId: Int, riderId: Int)', 'fun OrderChatScreen(orderId: Int, riderId: String)')
chat = chat.replace('viewModel.getChatMessages(orderId)', 'viewModel.getChatMessages(orderId.toString())')
chat = chat.replace('viewModel.getTypingStatus(orderId,', 'viewModel.getTypingStatus(orderId.toString(),')
chat = chat.replace('ChatSendRequest(order_id = orderId, sender_type = "rider", sender_id = riderId, message = msg)', 'ChatSendRequest(order_id = orderId.toString(), sender_type = "rider", sender_id = riderId, message = msg)')
chat = chat.replace('ChatSendRequest(orderId, "rider", riderId, messageText)', 'ChatSendRequest(orderId.toString(), "rider", riderId, messageText)')
chat = chat.replace('it.sender_id == riderId', 'it.sender_id == riderId.toString()')

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chat)

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    m = f.read()
m = m.replace('data class ChatSendRequest(\n    val order_id: Int,\n    val sender_type: String,\n    val sender_id: Int,', 'data class ChatSendRequest(\n    val order_id: String,\n    val sender_type: String,\n    val sender_id: String,')
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(m)

