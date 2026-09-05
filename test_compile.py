import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

# Replace bottomBar block with empty block
target = """        bottomBar = {"""
# Find the end of bottomBar
idx1 = content.find(target)
idx2 = content.find("    ) { padding ->", idx1)

content = content[:idx1] + "        bottomBar = {}\n" + content[idx2:]

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
