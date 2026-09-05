import re

with open('app/src/main/java/com/example/ChatViewModel.kt', 'r') as f:
    content = f.read()

target = """    fun fetchMessages(orderId: Int) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getChatMessages(orderId)
                Log.d("CHAT_API", "Fetch Messages - Raw Response: Code=${response.code()}, Body=${response.body()}")
                
                if (response.isSuccessful) {
                    val body = response.body()
                    Log.d("CHAT_API", "Fetch Messages - Parsed Body: Status=${body?.status}, Msg=${body?.message}, DataSize=${body?.data?.size}")
                    
                    if (body?.status == "success" && body.data != null) {
                        _chatMessages.value = body.data
                    } else {
                        Log.e("CHAT_API", "Fetch Messages - Server returned error status or null data: ${body?.message}")
                    }
                } else {
                    Log.e("CHAT_API", "Fetch Messages - Error Response Code: ${response.code()}")
                }
            } catch (e: Exception) {
                Log.e("CHAT_API", "Fetch Messages - Network/Mapping Exception: ${e.message}", e)
            }
        }
    }"""

replacement = """    fun fetchMessages(orderId: Int) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getChatMessages(orderId)
                val rawBody = response.body()
                
                Log.d("CHAT_API", "Fetch Messages - Raw Response: Code=${response.code()}, Body=$rawBody")
                
                if (response.isSuccessful) {
                    val body = response.body()
                    
                    if (body?.status == "success") {
                        val messagesList = body.data ?: emptyList()
                        Log.d("CHAT_API", "Fetch Messages - SUCCESS! Parsed Body Status: ${body?.status}, Msg: ${body?.message}, List Size: ${messagesList.size}")
                        _chatMessages.value = messagesList
                    } else {
                        Log.e("CHAT_API", "Fetch Messages - Server returned error status: ${body?.message}")
                    }
                } else {
                    val errorString = response.errorBody()?.string()
                    Log.e("CHAT_API", "Fetch Messages - Error Response Code: ${response.code()}, ErrorBody: $errorString")
                }
            } catch (e: Exception) {
                Log.e("CHAT_API", "Fetch Messages - Network/Mapping Exception: ${e.message}", e)
                e.printStackTrace()
            }
        }
    }"""

if target in content:
    new_content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/ChatViewModel.kt', 'w') as f:
        f.write(new_content)
    print("Replaced successfully!")
else:
    print("Target not found. Doing fallback regex replacement.")
    # Fallback to replace the entire method
    pattern = re.compile(r'    fun fetchMessages\(orderId: Int\) \{.*?    \}', re.DOTALL)
    new_content = pattern.sub(replacement, content, count=1)
    with open('app/src/main/java/com/example/ChatViewModel.kt', 'w') as f:
        f.write(new_content)
    print("Regex replace complete!")

