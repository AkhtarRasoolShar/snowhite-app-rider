import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

target = """                val requestBody = okhttp3.RequestBody.create(okhttp3.MediaType.parse("application/json; charset=utf-8"), rawJsonString)"""
replacement = """                val mediaType = okhttp3.MediaType.parse("application/json; charset=utf-8")
                val requestBody = okhttp3.RequestBody.create(mediaType, rawJsonString)"""
                
# Actually, the extension function is better
replacement2 = """                val mediaType = "application/json; charset=utf-8".let { okhttp3.MediaType.parse(it) } // Still deprecated but sometimes allowed? 
                """

# Let's import the extension functions and use them
if "import okhttp3.MediaType.Companion.toMediaTypeOrNull" not in content:
    content = "import okhttp3.MediaType.Companion.toMediaTypeOrNull\nimport okhttp3.RequestBody.Companion.toRequestBody\n" + content

target_ext = """                val requestBody = okhttp3.RequestBody.create(okhttp3.MediaType.parse("application/json; charset=utf-8"), rawJsonString)"""
replacement_ext = """                val mediaType = "application/json; charset=utf-8".toMediaTypeOrNull()
                val requestBody = rawJsonString.toRequestBody(mediaType)"""

content = content.replace(target_ext, replacement_ext)

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(content)
