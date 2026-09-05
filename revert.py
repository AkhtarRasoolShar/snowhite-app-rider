import re

with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chat = f.read()

chat = chat.replace('fun OrderChatScreen(orderId: Int, riderId: String)', 'fun OrderChatScreen(orderId: Int, riderId: Int)')
chat = chat.replace('viewModel.getChatMessages(orderId.toString())', 'viewModel.getChatMessages(orderId)')
chat = chat.replace('viewModel.getTypingStatus(orderId.toString(),', 'viewModel.getTypingStatus(orderId,')
chat = chat.replace('ChatSendRequest(order_id = orderId.toString(), sender_type = "rider", sender_id = riderId, message = msg)', 'ChatSendRequest(order_id = orderId, sender_type = "rider", sender_id = riderId, message = msg)')
chat = chat.replace('ChatSendRequest(orderId.toString(), "rider", riderId, messageText)', 'ChatSendRequest(orderId, "rider", riderId, messageText)')
chat = chat.replace('it.sender_id == riderId.toString()', 'it.sender_id == riderId.toString()') # wait, sender_id is String? now

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chat)

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

main = main.replace('fun fetchOrders(riderId: String)', 'fun fetchOrders(riderId: Int)')
main = main.replace('fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: String)', 'fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: Int)')
main = main.replace('fun getRiderOrders(@Query("rider_id") riderId: String)', 'fun getRiderOrders(@Query("rider_id") riderId: Int)')
main = main.replace('fun getChatMessages(@Query("order_id") orderId: String)', 'fun getChatMessages(@Query("order_id") orderId: Int)')

main = main.replace('fetchOrders(authData.id ?: "")', 'fetchOrders(authData.id?.toIntOrNull() ?: 0)')

main = main.replace('data class ChatSendRequest(\n    val order_id: String,\n    val sender_type: String,\n    val sender_id: String,', 'data class ChatSendRequest(\n    val order_id: Int,\n    val sender_type: String,\n    val sender_id: Int,')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)

with open('app/src/main/java/com/example/ChatWorker.kt', 'r') as f:
    cw = f.read()
cw = cw.replace('getChatMessages(orderId)', 'getChatMessages(orderId.toIntOrNull() ?: 0)')
with open('app/src/main/java/com/example/ChatWorker.kt', 'w') as f:
    f.write(cw)

with open('app/src/main/java/com/example/OrderPollingWorker.kt', 'r') as f:
    ow = f.read()
ow = ow.replace('getRiderOrders(riderId)', 'getRiderOrders(riderId.toIntOrNull() ?: 0)')
with open('app/src/main/java/com/example/OrderPollingWorker.kt', 'w') as f:
    f.write(ow)

