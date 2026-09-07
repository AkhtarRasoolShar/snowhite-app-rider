with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("import androidx.compose.runtime.getValue"): continue
    if line.startswith("import androidx.compose.runtime.setValue"): continue
    if line.startswith("import androidx.compose.ui.Modifier"): continue
    new_lines.append(line)

content = "".join(new_lines)
content = content.replace("package com.example", "package com.example\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue\nimport androidx.compose.ui.Modifier\n")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
