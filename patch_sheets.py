import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix RadarScreen Sheet
radar_sheet_start = '            ModalBottomSheet(\n                onDismissRequest = { selectedOrderForReview = null },\n                sheetState = sheetState,\n                containerColor = Color.White\n            ) {'
radar_sheet_end = '                    }\n                }\n            }'
# We will use string manipulation to find it
start_idx = content.find(radar_sheet_start)
if start_idx != -1:
    end_idx = content.find('            }', start_idx + len(radar_sheet_start))
    # Wait, end_idx might just find the first closing brace.
    # Let's just use bracket matching again.
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
    
    new_radar_sheet = """            ModalBottomSheet(
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
                        showReviewSheet = false
                    },
                    onReject = {
                        viewModel.rejectOrder(selectedOrderForReview!!.order_id ?: 0, context)
                        selectedOrderForReview = null
                        showReviewSheet = false
                    }
                )
            }"""
    content = content[:start_idx] + new_radar_sheet + content[end_idx:]

# Fix HistoryScreen Sheet
history_sheet_start = '            ModalBottomSheet(\n                onDismissRequest = { selectedOrderForUpdate = null },\n                sheetState = sheetState,\n                containerColor = Color.White\n            ) {'

start_idx = content.find(history_sheet_start)
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
    
    new_history_sheet = """            ModalBottomSheet(
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
                        showUpdateSheet = false
                    },
                    onPrint = { printReceipt(context, selectedOrderForUpdate!!) },
                    onChat = {
                        navController.navigate("chat/${selectedOrderForUpdate!!.order_id}")
                    }
                )
            }"""
    content = content[:start_idx] + new_history_sheet + content[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
