with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

bad_block = """                                Spacer(Modifier.height(16.dp))
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

good_block = """                                Spacer(Modifier.height(16.dp))
                Button("""

parts = content.split(bad_block)
if len(parts) > 2:
    # Keep the first replacement, revert the rest
    content = parts[0] + bad_block + good_block.join(parts[1:])

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
