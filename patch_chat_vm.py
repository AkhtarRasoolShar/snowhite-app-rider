import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

# Let's just rewrite the whole ChatViewModel.kt
new_content = """package com.example

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import java.text.SimpleDateFormat
import java.util.*

class ChatViewModel : ViewModel() {
    private val _chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatMessages: StateFlow<List<ChatMessage>> = _chatMessages.asStateFlow()

    private val _isOtherTyping = MutableStateFlow(false)
    val isOtherTyping: StateFlow<Boolean> = _isOtherTyping.asStateFlow()

    fun fetchMessages(orderId: Int) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.getChatMessages(orderId)
                if (response.isSuccessful) {
                    val body = response.body()
                    if (body?.status == "success") {
                        val messagesList = body.data ?: emptyList()
                        _chatMessages.value = messagesList
                    } else {
                        Log.e("CHAT_API", "Fetch Messages - Server returned error status: ${body?.message}")
                    }
                } else {
                    Log.e("CHAT_API", "Fetch Messages - Error Response Code: ${response.code()}")
                }
            } catch (e: Exception) {
                Log.e("CHAT_API", "Fetch Messages - Network Exception: ${e.message}")
            }
        }
    }

    fun sendChatMessage(orderId: Int, senderType: String, senderId: Int, message: String) {
        viewModelScope.launch {
            val currentTime = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(Date())
            // Optimistic insert
            val tempMsg = ChatMessage(-1, orderId, senderType, senderId, message, currentTime, "Sending")
            _chatMessages.value = _chatMessages.value + tempMsg

            try {
                val requestObj = SendMessageRequest(orderId, senderType, senderId, message)
                val rawJsonString = com.google.gson.Gson().toJson(requestObj)
                val mediaType = "application/json; charset=utf-8".toMediaTypeOrNull()
                val requestBody = rawJsonString.toRequestBody(mediaType)
                
                val response = RetrofitClient.apiService.sendChatMessage(requestBody)
                if (response.isSuccessful && response.body()?.status == "success") {
                    fetchMessages(orderId)
                } else {
                    Log.e("CHAT_API", "Send Message Failed: ${response.body()?.message}")
                }
            } catch (e: Exception) {
                Log.e("CHAT_API", "Send Message - Network Exception: ${e.message}")
            }
        }
    }

    fun updateTypingStatus(orderId: Int, senderType: String, isTyping: Boolean) {
        viewModelScope.launch {
            try {
                val map = mapOf(
                    "order_id" to orderId.toString(),
                    "sender_type" to senderType,
                    "is_typing" to if (isTyping) "1" else "0"
                )
                RetrofitClient.apiService.updateTypingStatus(map)
            } catch (e: Exception) {
                Log.e("CHAT_API", "Update Typing - Network Exception: ${e.message}")
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(new_content)
print("Updated ChatViewModel.kt")
