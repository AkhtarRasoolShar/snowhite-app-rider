for act in get_chat send_chat fetch_chat chat send_message get_messages chat_messages order_chat get_order_chat send_order_chat send_msg get_msg; do
    res=$(curl -s "https://snow.akfasft.com/api/routes.php?action=$act")
    if [[ "$res" != *"Invalid endpoint"* ]]; then
        echo "FOUND ACTION: $act - Response: $res"
    fi
done
