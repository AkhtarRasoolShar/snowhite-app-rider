import re
with open("/app/applet/app/src/main/java/com/example/ui/screens/LaundryHomeScreen.kt", "r") as f:
    content = f.read()

# Revert my bad patch globally
content = content.replace("Column(modifier = Modifier.weight(1f)) {", "Column {")

# Then selectively apply weight to GarmentItemCard's text column
content = content.replace(
    'Column {',
    'Column(modifier = Modifier.weight(1f)) {',
    1
) # Wait, this might match the first Column in the file.

with open("/app/applet/app/src/main/java/com/example/ui/screens/LaundryHomeScreen.kt", "w") as f:
    f.write(content)
