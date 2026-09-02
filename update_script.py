import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update Colors
content = content.replace("Color(0xFF0F172A)", "Color(0xFF03045E)") # DarkBlue
content = content.replace("Color(0xFF14B8A6)", "Color(0xFF00B4D8)") # TealAccent

# 2. Update Data Class
old_data_class = """data class RiderOrderResponse(
    val order_id: String,
    val address: String?,
    val total_amount: String?,
    val status: String?,
    @com.google.gson.annotations.SerializedName("items") val items: List<CartItem>? = null
)"""

new_data_class = """data class RiderOrder(
    val order_id: Int?,
    val pickup_address: String?,
    val total_amount: String?,
    val date: String?,
    val status: String?,
    @com.google.gson.annotations.SerializedName("items") val items: List<CartItem>? = null
)"""
content = content.replace(old_data_class, new_data_class)

# 3. Rename everywhere
content = content.replace("RiderOrderResponse", "RiderOrder")
content = content.replace("order.address", "order.pickup_address")
content = content.replace("order_id = it.order_id", "order_id = it.order_id.toString()")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
