with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

old_chat = """data class ChatMessage(
    @SerializedName("id") val id: Int = -1,
    @SerializedName("order_id") val order_id: String? = null,
    @SerializedName("sender_type") val sender_type: String? = null,
    @SerializedName("sender_id") val sender_id: String? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val created_at: String? = null,
    @SerializedName("status") val status: String? = null // e.g., sent, delivered, seen
)"""

new_chat = """data class ChatMessage(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("order_id") val orderId: Int? = null,
    @SerializedName("sender_type") val senderType: String? = null,
    @SerializedName("sender_id") val senderId: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("status") var status: String? = null // e.g., sent, delivered, seen
)"""

main = main.replace(old_chat, new_chat)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)


with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chatui = f.read()

chatui = chatui.replace("""                            val tempMsg = ChatMessage(
                                id = -1, order_id = orderId.toString(), sender_type = mySenderType,
                                sender_id = mySenderId.toString(), message = msg, status = "Sending"
                            )""", """                            val tempMsg = ChatMessage(
                                id = -1, orderId = orderId, senderType = mySenderType,
                                senderId = mySenderId, message = msg, status = "Sending"
                            )""")

chatui = chatui.replace("""val isMine = msg.sender_type == mySenderType && msg.sender_id == mySenderId.toString()""", 
"""val isMine = msg.senderType == mySenderType && msg.senderId == mySenderId""")

# The catch block already logs using android.util.Log.e("ChatUI", "Failed to send message", e).
# I'll update it to use the exact log the user requested:
chatui = chatui.replace("""                                } catch (e: Exception) {
                                    android.util.Log.e("ChatUI", "Failed to send message", e)""",
"""                                } catch (e: Exception) {
                                    android.util.Log.e("CHAT_ERROR", "Failed to send", e)""")


with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chatui)

