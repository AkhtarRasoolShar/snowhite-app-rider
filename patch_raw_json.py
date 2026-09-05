import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """    @Headers("Content-Type: application/json")
    @POST("routes.php?action=send_chat_message")
    suspend fun sendChatMessage(@Body request: SendMessageRequest): retrofit2.Response<GenericResponse<Any>>"""

replacement = """    @Headers("Content-Type: application/json")
    @POST("routes.php?action=send_chat_message")
    suspend fun sendChatMessage(@Body requestBody: okhttp3.RequestBody): retrofit2.Response<GenericResponse<Any>>"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("MainActivity.kt: Target not found")
    
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content2 = f.read()

target2 = """            try {
                val request = SendMessageRequest(orderId, senderType, senderId, message)
                val response = RetrofitClient.apiService.sendChatMessage(request)"""

replacement2 = """            try {
                val jsonObject = org.json.JSONObject()
                jsonObject.put("order_id", orderId)
                jsonObject.put("sender_type", senderType)
                jsonObject.put("sender_id", senderId)
                jsonObject.put("message", message)
                
                val rawJsonString = jsonObject.toString()
                val requestBody = okhttp3.RequestBody.create(okhttp3.MediaType.parse("application/json; charset=utf-8"), rawJsonString)
                
                val response = RetrofitClient.apiService.sendChatMessage(requestBody)"""

if target2 in content2:
    content2 = content2.replace(target2, replacement2)
else:
    print("ChatViewModel.kt: Target not found")

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(content2)
