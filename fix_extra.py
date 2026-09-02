with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("@Composable\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
