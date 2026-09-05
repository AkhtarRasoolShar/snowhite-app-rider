import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target1 = """    var qr1 by remember { mutableStateOf(viewModel.quickReply1.value) }
    var qr2 by remember { mutableStateOf(viewModel.quickReply2.value) }"""

content = content.replace(target1, "")

target2 = """                Button(
                    onClick = { viewModel.saveProfileDetails(context, address, bankName, bankIban, qr1, qr2)"""

replacement2 = """                Button(
                    onClick = { viewModel.saveProfileDetails(context, address, bankName, bankIban, viewModel.quickReply1.value, viewModel.quickReply2.value)"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
