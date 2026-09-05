with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chatui = f.read()

chatui = chatui.replace("text = msg.status,", "text = msg.status ?: \"\",")

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chatui)

with open('app/src/main/java/com/example/ChatWorker.kt', 'r') as f:
    worker = f.read()

worker = worker.replace("msg.sender_type", "msg.senderType")
worker = worker.replace("msg.order_id", "msg.orderId")

with open('app/src/main/java/com/example/ChatWorker.kt', 'w') as f:
    f.write(worker)

