with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chatui = f.read()

old_state = """    var messages by remember { mutableStateOf<List<ChatMessage>>(emptyList()) }"""
new_state = """    val chatMessages = remember { androidx.compose.runtime.mutableStateListOf<ChatMessage>() }"""
chatui = chatui.replace(old_state, new_state)

# Polling logic
old_poll = """                val response = RetrofitClient.apiService.getChatMessages(orderId)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val newMessages = response.body()?.data ?: emptyList()
                    if (newMessages.size > messages.size) {
                        messages = newMessages
                        scope.launch {
                            listState.animateScrollToItem(messages.size)
                        }
                    } else {
                        // Update statuses
                        messages = newMessages
                    }
                }"""

new_poll = """                val response = RetrofitClient.apiService.getChatMessages(orderId)
                if (response.isSuccessful) {
                    val body = response.body()
                    android.util.Log.d("CHAT_API", "Fetched ${body?.data?.size} messages")
                    if (body?.status == "success") {
                        val newMessages = body.data ?: emptyList()
                        if (newMessages.size != chatMessages.size) {
                            chatMessages.clear()
                            chatMessages.addAll(newMessages)
                            scope.launch {
                                listState.animateScrollToItem(chatMessages.size)
                            }
                        } else {
                            chatMessages.clear()
                            chatMessages.addAll(newMessages)
                        }
                    }
                }"""
chatui = chatui.replace(old_poll, new_poll)

# And the optimistic insert and send logic
old_send = """                            messages = messages + tempMsg
                            scope.launch {
                                listState.animateScrollToItem(messages.size)
                                try {
                                    val sendResp = RetrofitClient.apiService.sendChatMessage(
                                        ChatSendRequest(orderId, mySenderType, mySenderId, msg)
                                    )
                                    if (sendResp.isSuccessful && sendResp.body()?.status == "success") {
                                        val getResp = RetrofitClient.apiService.getChatMessages(orderId)
                                        if (getResp.isSuccessful && getResp.body()?.status == "success") {
                                            messages = getResp.body()?.data ?: emptyList()
                                        } else {
                                            messages = messages.filter { it.id != -1 }
                                        }
                                    } else {
                                        messages = messages.filter { it.id != -1 }
                                    }
                                } catch (e: Exception) {
                                    android.util.Log.e("CHAT_ERROR", "Failed to send", e)
                                    messages = messages.filter { it.id != -1 }
                                }
                            }"""

new_send = """                            chatMessages.add(tempMsg)
                            scope.launch {
                                listState.animateScrollToItem(chatMessages.size)
                                try {
                                    val sendResp = RetrofitClient.apiService.sendChatMessage(
                                        ChatSendRequest(orderId, mySenderType, mySenderId, msg)
                                    )
                                    if (sendResp.isSuccessful && sendResp.body()?.status == "success") {
                                        val getResp = RetrofitClient.apiService.getChatMessages(orderId)
                                        if (getResp.isSuccessful) {
                                            val body = getResp.body()
                                            android.util.Log.d("CHAT_API", "Fetched ${body?.data?.size} messages after send")
                                            if (body?.status == "success") {
                                                chatMessages.clear()
                                                body.data?.let { chatMessages.addAll(it) }
                                            } else {
                                                chatMessages.removeAll { it.id == -1 }
                                            }
                                        } else {
                                            chatMessages.removeAll { it.id == -1 }
                                        }
                                    } else {
                                        chatMessages.removeAll { it.id == -1 }
                                    }
                                } catch (e: Exception) {
                                    android.util.Log.e("CHAT_ERROR", "Failed to send", e)
                                    chatMessages.removeAll { it.id == -1 }
                                }
                            }"""
chatui = chatui.replace(old_send, new_send)

chatui = chatui.replace("items(messages)", "items(chatMessages)")
chatui = chatui.replace("messages.isEmpty()", "chatMessages.isEmpty()")

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chatui)
