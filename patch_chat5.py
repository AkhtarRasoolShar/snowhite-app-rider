import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

target1 = """    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()"""

replacement1 = """    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()
    
    val context = LocalContext.current
    val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
    val qr1 = prefs.getString("quick_reply_1", "I am on my way!") ?: "I am on my way!"
    val qr2 = prefs.getString("quick_reply_2", "I have arrived at the pickup location.") ?: "I have arrived at the pickup location."
"""
content = content.replace(target1, replacement1)

target2 = """        bottomBar = {
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
                ) {"""

replacement2 = """        bottomBar = {
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
                    ) {"""
content = content.replace(target2, replacement2)

# Make sure LazyRow is imported
if "import androidx.compose.foundation.lazy.LazyRow" not in content:
    content = content.replace("import androidx.compose.foundation.lazy.LazyColumn", "import androidx.compose.foundation.lazy.LazyColumn\nimport androidx.compose.foundation.lazy.LazyRow")

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
