import re
with open("/app/applet/app/src/main/java/com/example/ui/screens/LaundryHomeScreen.kt", "r") as f:
    content = f.read()

# Add weight to item text column
content = content.replace(
    'Column {',
    'Column(modifier = Modifier.weight(1f)) {'
)

with open("/app/applet/app/src/main/java/com/example/ui/screens/LaundryHomeScreen.kt", "w") as f:
    f.write(content)
