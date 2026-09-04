with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_order = """data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<CartItem>? = null
)"""

new_order = """data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<CartItem>? = null,
    @SerializedName("zone") val zone: String? = null,
    var distanceInMeters: Float? = null
)"""

content = content.replace(old_order, new_order)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
