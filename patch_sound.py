import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

# Add import if needed
if "mutableIntStateOf" not in content:
    content = content.replace("import androidx.compose.runtime.mutableStateOf", "import androidx.compose.runtime.mutableStateOf\nimport androidx.compose.runtime.mutableIntStateOf")

target = """    val isKeyboardVisible = WindowInsets.ime.getBottom(LocalDensity.current) > 0
    LaunchedEffect(chatMessages.size, isKeyboardVisible) {
        if (chatMessages.isNotEmpty()) {
            listState.animateScrollToItem(chatMessages.size - 1)
        }
    }"""

replacement = """    var previousCount by remember { mutableIntStateOf(0) }
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
    }"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("TARGET NOT FOUND!")

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
