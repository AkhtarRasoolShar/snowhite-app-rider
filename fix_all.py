import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix order_id type mismatch in API calls
content = content.replace("viewModel.acceptOrder(order.order_id, context)", "viewModel.acceptOrder(order.order_id?.toString() ?: \"\", context)")
content = content.replace("viewModel.updateOrderStatus(selectedOrderForUpdate!!.order_id, st, context)", "viewModel.updateOrderStatus(selectedOrderForUpdate!!.order_id?.toString() ?: \"\", st, context)")

# Fix HistoryScreen selectedOrderForUpdate type
content = content.replace("var selectedOrderForUpdate by remember { mutableStateOf<RiderOrderResponse?>(null) }", "var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
