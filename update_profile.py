import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add states for ProfileScreen
old_states = """    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }"""

new_states = """    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }
    var whatsapp by remember { mutableStateOf(if (viewModel.whatsappNumber.value.isNotEmpty()) viewModel.whatsappNumber.value else viewModel.riderPhone.value) }"""

content = content.replace(old_states, new_states)

# Add new UI section
old_ui = """                Spacer(Modifier.height(16.dp))
                Text("Bank Details for Payouts","""

new_ui = """                Spacer(Modifier.height(16.dp))
                Text("Contact Information", color = DarkBlue, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = whatsapp,
                    onValueChange = { whatsapp = it },
                    label = { Text("WhatsApp Number (Visible to Customers)") },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(Modifier.height(16.dp))
                Text("Bank Details for Payouts","""

content = content.replace(old_ui, new_ui)

# Update onClick
old_click = """viewModel.saveProfileDetails(context, address, bankName, bankIban)"""
new_click = """viewModel.saveProfileDetails(context, address, bankName, bankIban)
                        viewModel.updateWhatsApp(context, whatsapp)"""
content = content.replace(old_click, new_click)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
