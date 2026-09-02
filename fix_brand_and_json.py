import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update Brand Name
content = content.replace("SnowWhite", "Snowhite")

# 2. Update Data Classes
old_rider_order = """data class RiderOrder(
    val order_id: Int?,
    val pickup_address: String?,
    val total_amount: String?,
    val date: String?,
    val status: String?,
    @com.google.gson.annotations.SerializedName("items") val items: List<CartItem>? = null
)"""

new_rider_order = """data class RiderOrder(
    @com.google.gson.annotations.SerializedName("order_id") val order_id: Int? = null,
    @com.google.gson.annotations.SerializedName("pickup_address") val pickup_address: String? = null,
    @com.google.gson.annotations.SerializedName("total_amount") val total_amount: String? = null,
    @com.google.gson.annotations.SerializedName("date") val date: String? = null,
    @com.google.gson.annotations.SerializedName("status") val status: String? = null,
    @com.google.gson.annotations.SerializedName("items") val items: List<CartItem>? = null
)"""

content = content.replace(old_rider_order, new_rider_order)

old_cart_item = "data class CartItem(val name: String?, val quantity: Int?)"
new_cart_item = """data class CartItem(
    @com.google.gson.annotations.SerializedName("name") val name: String? = null,
    @com.google.gson.annotations.SerializedName("quantity") val quantity: Int? = null
)"""

content = content.replace(old_cart_item, new_cart_item)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

