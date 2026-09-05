import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

target = """                val jsonObject = org.json.JSONObject()
                jsonObject.put("order_id", orderId)
                jsonObject.put("sender_type", senderType)
                jsonObject.put("sender_id", senderId)
                jsonObject.put("message", message)
                
                val rawJsonString = jsonObject.toString()"""

replacement = """                val requestObj = SendMessageRequest(orderId, senderType, senderId, message)
                val rawJsonString = com.google.gson.Gson().toJson(requestObj)"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
        f.write(content)
    print("Patched ChatViewModel.kt")
else:
    print("Target not found in ChatViewModel.kt")
