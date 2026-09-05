with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix updateProfile (lines 333-335)
bad_update_profile = """                Toast.makeText(context, "Network Error. Order acceptance queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.AcceptOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)"""
good_update_profile = """                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()"""
content = content.replace(bad_update_profile, good_update_profile, 1)

# Fix fetchAvailableOrders (lines 420-422)
bad_fetch = """                Toast.makeText(context, "Network Error. Order rejection queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.RejectOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)"""
good_fetch = """                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()"""
content = content.replace(bad_fetch, good_fetch, 1)

# Fix getRiderOrders (lines 477-479)
bad_get_orders = """                Toast.makeText(context, "Network Error. Status update queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.UpdateOrderStatus(orderId, newStatus)
                if (!pendingActions.contains(action)) pendingActions.add(action)"""
good_get_orders = """                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()"""
content = content.replace(bad_get_orders, good_get_orders, 1)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
