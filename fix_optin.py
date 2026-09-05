with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("@Composable\nfun OrderChatScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun OrderChatScreen")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
