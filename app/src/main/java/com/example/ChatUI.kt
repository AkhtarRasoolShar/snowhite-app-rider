package com.example

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
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
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalContext
import android.content.Context
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

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
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
    
    val context = LocalContext.current
    val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
    val qr1 = prefs.getString("quick_reply_1", "I am on my way!") ?: "I am on my way!"
    val qr2 = prefs.getString("quick_reply_2", "I have arrived at the pickup location.") ?: "I have arrived at the pickup location."

    val scope = rememberCoroutineScope()
    
    LaunchedEffect(orderId) {
        while(true) {
            viewModel.fetchMessages(orderId)
            delay(3000) // Poll every 3 seconds
        }
    }
    
    var previousCount by remember { mutableIntStateOf(0) }
    val isKeyboardVisible = WindowInsets.ime.getBottom(LocalDensity.current) > 0
    LaunchedEffect(chatMessages.size, isKeyboardVisible) {
        val currentSize = chatMessages.size
        
        // 1. Auto-Scroll to bottom
        if (currentSize > 0) {
            listState.animateScrollToItem(currentSize - 1)
        }

        // 2. Play Notification Tone for NEW INCOMING messages
        if (currentSize > previousCount && previousCount > 0) {
            val lastMessage = chatMessages.last()
            
            val isIncoming = !lastMessage.senderType.equals(mySenderType, ignoreCase = true)
            
            if (isIncoming) {
                try {
                    val uri = android.media.RingtoneManager.getDefaultUri(android.media.RingtoneManager.TYPE_NOTIFICATION)
                    val ringtone = android.media.RingtoneManager.getRingtone(context, uri)
                    ringtone.play()
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
        previousCount = currentSize
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
        modifier = Modifier.fillMaxSize().imePadding(),
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
                Column(
                    modifier = Modifier.fillMaxWidth().navigationBarsPadding()
                ) {
                    // Quick Replies
                    LazyRow(
                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        if (qr1.isNotBlank()) {
                            item {
                                Surface(
                                    shape = RoundedCornerShape(16.dp),
                                    color = Color(0xFFE3F2FD),
                                    onClick = { 
                                        viewModel.sendChatMessage(orderId, mySenderType, mySenderId, qr1)
                                    }
                                ) {
                                    Text(
                                        text = qr1,
                                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                        color = Color(0xFF00B4D8),
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.Medium
                                    )
                                }
                            }
                        }
                        if (qr2.isNotBlank()) {
                            item {
                                Surface(
                                    shape = RoundedCornerShape(16.dp),
                                    color = Color(0xFFE3F2FD),
                                    onClick = { 
                                        viewModel.sendChatMessage(orderId, mySenderType, mySenderId, qr2)
                                    }
                                ) {
                                    Text(
                                        text = qr2,
                                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                        color = Color(0xFF00B4D8),
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.Medium
                                    )
                                }
                            }
                        }
                    }
                    
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(start = 16.dp, end = 16.dp, bottom = 12.dp),
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
                        val isMine = msg.senderType.equals(mySenderType, ignoreCase = true)
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
                    val isRead = msg.isRead == "1" || msg.isRead == "true"
                    val statusIcon = if (isRead) Icons.Default.DoneAll else when (msg.status?.lowercase()) {
                        "sending" -> Icons.Default.Done
                        "sent" -> Icons.Default.Done
                        "delivered", "seen" -> Icons.Default.DoneAll
                        else -> Icons.Default.Done
                    }
                    val statusTint = if (isRead || msg.status?.lowercase() == "seen") Color(0xFF00B4D8) else Color.Gray
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
