import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

target = """                if (isMine) {
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
                }"""

replacement = """                if (isMine) {
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
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
