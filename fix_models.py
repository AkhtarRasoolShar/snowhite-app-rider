import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # GenericResponse
    content = content.replace('val status: String,', '@SerializedName("status") val status: String? = null,')
    content = content.replace('val message: String,', '@SerializedName("message") val message: String? = null,')
    content = content.replace('val data: T?', '@SerializedName("data") val data: T? = null')

    # TypingStatus
    content = content.replace('val is_typing: Boolean', '@SerializedName("is_typing") val is_typing: Boolean? = null')

    # ChatMessage
    content = content.replace('val id: Int? = null', 'val id: String? = null')
    content = content.replace('val order_id: Int? = null', 'val order_id: String? = null')
    content = content.replace('val sender_id: Int? = null', 'val sender_id: String? = null')

    # RiderAuthData
    content = content.replace('val id: Int,', '@SerializedName("id") val id: String? = null,')
    content = content.replace('val name: String,', '@SerializedName("name") val name: String? = null,')
    content = content.replace('val phone: String,', '@SerializedName("phone") val phone: String? = null,')
    content = content.replace('val service_zone: String', '@SerializedName("service_zone") val service_zone: String? = null')

    # RiderOrder
    content = content.replace('val orderId: Int? = null', 'val orderId: String? = null')
    
    # OrderItem
    content = content.replace('val quantity: Int? = null', 'val quantity: String? = null')

    # Update usages in MainActivity.kt
    if 'MainActivity.kt' in filepath:
        content = content.replace('orders.sortedByDescending { it.orderId ?: 0 }', 'orders.sortedByDescending { it.orderId?.toIntOrNull() ?: 0 }')
        content = content.replace('it.orderId ?: it.hashCode()', 'it.orderId?.toIntOrNull() ?: it.hashCode()')
        content = content.replace('viewModel.rejectOrder(selectedOrderForReview!!.orderId ?: 0, context)', 'viewModel.rejectOrder(selectedOrderForReview!!.orderId?.toIntOrNull() ?: 0, context)')
        content = content.replace('getChatMessages(@Query("order_id") orderId: Int)', 'getChatMessages(@Query("order_id") orderId: String)')
        content = content.replace('getTypingStatus(@Query("order_id") orderId: Int', 'getTypingStatus(@Query("order_id") orderId: String')
        content = content.replace('PendingAction.RejectOrder(val orderId: Int)', 'PendingAction.RejectOrder(val orderId: String)')
        content = content.replace('fun rejectOrder(orderId: Int, context: Context)', 'fun rejectOrder(orderId: String, context: Context)')
        
    with open(filepath, 'w') as f:
        f.write(content)

process_file('app/src/main/java/com/example/MainActivity.kt')

# Update ChatWorker.kt
with open('app/src/main/java/com/example/ChatWorker.kt', 'r') as f:
    chat_worker = f.read()
chat_worker = chat_worker.replace('showNotification(orderId, "New message from Customer ($unseenCount)")', 'showNotification(orderId.toIntOrNull() ?: 0, "New message from Customer ($unseenCount)")')
with open('app/src/main/java/com/example/ChatWorker.kt', 'w') as f:
    f.write(chat_worker)

