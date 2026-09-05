import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("package com.exampleimport", "package com.example\nimport")
content = content.replace("toMediaTypeOrNullimport", "toMediaTypeOrNull\nimport")
content = content.replace("toRequestBodyimport", "toRequestBody\nimport")

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(content)
