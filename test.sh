#!/bin/bash
for act in rider_send_message rider_get_messages get_order_chat_messages send_order_chat_message get_messages send_message chat_messages chat_send_message; do
    res=$(curl -s "https://snow.akfasft.com/api/routes.php?action=$act")
    if [[ "$res" != *"Invalid endpoint"* ]]; then
        echo "FOUND ACTION: $act - Response: $res"
    fi
done
