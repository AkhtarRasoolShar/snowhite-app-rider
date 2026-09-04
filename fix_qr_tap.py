import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_qr1 = """                OutlinedTextField(
                    value = qr1,
                    onValueChange = { qr1 = it },
                    label = { Text("Quick Reply 1 (e.g. On my way)") },
                    modifier = Modifier.fillMaxWidth()
                )"""

new_qr1 = """                OutlinedTextField(
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
                )"""

old_qr2 = """                OutlinedTextField(
                    value = qr2,
                    onValueChange = { qr2 = it },
                    label = { Text("Quick Reply 2 (e.g. Arrived)") },
                    modifier = Modifier.fillMaxWidth()
                )"""

new_qr2 = """                OutlinedTextField(
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

content = content.replace(old_qr1, new_qr1)
content = content.replace(old_qr2, new_qr2)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
