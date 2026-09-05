with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace('    @POST("routes.php?action=update_order_status")\n    \n    @GET("routes.php?action=get_chat_messages")', '    @GET("routes.php?action=get_chat_messages")')
content = content.replace('    @POST("routes.php?action=send_chat_message")\n    \n    @GET("routes.php?action=get_typing_status")', '    @GET("routes.php?action=get_typing_status")')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
