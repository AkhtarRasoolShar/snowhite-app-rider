with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Instead of regex for Scaffold, use replace
old_scaffold = """    Scaffold(
        bottomBar = {"""
new_scaffold = """    Scaffold(
        contentWindowInsets = WindowInsets.ime,
        bottomBar = {"""

content = content.replace(old_scaffold, new_scaffold)

# We also need to remove .imePadding() from the Box to avoid double-padding
old_box = "        Box(modifier = Modifier.padding(padding).fillMaxSize().imePadding()) {"
new_box = "        Box(modifier = Modifier.padding(padding).fillMaxSize()) {"

content = content.replace(old_box, new_box)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
