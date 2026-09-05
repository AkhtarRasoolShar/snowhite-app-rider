import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """fun QuickRepliesScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
"""
replacement = """fun QuickRepliesScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
    val qr1State = viewModel.quickReply1.collectAsState()
    val qr2State = viewModel.quickReply2.collectAsState()
    var qr1 by remember { mutableStateOf(qr1State.value) }
    var qr2 by remember { mutableStateOf(qr2State.value) }
"""

content = content.replace(target, replacement)
content = content.replace("Icons.AutoMirrored.Filled.ArrowBack", "Icons.Default.ArrowBack")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
