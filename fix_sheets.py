import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will find the whole block:
radar_block_start = "if (selectedOrderForReview != null) {"
radar_block_end = "    }\n}\n"

start_idx = content.find(radar_block_start)
if start_idx != -1:
    idx = start_idx
    open_count = 0
    found_first = False
    while idx < len(content):
        if content[idx] == '{':
            open_count += 1
            found_first = True
        elif content[idx] == '}':
            open_count -= 1
        if found_first and open_count == 0:
            break
        idx += 1
    
    end_idx = idx + 1
    
    new_radar_sheet = """if (selectedOrderForReview != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForReview = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                OrderDetailsSheetContent(
                    order = selectedOrderForReview!!,
                    isHistory = false,
                    onAccept = {
                        viewModel.acceptOrder(selectedOrderForReview!!.order_id.toString(), context)
                        selectedOrderForReview = null
                    },
                    onReject = {
                        viewModel.rejectOrder(selectedOrderForReview!!.order_id ?: 0, context)
                        selectedOrderForReview = null
                    }
                )
            }
        }"""
    content = content[:start_idx] + new_radar_sheet + content[end_idx:]


history_block_start = "if (selectedOrderForUpdate != null) {"
start_idx = content.find(history_block_start)
if start_idx != -1:
    idx = start_idx
    open_count = 0
    found_first = False
    while idx < len(content):
        if content[idx] == '{':
            open_count += 1
            found_first = True
        elif content[idx] == '}':
            open_count -= 1
        if found_first and open_count == 0:
            break
        idx += 1
    
    end_idx = idx + 1
    
    new_history_sheet = """if (selectedOrderForUpdate != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForUpdate = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                OrderDetailsSheetContent(
                    order = selectedOrderForUpdate!!,
                    isHistory = true,
                    onUpdateStatus = { nextStatus ->
                        viewModel.updateOrderStatus(selectedOrderForUpdate!!.order_id.toString(), nextStatus, context)
                        selectedOrderForUpdate = null
                    },
                    onPrint = { printReceipt(context, selectedOrderForUpdate!!) },
                    onChat = {
                        navController.navigate("chat/${selectedOrderForUpdate!!.order_id}")
                    }
                )
            }
        }"""
    content = content[:start_idx] + new_history_sheet + content[end_idx:]


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
