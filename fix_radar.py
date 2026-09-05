import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make sure the UI doesn't freeze because the ModalBottomSheet is rendering *behind* the Column
# Moving it out of the main column context if necessary

target = """    if (selectedOrderForReview != null) {
        ModalBottomSheet(
            onDismissRequest = { selectedOrderForReview = null },
            sheetState = radarSheetState,
            containerColor = Color.White,
            modifier = Modifier.fillMaxHeight(0.9f)
        ) {"""

replacement = """    if (selectedOrderForReview != null) {
        ModalBottomSheet(
            onDismissRequest = { selectedOrderForReview = null },
            sheetState = radarSheetState,
            containerColor = Color.White,
            modifier = Modifier.fillMaxHeight(0.9f)
        ) {"""

# Replace `Column(modifier = Modifier.fillMaxSize().background(Color(0xFFF5F6FA))) {`
# With a Box wrapper so the ModalBottomSheet can overlay correctly if needed.
# Actually, ModalBottomSheet handles its own window, but sometimes Compose versions bug out if it's placed sequentially.

target2 = """    // Clean Layout Hierarchy: No Overlapping Full-Size Boxes
    Column(modifier = Modifier.fillMaxSize().background(Color(0xFFF5F6FA))) {"""

replacement2 = """    // Clean Layout Hierarchy: No Overlapping Full-Size Boxes
    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF5F6FA))) {
    Column(modifier = Modifier.fillMaxSize()) {"""

target3 = """            }
        }
    }

    if (selectedOrderForReview != null) {"""

replacement3 = """            }
        }
    }
    } // End of Column, still inside Box

    if (selectedOrderForReview != null) {"""


if target2 in content and target3 in content:
    content = content.replace(target2, replacement2)
    content = content.replace(target3, replacement3)
    
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
