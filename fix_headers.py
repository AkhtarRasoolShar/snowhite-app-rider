with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """    @POST("routes.php?action=send_chat_message")
    suspend fun sendChatMessage(@Body request: SendMessageRequest): retrofit2.Response<GenericResponse<Any>>"""

replacement = """    @Headers("Content-Type: application/json")
    @POST("routes.php?action=send_chat_message")
    suspend fun sendChatMessage(@Body request: SendMessageRequest): retrofit2.Response<GenericResponse<Any>>"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Target not found in MainActivity.kt")

