with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_code = """    suspend fun sendChatMessage(@Body request: ChatSendRequest): retrofit2.Response<GenericResponse<Unit>>

    suspend fun updateOrderStatus(@Body request: UpdateOrderStatusRequest): Response<GenericResponse<Unit>>"""

new_code = """    @POST("routes.php?action=send_chat_message")
    suspend fun sendChatMessage(@Body request: ChatSendRequest): retrofit2.Response<GenericResponse<Unit>>

    @POST("routes.php?action=update_order_status")
    suspend fun updateOrderStatus(@Body request: UpdateOrderStatusRequest): Response<GenericResponse<Unit>>"""

content = content.replace(old_code, new_code)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

