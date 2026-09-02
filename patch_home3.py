import re
with open("/app/applet/app/src/main/java/com/example/ui/screens/LaundryHomeScreen.kt", "r") as f:
    content = f.read()

# Make sure all columns are just Column {
content = content.replace("Column(modifier = Modifier.weight(1f)) {", "Column {")

# In GarmentItemCard, there's a Column for the text. Let's find it.
garment_card_body = """            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(12.dp)
            ) {
                Column(modifier = Modifier.weight(1f)) {"""

# Current structure is probably:
# Row(
#     verticalAlignment = Alignment.CenterVertically,
#     modifier = Modifier.padding(12.dp)
# ) {
#     Column {
#         Text(garment.name, ...

content = re.sub(
    r"Row\(\s*verticalAlignment = Alignment\.CenterVertically,\s*modifier = Modifier\.padding\(12\.dp\)\s*\)\s*\{\s*Column\s*\{",
    garment_card_body,
    content
)

with open("/app/applet/app/src/main/java/com/example/ui/screens/LaundryHomeScreen.kt", "w") as f:
    f.write(content)
