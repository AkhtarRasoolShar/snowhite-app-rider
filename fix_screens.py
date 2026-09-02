import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Update RadarScreen background
content = content.replace(
    'Box(modifier = Modifier.fillMaxSize().background(SoftWhite)) {',
    'Box(modifier = Modifier.fillMaxSize()) {\n        AsyncImage(model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080", contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())\n        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.92f)))'
)

# Replace any existing AsyncImage background in RadarScreen that might be there
content = re.sub(r'AsyncImage\([\s\S]*?modifier = Modifier\.fillMaxSize\(\)\.alpha\(0\.05f\)\n        \)', '', content)

# Update HistoryScreen
content = content.replace(
    'Column(modifier = Modifier.fillMaxSize().background(SoftWhite)) {',
    'Box(modifier = Modifier.fillMaxSize()) {\n        AsyncImage(model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080", contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())\n        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.92f)))\n        Column(modifier = Modifier.fillMaxSize()) {'
)
content = content.replace('        }\n    }\n\n    if (selectedOrderForUpdate != null) {', '        }\n    }\n    }\n\n    if (selectedOrderForUpdate != null) {')

# Update ProfileScreen
content = content.replace(
    'Column(modifier = Modifier.fillMaxSize().background(SoftWhite)) {',
    'Box(modifier = Modifier.fillMaxSize()) {\n        AsyncImage(model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080", contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())\n        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.92f)))\n        Column(modifier = Modifier.fillMaxSize()) {'
)
content = content.replace('        }\n    }\n}\n\n@Composable', '        }\n    }\n    }\n}\n\n@Composable') # Might need to be more precise, let's just do it cleanly

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
