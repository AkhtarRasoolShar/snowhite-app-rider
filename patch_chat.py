import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

# We need to replace everything from @OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun OrderChatScreen
# to the end of OrderChatScreen (right before @Composable\nfun MessageBubble)

start_marker = "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun OrderChatScreen("
end_marker = "@Composable\nfun MessageBubble("

if start_marker in content and end_marker in content:
    start_idx = content.index(start_marker)
    end_idx = content.index(end_marker)
    
    new_screen = """@OptIn(ExperimentalMaterial3Api::class)
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
        while(true) {
            viewModel.fetchMessages(orderId)
            delay(3000) // Poll every 3 seconds
        }
    }
    
    LaunchedEffect(chatMessages.size) {
        if (chatMessages.isNotEmpty()) {
            listState.animateScrollToItem(chatMessages.size - 1)
        }
    }
    
    val isImeVisible = WindowInsets.isImeVisible
    LaunchedEffect(isImeVisible) {
        if (isImeVisible && chatMessages.isNotEmpty()) {
            delay(100)
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
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFEFEFEF))
            .systemBarsPadding()
            .imePadding()
    ) {
        // 1. HEADER (Fixed at the top)
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
        
        // 2. MESSAGES (Takes remaining space)
        if (chatMessages.isEmpty()) {
            Column(
                modifier = Modifier.weight(1f).fillMaxWidth(),
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
                modifier = Modifier.weight(1f).fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(chatMessages) { msg ->
                    val isMine = msg.senderType.equals(mySenderType, ignoreCase = true)
                    MessageBubble(msg = msg, isMine = isMine)
                }
            }
        }
        
        // 3. INPUT BAR (Fixed at the bottom)
        Surface(
            color = Color.White,
            shadowElevation = 8.dp,
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
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

"""
    
    new_content = content[:start_idx] + new_screen + content[end_idx:]
    
    with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
        f.write(new_content)
    print("Patched ChatUI.kt successfully.")
else:
    print("Markers not found!")

