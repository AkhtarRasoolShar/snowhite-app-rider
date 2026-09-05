import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

# Fix the broken import at the very beginning
if content.startswith("import okhttp3.MediaType.Companion.toMediaTypeOrNull\nimport okhttp3.RequestBody.Companion.toRequestBody\npackage com.example"):
    content = content.replace(
        "import okhttp3.MediaType.Companion.toMediaTypeOrNull\nimport okhttp3.RequestBody.Companion.toRequestBody\npackage com.example",
        "package com.example\n\nimport okhttp3.MediaType.Companion.toMediaTypeOrNull\nimport okhttp3.RequestBody.Companion.toRequestBody\n"
    )
elif content.startswith("import "):
    # Generally fix if it starts with import but has package later
    match = re.search(r"^(.*?)(package com.example.*?)$", content, re.DOTALL)
    if match:
        imports = match.group(1)
        rest = match.group(2)
        content = rest.replace("package com.example", "package com.example\n" + imports)

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(content)
