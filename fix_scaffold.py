import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace MainAppScreen
pattern = r"""fun MainAppScreen\(viewModel: RiderViewModel\) \{\s*val navController = rememberNavController\(\)\s*Scaffold\(\s*bottomBar = \{(.*?)\}\s*\) \{ padding ->\s*NavHost\(navController = navController, startDestination = "radar", modifier = Modifier\.padding\(padding\)\) \{(.*?)\}\s*\}"""

def replacer(match):
    bottom_bar = match.group(1)
    nav_host = match.group(2)
    return f"""fun MainAppScreen(viewModel: RiderViewModel) {{
    val navController = rememberNavController()
    val isLoading by viewModel.isLoading.collectAsState()
    Scaffold(
        bottomBar = {{{bottom_bar}}}
    ) {{ padding ->
        Box(modifier = Modifier.padding(padding).fillMaxSize()) {{
            NavHost(navController = navController, startDestination = "radar", modifier = Modifier.fillMaxSize()) {{{nav_host}}}
            if (isLoading) {{
                Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).clickable(enabled = false) {{}}, contentAlignment = Alignment.Center) {{
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }}
            }}
        }}
    }}"""

new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Fix RadarScreen isLoading check
new_content = new_content.replace(
"""            if (isLoading && orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    SophisticatedLoadingIndicator()
                }
            } else if (orders.isEmpty()) {""",
"""            if (orders.isEmpty()) {"""
)

# Fix HistoryScreen isLoading check
new_content = new_content.replace(
"""            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            } else if (orders.isEmpty()) {""",
"""            if (orders.isEmpty()) {"""
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)
print("Done!")
