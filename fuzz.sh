#!/bin/bash
actions=(
  "get_chat" "get_chats" "chat" "chats"
  "get_messages" "get_message" "messages" "message"
  "fetch_messages" "fetch_chat"
  "get_order_chat" "get_order_messages"
  "order_chat" "order_messages"
  "chat_messages" "get_chat_messages"
  "send_message" "send_chat" "send_chat_message" "add_message" "add_chat_message"
  "insert_message" "insert_chat"
  "rider_chat" "rider_messages"
)
for act in "${actions[@]}"; do
    res=$(curl -s "https://snow.akfasft.com/api/routes.php?action=$act")
    if [[ "$res" != *"Invalid endpoint"* && -n "$res" && "$res" != *"<html"* ]]; then
        echo "FOUND: $act -> $res"
    fi
done
