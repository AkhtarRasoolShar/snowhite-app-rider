import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

import_str = "import androidx.compose.ui.platform.LocalDensity\n"
if "LocalDensity" not in content:
    content = content.replace("import androidx.compose.ui.Modifier\n", "import androidx.compose.ui.Modifier\n" + import_str)

target = """    LaunchedEffect(chatMessages.size) {
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
    }"""

replacement = """    val isKeyboardVisible = WindowInsets.ime.getBottom(LocalDensity.current) > 0
    LaunchedEffect(chatMessages.size, isKeyboardVisible) {
        if (chatMessages.isNotEmpty()) {
            listState.animateScrollToItem(chatMessages.size - 1)
        }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
