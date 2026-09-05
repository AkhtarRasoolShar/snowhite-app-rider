import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

sealed_class = """    sealed class PendingAction {
        data class AcceptOrder(val orderId: String) : PendingAction()
        data class RejectOrder(val orderId: String) : PendingAction()
        data class UpdateOrderStatus(val orderId: String, val newStatus: String) : PendingAction()
    }
    
    private val pendingActions"""

content = content.replace('    private val pendingActions', sealed_class)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
