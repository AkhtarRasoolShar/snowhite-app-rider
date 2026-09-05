import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

# Revert RiderAuthData id back to Int! It's much simpler.
main = main.replace('@SerializedName("id") val id: String? = null,', '@SerializedName("id") val id: Int = -1,')

# Wait, if id is Int, putString("rider_id", data.id ?: "") is invalid.
main = main.replace('putString("rider_id", data.id ?: "")', 'putInt("rider_id", data.id)')
main = main.replace('putString("rider_id", data.id.toString())', 'putInt("rider_id", data.id)')
main = main.replace('val rId = prefs.getString("rider_id", "-1") ?: "-1"\n        _riderId.value = rId.toIntOrNull() ?: -1', '_riderId.value = prefs.getInt("rider_id", -1)')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)

with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chat = f.read()

# Fix ChatUI.kt msg.sender_id
chat = chat.replace('msg.sender_id == mySenderId', 'msg.sender_id == mySenderId.toString()')

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chat)

