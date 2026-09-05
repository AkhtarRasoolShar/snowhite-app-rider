with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    content = f.read()

# Polling logging
content = content.replace(
    'android.util.Log.d("CHAT_API", "Fetched ${body?.data?.size} messages")',
    'android.util.Log.d("CHAT_API", "Poll Response - Status: ${body?.status}, Msg: ${body?.message}, DataSize: ${body?.data?.size}")'
)

# Send logging
old_send = """                                    val sendResp = RetrofitClient.apiService.sendChatMessage(
                                        SendMessageRequest(orderId, mySenderType, mySenderId, msg)
                                    )
                                    if (sendResp.isSuccessful && sendResp.body()?.status == "success") {"""

new_send = """                                    val sendResp = RetrofitClient.apiService.sendChatMessage(
                                        SendMessageRequest(orderId, mySenderType, mySenderId, msg)
                                    )
                                    android.util.Log.d("CHAT_API_SEND", "Send Resp: Code=${sendResp.code()}, Body=${sendResp.body()}")
                                    if (sendResp.isSuccessful && sendResp.body()?.status == "success") {"""

content = content.replace(old_send, new_send)

# Fetch after send logging
content = content.replace(
    'android.util.Log.d("CHAT_API", "Fetched ${body?.data?.size} messages after send")',
    'android.util.Log.d("CHAT_API", "Fetch after send - Status: ${body?.status}, Msg: ${body?.message}, DataSize: ${body?.data?.size}")'
)

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(content)
