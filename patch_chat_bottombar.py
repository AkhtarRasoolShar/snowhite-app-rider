import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

bottomBarContent = """        bottomBar = {
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
        }"""

content = content.replace("        bottomBar = {}", bottomBarContent)

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
