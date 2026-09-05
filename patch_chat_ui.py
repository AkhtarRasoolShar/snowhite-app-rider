import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

target1 = """    LaunchedEffect(orderId) {
        viewModel.startPolling(orderId, mySenderType)
    }"""

replacement1 = """    LaunchedEffect(orderId) {
        while(true) {
            viewModel.fetchMessages(orderId)
            delay(3000) // Poll every 3 seconds
        }
    }"""

target2 = """                        val isMine = msg.senderType == mySenderType && msg.senderId == mySenderId"""

replacement2 = """                        val isMine = msg.senderType.equals(mySenderType, ignoreCase = true)"""

if target1 in content and target2 in content:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
        f.write(content)
    print("Patched ChatUI.kt")
else:
    print("Target not found in ChatUI.kt")
    print("target1 present:", target1 in content)
    print("target2 present:", target2 in content)
