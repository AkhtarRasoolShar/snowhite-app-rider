import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_header = """            Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
                Text("Update Order Status", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = DarkBlue)
                Spacer(Modifier.height(8.dp))
                Text("Order #${selectedOrderForUpdate!!.order_id}", color = Color.Gray)"""

new_header = """            Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column {
                        Text("Update Order Status", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = DarkBlue)
                        Spacer(Modifier.height(8.dp))
                        Text("Order #${selectedOrderForUpdate!!.order_id}", color = Color.Gray)
                    }
                    IconButton(onClick = { printReceipt(context, selectedOrderForUpdate!!) }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print Receipt", tint = TealAccent)
                    }
                }"""
content = content.replace(old_header, new_header)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
