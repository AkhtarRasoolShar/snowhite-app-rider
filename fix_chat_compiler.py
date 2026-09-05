with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

# Fix maxOfOrNull
content = content.replace("localMessages.maxOfOrNull { it.id }", "localMessages.maxByOrNull { it.id.toInt() }?.id")
# Wait, if id is a string? Let's check ChatMessage data class.
