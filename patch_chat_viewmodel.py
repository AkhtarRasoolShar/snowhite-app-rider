import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

target = 'val tempMsg = ChatMessage(-1, orderId, senderType, senderId, message, currentTime, "Sending")'
replacement = 'val tempMsg = ChatMessage(-1, orderId, senderType, senderId, message, currentTime, "Sending", "0")'

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(content)
