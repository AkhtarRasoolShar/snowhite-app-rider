import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I see `dge(status: String) {` in the compiler error. Let's fix that.
content = content.replace("dge(status: String) {", "fun StatusBadge(status: String) {")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
