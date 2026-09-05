import re

new_vm = """package com.example

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ChatViewModel : ViewModel() {
    private val _chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatMessages: StateFlow<List<ChatMessage>> = _chatMessages

    private val _isOtherTyping = MutableStateFlow(false)
    val isOtherTyping: StateFlow<Boolean> = _isOtherTyping

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

    fun startPolling(orderId: Int, mySenderType: String) {
        viewModelScope.launch {
            while (true) {
                fetchMessages(orderId)
                
                try {
                    val otherType = if (mySenderType == "rider") "customer" else "rider"
                    val typingResp = RetrofitClient.apiService.getTypingStatus(orderId, otherType)
                    if (typingResp.isSuccessful && typingResp.body()?.status == "success") {
                        _isOtherTyping.value = typingResp.body()?.data?.is_typing ?: false
                    }
                } catch (e: Exception) {
                    Log.e("CHAT_API", "Polling Typing Status - Error: ${e.message}")
                }
                delay(3000)
            }
        }
    }

    fun sendChatMessage(orderId: Int, senderType: String, senderId: Int, message: String) {
        viewModelScope.launch {
            // Optimistic update
            val tempMsg = ChatMessage(-1, orderId, senderType, senderId, message, "", "Sending")
            _chatMessages.value = _chatMessages.value + tempMsg

            try {
                val request = SendMessageRequest(orderId, senderType, senderId, message)
                val response = RetrofitClient.apiService.sendChatMessage(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    fetchMessages(orderId)
                } else {
                    Log.e("CHAT_API_SEND", "Send Failed - Server Status: ${response.body()?.status}")
                    _chatMessages.value = _chatMessages.value.filter { it.id != -1 }
                }
            } catch (e: Exception) {
                Log.e("CHAT_API_SEND", "Send Exception: ${e.message}")
                _chatMessages.value = _chatMessages.value.filter { it.id != -1 }
            }
        }
    }

    fun updateTypingStatus(orderId: Int, senderType: String, isTyping: Boolean) {
        viewModelScope.launch {
            try {
                RetrofitClient.apiService.updateTypingStatus(
                    mapOf(
                        "order_id" to orderId.toString(),
                        "sender_type" to senderType,
                        "is_typing" to isTyping.toString()
                    )
                )
            } catch (e: Exception) {
                Log.e("CHAT_API", "Update Typing - Error: ${e.message}")
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(new_vm)
