import re

with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    content = f.read()

# I will just write a completely clean version of ChatUI.kt instead of trying to regex it because it is complex.

new_content = """package com.example

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import androidx.lifecycle.viewmodel.compose.viewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    orderId: Int,
    mySenderType: String, // "rider" or "customer"
    mySenderId: Int,
    onBack: () -> Unit,
    viewModel: ChatViewModel = viewModel()
) {
    val chatMessages by viewModel.chatMessages.collectAsState()
    val isOtherTyping by viewModel.isOtherTyping.collectAsState()
    
    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    LaunchedEffect(orderId) {
        viewModel.startPolling(orderId, mySenderType)
    }

    LaunchedEffect(chatMessages.size) {
        if (chatMessages.isNotEmpty()) {
            listState.animateScrollToItem(chatMessages.size - 1)
        }
    }

    // Debounce typing status
    LaunchedEffect(inputText) {
        if (inputText.isNotBlank()) {
            viewModel.updateTypingStatus(orderId, mySenderType, true)
            delay(2000)
            viewModel.updateTypingStatus(orderId, mySenderType, false)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Column {
                        Text("Chat - Order #$orderId", color = Color.White)
                        if (isOtherTyping) {
                            Text("Typing...", color = Color.White.copy(alpha=0.7f), fontSize = 12.sp)
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF03045E))
            )
        },
        bottomBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = inputText,
                    onValueChange = { inputText = it },
                    modifier = Modifier.weight(1f),
                    placeholder = { Text("Type a message...") },
                    shape = RoundedCornerShape(24.dp)
                )
                Spacer(Modifier.width(8.dp))
                IconButton(
                    onClick = {
                        if (inputText.isNotBlank()) {
                            viewModel.sendChatMessage(orderId, mySenderType, mySenderId, inputText)
                            inputText = ""
                        }
                    },
                    modifier = Modifier
                        .background(Color(0xFF00B4D8), androidx.compose.foundation.shape.CircleShape)
                        .padding(8.dp)
                ) {
                    Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White)
                }
            }
        }
    ) { padding ->
        LazyColumn(
            state = listState,
            contentPadding = PaddingValues(16.dp),
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(Color(0xFFF8F9FA)),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(chatMessages) { msg ->
                val isMine = msg.senderType == mySenderType && msg.senderId == mySenderId
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = if (isMine) Arrangement.End else Arrangement.Start
                ) {
                    Column(horizontalAlignment = if (isMine) Alignment.End else Alignment.Start) {
                        Box(
                            modifier = Modifier
                                .background(
                                    color = if (isMine) Color(0xFF00B4D8) else Color(0xFFE0E0E0),
                                    shape = RoundedCornerShape(12.dp).copy(
                                        bottomEnd = if (isMine) androidx.compose.foundation.shape.CornerSize(0.dp) else androidx.compose.foundation.shape.CornerSize(12.dp),
                                        bottomStart = if (!isMine) androidx.compose.foundation.shape.CornerSize(0.dp) else androidx.compose.foundation.shape.CornerSize(12.dp)
                                    )
                                )
                                .padding(12.dp)
                                .widthIn(max = 280.dp)
                        ) {
                            Text(
                                text = msg.message ?: "",
                                color = if (isMine) Color.White else Color.Black
                            )
                        }
                        if (isMine && msg.status != null) {
                            Text(
                                text = msg.status ?: "",
                                fontSize = 10.sp,
                                color = Color.Gray,
                                modifier = Modifier.padding(top = 2.dp, end = 4.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
"""

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(new_content)
