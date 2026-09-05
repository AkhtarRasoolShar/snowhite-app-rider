with open('app/src/main/java/com/example/ChatUI.kt', 'r') as f:
    chat = f.read()

chat = chat.replace('id = -1, order_id = orderId, sender_type = mySenderType,\n                                sender_id = mySenderId,', 'id = "-1", order_id = orderId.toString(), sender_type = mySenderType,\n                                sender_id = mySenderId.toString(),')

chat = chat.replace('it.sender_id == mySenderId', 'it.sender_id == mySenderId.toString()')

with open('app/src/main/java/com/example/ChatUI.kt', 'w') as f:
    f.write(chat)

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

main = main.replace('fun fetchOrders(riderId: String)', 'fun fetchOrders(riderId: Int)')
main = main.replace('fetchOrders(authData.id?.toIntOrNull() ?: 0)', 'fetchOrders(authData.id?.toIntOrNull() ?: 0)')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)

