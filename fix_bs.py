with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target_radar = """    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }
    var sortOption by remember { mutableStateOf("Newest") }"""
replacement_radar = """    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }
    val radarSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var sortOption by remember { mutableStateOf("Newest") }"""

target_radar_if = """        if (selectedOrderForReview != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForReview = null },
                sheetState = sheetState,"""
replacement_radar_if = """        if (selectedOrderForReview != null) {
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForReview = null },
                sheetState = radarSheetState,"""

target_history = """    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }
    var showStatusDialogForOrder by remember { mutableStateOf<RiderOrder?>(null) }"""
replacement_history = """    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }
    val historySheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showStatusDialogForOrder by remember { mutableStateOf<RiderOrder?>(null) }"""

target_history_if = """        if (selectedOrderForUpdate != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForUpdate = null },
                sheetState = sheetState,"""
replacement_history_if = """        if (selectedOrderForUpdate != null) {
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForUpdate = null },
                sheetState = historySheetState,"""


if target_radar in content:
    content = content.replace(target_radar, replacement_radar)
    content = content.replace(target_radar_if, replacement_radar_if)
    
if target_history in content:
    content = content.replace(target_history, replacement_history)
    content = content.replace(target_history_if, replacement_history_if)

# Also let's fix MainAppScreen blocking box, just in case `clickable(enabled = false)` is the issue.
target_box = """            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).clickable(enabled = false) {}, contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            }"""
replacement_box = """            if (isLoading) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.White.copy(alpha = 0.5f))
                        .pointerInput(Unit) { detectTapGestures { } }, 
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            }"""
if target_box in content:
    content = content.replace(target_box, replacement_box)

# Wait, let's also remove `pointerInput` from HistoryScreen if it has any, but it doesn't.

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

print("Done replacing.")
