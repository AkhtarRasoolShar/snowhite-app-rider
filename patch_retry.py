import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Add PendingAction class
pending_action_code = """
    sealed class PendingAction {
        data class AcceptOrder(val orderId: String) : PendingAction()
        data class RejectOrder(val orderId: Int) : PendingAction()
        data class UpdateOrderStatus(val orderId: String, val newStatus: String) : PendingAction()
    }

    private val pendingActions = mutableListOf<PendingAction>()
    
    fun retryPendingActions(context: android.content.Context) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.Main) {
            if (pendingActions.isNotEmpty()) {
                android.widget.Toast.makeText(context, "Network Restored. Retrying pending actions...", android.widget.Toast.LENGTH_SHORT).show()
                val actionsToRetry = pendingActions.toList()
                pendingActions.clear()
                actionsToRetry.forEach { action ->
                    when (action) {
                        is PendingAction.AcceptOrder -> acceptOrder(action.orderId, context)
                        is PendingAction.RejectOrder -> rejectOrder(action.orderId, context)
                        is PendingAction.UpdateOrderStatus -> updateOrderStatus(action.orderId, action.newStatus, context)
                    }
                }
            }
            fetchAvailableOrders(context)
            fetchMyOrders(context)
        }
    }
"""

if "sealed class PendingAction" not in content:
    content = content.replace("class RiderViewModel : ViewModel() {\n", "class RiderViewModel : ViewModel() {\n" + pending_action_code)

# 2. Update initSession
old_init_session = """    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: ""
        _bankName.value = prefs.getString("bank_name", "") ?: ""
        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
        _quickReply1.value = prefs.getString("quick_reply_1", "I am on my way!") ?: "I am on my way!"
        _quickReply2.value = prefs.getString("quick_reply_2", "I have arrived at the pickup location.") ?: "I have arrived at the pickup location."
    }"""

new_init_session = """    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: ""
        _bankName.value = prefs.getString("bank_name", "") ?: ""
        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
        _quickReply1.value = prefs.getString("quick_reply_1", "I am on my way!") ?: "I am on my way!"
        _quickReply2.value = prefs.getString("quick_reply_2", "I have arrived at the pickup location.") ?: "I have arrived at the pickup location."
        
        try {
            val connectivityManager = context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
            val request = android.net.NetworkRequest.Builder()
                .addCapability(android.net.NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .build()
            connectivityManager.registerNetworkCallback(request, object : android.net.ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: android.net.Network) {
                    retryPendingActions(context)
                }
            })
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }"""

content = content.replace(old_init_session, new_init_session)

# We use regex to carefully replace the catch blocks for specific methods
# For acceptOrder
content = re.sub(
    r'(fun acceptOrder\(.*?\}\s*catch\s*\(e:\s*Exception\)\s*\{\s*)(Toast\.makeText\(context,\s*"Network Error",\s*Toast\.LENGTH_SHORT\)\.show\(\))',
    r'\1Toast.makeText(context, "Network Error. Order acceptance queued.", Toast.LENGTH_SHORT).show()\n                val action = PendingAction.AcceptOrder(orderId)\n                if (!pendingActions.contains(action)) pendingActions.add(action)',
    content,
    flags=re.DOTALL
)

# For rejectOrder
content = re.sub(
    r'(fun rejectOrder\(.*?\}\s*catch\s*\(e:\s*Exception\)\s*\{\s*)(Toast\.makeText\(context,\s*"Network Error",\s*Toast\.LENGTH_SHORT\)\.show\(\))',
    r'\1Toast.makeText(context, "Network Error. Order rejection queued.", Toast.LENGTH_SHORT).show()\n                val action = PendingAction.RejectOrder(orderId)\n                if (!pendingActions.contains(action)) pendingActions.add(action)',
    content,
    flags=re.DOTALL
)

# For updateOrderStatus
content = re.sub(
    r'(fun updateOrderStatus\(.*?\}\s*catch\s*\(e:\s*Exception\)\s*\{\s*)(Toast\.makeText\(context,\s*"Network Error",\s*Toast\.LENGTH_SHORT\)\.show\(\))',
    r'\1Toast.makeText(context, "Network Error. Status update queued.", Toast.LENGTH_SHORT).show()\n                val action = PendingAction.UpdateOrderStatus(orderId, newStatus)\n                if (!pendingActions.contains(action)) pendingActions.add(action)',
    content,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

