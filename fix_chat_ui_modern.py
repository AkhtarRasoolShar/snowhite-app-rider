import re

new_chat_ui = """package com.example

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.CornerSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Done
import androidx.compose.material.icons.filled.DoneAll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OrderChatScreen(
    orderId: Int,
    mySenderType: String,
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
                        Text(
                            text = "Customer Support",
                            fontWeight = FontWeight.Bold,
                            fontSize = 18.sp,
                            color = Color.White
                        )
                        Text(
                            text = if (isOtherTyping) "typing..." else "Order #$orderId",
                            fontSize = 12.sp,
                            color = if (isOtherTyping) Color(0xFF00E676) else Color.White.copy(alpha=0.7f),
                            fontWeight = if (isOtherTyping) FontWeight.Medium else FontWeight.Normal
                        )
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
            Surface(
                color = Color.White,
                shadowElevation = 8.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp)
                        .navigationBarsPadding(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = inputText,
                        onValueChange = { inputText = it },
                        modifier = Modifier.weight(1f),
                        placeholder = { Text("Message...", color = Color.Gray) },
                        shape = RoundedCornerShape(24.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Color(0xFF00B4D8),
                            unfocusedBorderColor = Color.LightGray,
                            focusedContainerColor = Color(0xFFF5F6FA),
                            unfocusedContainerColor = Color(0xFFF5F6FA)
                        ),
                        maxLines = 4,
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send)
                    )
                    Spacer(Modifier.width(12.dp))
                    IconButton(
                        onClick = {
                            if (inputText.isNotBlank()) {
                                viewModel.sendChatMessage(orderId, mySenderType, mySenderId, inputText.trim())
                                inputText = ""
                            }
                        },
                        modifier = Modifier
                            .size(48.dp)
                            .background(if (inputText.isNotBlank()) Color(0xFF00B4D8) else Color.LightGray, CircleShape)
                    ) {
                        Icon(
                            Icons.AutoMirrored.Filled.Send,
                            contentDescription = "Send",
                            tint = Color.White,
                            modifier = Modifier.padding(start = 4.dp)
                        )
                    }
                }
            }
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(Color(0xFFEFEFEF))
        ) {
            if (chatMessages.isEmpty()) {
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        Icons.Default.DoneAll,
                        contentDescription = "Empty",
                        tint = Color.LightGray,
                        modifier = Modifier.size(64.dp)
                    )
                    Spacer(Modifier.height(16.dp))
                    Text(
                        "No messages yet.",
                        color = Color.Gray,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        "Send a message to start chatting.",
                        color = Color.Gray,
                        fontSize = 14.sp
                    )
                }
            } else {
                LazyColumn(
                    state = listState,
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 24.dp),
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(chatMessages) { msg ->
                        val isMine = msg.senderType == mySenderType && msg.senderId == mySenderId
                        MessageBubble(msg = msg, isMine = isMine)
                    }
                }
            }
        }
    }
}

@Composable
fun MessageBubble(msg: ChatMessage, isMine: Boolean) {
    val timeFormat = SimpleDateFormat("hh:mm a", Locale.getDefault())
    val formattedTime = try {
        if (!msg.createdAt.isNullOrEmpty()) {
            val parser = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
            val date = parser.parse(msg.createdAt)
            if (date != null) timeFormat.format(date) else ""
        } else {
            timeFormat.format(Date())
        }
    } catch (e: Exception) {
        timeFormat.format(Date())
    }

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isMine) Arrangement.End else Arrangement.Start
    ) {
        Column(
            horizontalAlignment = if (isMine) Alignment.End else Alignment.Start
        ) {
            Box(
                modifier = Modifier
                    .clip(
                        RoundedCornerShape(16.dp).copy(
                            bottomEnd = if (isMine) CornerSize(0.dp) else CornerSize(16.dp),
                            bottomStart = if (!isMine) CornerSize(0.dp) else CornerSize(16.dp)
                        )
                    )
                    .background(if (isMine) Color(0xFF00B4D8) else Color.White)
                    .padding(horizontal = 16.dp, vertical = 10.dp)
                    .widthIn(min = 80.dp, max = 280.dp)
            ) {
                Text(
                    text = msg.message ?: "",
                    color = if (isMine) Color.White else Color(0xFF333333),
                    fontSize = 15.sp,
                    lineHeight = 20.sp
                )
            }
            
            Row(
                modifier = Modifier.padding(top = 4.dp, start = 4.dp, end = 4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = formattedTime,
                    fontSize = 11.sp,
                    color = Color.Gray
                )
                if (isMine) {
                    Spacer(Modifier.width(4.dp))
                    val statusIcon = when (msg.status?.lowercase()) {
                        "sending" -> Icons.Default.Done
                        "sent" -> Icons.Default.Done
                        "delivered", "seen" -> Icons.Default.DoneAll
                        else -> Icons.Default.Done
                    }
                    val statusTint = if (msg.status?.lowercase() == "seen") Color(0xFF00B4D8) else Color.Gray
                    Icon(
                        imageVector = statusIcon,
                        contentDescription = "Status",
                        tint = statusTint,
                        modifier = Modifier.size(14.dp)
                    )
                }
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(new_chat_ui)
