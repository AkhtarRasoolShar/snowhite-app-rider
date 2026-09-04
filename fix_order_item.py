import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Rename CartItem to OrderItem and define it exactly as user asked
old_cart_item = """data class CartItem(
    @SerializedName("name") val name: String? = null,
    @SerializedName("quantity") val quantity: Int? = null
)"""

new_order_item = """data class OrderItem(
    @SerializedName("name") val name: String? = null,
    @SerializedName("quantity") val quantity: Int? = null
)"""

if old_cart_item in content:
    content = content.replace(old_cart_item, new_order_item)
else:
    # Fallback if there's subtle differences
    content = re.sub(r'data class CartItem\([\s\S]*?\)', new_order_item, content)

# 2. Update RiderOrder to use List<OrderItem> instead of List<CartItem>
content = content.replace('val items: List<CartItem>?', 'val items: List<OrderItem>?')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
