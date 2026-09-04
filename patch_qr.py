import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add to ViewModel State
if "_quickReply1" not in content:
    content = content.replace(
        "val bankIban = _bankIban.asStateFlow()",
        "val bankIban = _bankIban.asStateFlow()\n\n    private val _quickReply1 = MutableStateFlow(\"I am on my way!\")\n    val quickReply1 = _quickReply1.asStateFlow()\n    private val _quickReply2 = MutableStateFlow(\"I have arrived at the pickup location.\")\n    val quickReply2 = _quickReply2.asStateFlow()"
    )

# Add to initSession
if "quick_reply_1" not in content:
    content = content.replace(
        "_bankIban.value = prefs.getString(\"bank_iban\", \"\") ?: \"\"",
        "_bankIban.value = prefs.getString(\"bank_iban\", \"\") ?: \"\"\n        _quickReply1.value = prefs.getString(\"quick_reply_1\", \"I am on my way!\") ?: \"I am on my way!\"\n        _quickReply2.value = prefs.getString(\"quick_reply_2\", \"I have arrived at the pickup location.\") ?: \"I have arrived at the pickup location.\""
    )

# Add to saveProfileDetails signature and body
if "qr1: String, qr2: String" not in content:
    content = content.replace(
        "fun saveProfileDetails(context: Context, address: String, bank: String, iban: String) {",
        "fun saveProfileDetails(context: Context, address: String, bank: String, iban: String, qr1: String, qr2: String) {"
    ).replace(
        "putString(\"bank_iban\", iban)",
        "putString(\"bank_iban\", iban)\n            putString(\"quick_reply_1\", qr1)\n            putString(\"quick_reply_2\", qr2)"
    )

# Add states in ProfileScreen
if "var qr1 by remember" not in content:
    content = content.replace(
        "var whatsapp by remember { mutableStateOf(if (viewModel.whatsappNumber.value.isNotEmpty()) viewModel.whatsappNumber.value else viewModel.riderPhone.value) }",
        "var whatsapp by remember { mutableStateOf(if (viewModel.whatsappNumber.value.isNotEmpty()) viewModel.whatsappNumber.value else viewModel.riderPhone.value) }\n    var qr1 by remember { mutableStateOf(viewModel.quickReply1.value) }\n    var qr2 by remember { mutableStateOf(viewModel.quickReply2.value) }"
    )

# Add UI in ProfileScreen
new_ui = """                Spacer(Modifier.height(16.dp))
                Text("WhatsApp Quick Replies", color = DarkBlue, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = qr1,
                    onValueChange = { qr1 = it },
                    label = { Text("Quick Reply 1 (e.g. On my way)") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = qr2,
                    onValueChange = { qr2 = it },
                    label = { Text("Quick Reply 2 (e.g. Arrived)") },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(Modifier.height(16.dp))
                Button("""

if "WhatsApp Quick Replies" not in content:
    content = content.replace(
        "Spacer(Modifier.height(16.dp))\n                Button(",
        new_ui
    )

# Update onClick
if "qr1, qr2" not in content:
    content = content.replace(
        "viewModel.saveProfileDetails(context, address, bankName, bankIban)",
        "viewModel.saveProfileDetails(context, address, bankName, bankIban, qr1, qr2)"
    )

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
