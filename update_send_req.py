with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

main = main.replace("data class ChatSendRequest(", "data class SendMessageRequest(")
main = main.replace("sendChatMessage(@Body request: ChatSendRequest): retrofit2.Response<GenericResponse<Unit>>", "sendChatMessage(@Body request: SendMessageRequest): retrofit2.Response<GenericResponse<Any>>")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)

with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chat = f.read()

chat = chat.replace("ChatSendRequest(", "SendMessageRequest(")

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chat)

