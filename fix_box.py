with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """            composable("profile") { ProfileScreen(viewModel) }
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).clickable(enabled = false) {}, contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            }
        }"""

replacement = """            composable("profile") { ProfileScreen(viewModel) }
        }
        
        if (isLoading) {
            Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).clickable(enabled = false) {}, contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFF00B4D8))
            }
        }"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Fixed Box placement")
else:
    print("Target not found")
