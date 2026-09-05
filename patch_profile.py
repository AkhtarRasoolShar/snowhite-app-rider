import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update ProfileScreen signature
content = content.replace("fun ProfileScreen(viewModel: RiderViewModel) {", "fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController) {")

# 2. Replace the quick replies section in ProfileScreen with a button
target = """                                Spacer(Modifier.height(16.dp))
                Text("WhatsApp Quick Replies", color = DarkBlue, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = qr1,
                    onValueChange = { qr1 = it },
                    label = { Text("Quick Reply 1 (e.g. On my way)") },
                    modifier = Modifier.fillMaxWidth(),
                    trailingIcon = {
                        IconButton(onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/?text=${Uri.encode(qr1)}"))
                            try { context.startActivity(intent) } catch (e: Exception) { Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show() }
                        }) {
                            Icon(Icons.Default.Send, contentDescription = "Send", tint = Color(0xFF25D366))
                        }
                    }
                )
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = qr2,
                    onValueChange = { qr2 = it },
                    label = { Text("Quick Reply 2 (e.g. Arrived)") },
                    modifier = Modifier.fillMaxWidth(),
                    trailingIcon = {
                        IconButton(onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/?text=${Uri.encode(qr2)}"))
                            try { context.startActivity(intent) } catch (e: Exception) { Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show() }
                        }) {
                            Icon(Icons.Default.Send, contentDescription = "Send", tint = Color(0xFF25D366))
                        }
                    }
                )"""

replacement = """                Spacer(Modifier.height(16.dp))
                Text("App Settings", color = DarkBlue, fontWeight = FontWeight.Bold)
                Button(
                    onClick = { navController.navigate("quickReplies") },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE3F2FD), contentColor = DarkBlue)
                ) {
                    Icon(Icons.Default.Settings, contentDescription = "Settings", modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text("Manage Quick Replies", fontWeight = FontWeight.Medium)
                }"""

content = content.replace(target, replacement)

# 3. Add QuickRepliesScreen composable definition at the end
new_screen = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuickRepliesScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
    var qr1 by remember { mutableStateOf(viewModel.quickReply1.value) }
    var qr2 by remember { mutableStateOf(viewModel.quickReply2.value) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Quick Replies", fontWeight = FontWeight.Bold, color = DarkBlue) },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = DarkBlue)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(SoftWhite)
                .padding(padding)
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                "Save custom message templates to use in the order chat or send via WhatsApp.",
                color = Color.Gray,
                fontSize = 14.sp
            )
            
            OutlinedTextField(
                value = qr1,
                onValueChange = { qr1 = it },
                label = { Text("Quick Reply 1 (e.g. On my way)") },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            )
            OutlinedTextField(
                value = qr2,
                onValueChange = { qr2 = it },
                label = { Text("Quick Reply 2 (e.g. Arrived)") },
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp)
            )
            
            Spacer(Modifier.weight(1f))
            Button(
                onClick = { 
                    viewModel.saveProfileDetails(context, viewModel.homeAddress.value, viewModel.bankName.value, viewModel.bankIban.value, qr1, qr2)
                    Toast.makeText(context, "Quick Replies Saved", Toast.LENGTH_SHORT).show()
                    navController.popBackStack()
                },
                modifier = Modifier.fillMaxWidth().height(48.dp),
                colors = ButtonDefaults.buttonColors(containerColor = TealAccent)
            ) {
                Text("Save Templates", color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
    }
}
"""
content += new_screen

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
