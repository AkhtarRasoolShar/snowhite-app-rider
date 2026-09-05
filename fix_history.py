import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add showStatusDialogForOrder to HistoryScreen
dialog_decl = """    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }
    var showStatusDialogForOrder by remember { mutableStateOf<RiderOrder?>(null) }"""

content = content.replace("    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }", dialog_decl)

# Update the Button onClick to trigger dialog
old_button = """                                    Button(
                                        onClick = { selectedOrderForUpdate = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(8.dp),
                                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                                    ) {
                                        Text("Update", fontSize = 12.sp, color = Color.White)
                                    }"""

new_button = """                                    Button(
                                        onClick = { showStatusDialogForOrder = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(8.dp),
                                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                                    ) {
                                        Text("Update", fontSize = 12.sp, color = Color.White)
                                    }"""
content = content.replace(old_button, new_button)


# Add the dialog code before the ModalBottomSheet
dialog_code = """        if (showStatusDialogForOrder != null) {
            val order = showStatusDialogForOrder!!
            androidx.compose.material3.AlertDialog(
                onDismissRequest = { showStatusDialogForOrder = null },
                title = { Text("Update Order #${order.orderId}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E)) },
                text = {
                    Column {
                        val statuses = listOf("RECEIVED_AT_HUB", "IN_WASHING", "OUT_FOR_DELIVERY", "DELIVERED")
                        statuses.forEach { status ->
                            Button(
                                onClick = { 
                                    viewModel.updateOrderStatus(order.orderId.toString(), status, context)
                                    showStatusDialogForOrder = null
                                },
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Text(status, color = Color.White)
                            }
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showStatusDialogForOrder = null }) {
                        Text("Cancel", color = Color.Gray)
                    }
                },
                containerColor = Color.White
            )
        }

        if (selectedOrderForUpdate != null) {"""

content = content.replace("        if (selectedOrderForUpdate != null) {", dialog_code)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

