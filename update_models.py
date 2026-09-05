with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_order = """data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = null,
    @SerializedName("zone") val zone: String? = null,
    @SerializedName("customer_name") val customer_name: String? = null,
    @SerializedName("customer_phone") val customer_phone: String? = null,
    var distanceInMeters: Float? = null
)"""

new_order = """data class RiderOrder(
    @SerializedName("order_id") val orderId: Int? = null,
    @SerializedName("pickup_address") val pickupAddress: String? = null,
    @SerializedName("total_amount") val totalAmount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = emptyList(),
    @SerializedName("zone") val zone: String? = null,
    @SerializedName("customer_name") val customerName: String? = null,
    @SerializedName("customer_phone") val customerPhone: String? = null,
    var distanceInMeters: Float? = null
)"""

content = content.replace(old_order, new_order)
content = content.replace('order.order_id', 'order.orderId')
content = content.replace('it.order_id', 'it.orderId')
content = content.replace('order.total_amount', 'order.totalAmount')
content = content.replace('order.pickup_address', 'order.pickupAddress')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/RiderUI.kt', 'r') as f:
    ui_content = f.read()

ui_content = ui_content.replace('order.order_id', 'order.orderId')
ui_content = ui_content.replace('order.total_amount', 'order.totalAmount')
ui_content = ui_content.replace('order.pickup_address', 'order.pickupAddress')
ui_content = ui_content.replace('order.customer_name', 'order.customerName')
ui_content = ui_content.replace('order.customer_phone', 'order.customerPhone')

with open('app/src/main/java/com/example/RiderUI.kt', 'w') as f:
    f.write(ui_content)
