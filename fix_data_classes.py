with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if "import com.google.gson.annotations.SerializedName" not in content:
    content = content.replace("import com.google.gson.GsonBuilder", "import com.google.gson.GsonBuilder\nimport com.google.gson.annotations.SerializedName")

old_rider = """data class RiderOrder(
    @com.google.gson.annotations.SerializedName("order_id") val order_id: Int? = null,
    @com.google.gson.annotations.SerializedName("pickup_address") val pickup_address: String? = null,
    @com.google.gson.annotations.SerializedName("total_amount") val total_amount: String? = null,
    @com.google.gson.annotations.SerializedName("date") val date: String? = null,
    @com.google.gson.annotations.SerializedName("status") val status: String? = null,
    @com.google.gson.annotations.SerializedName("items") val items: List<CartItem>? = null
)"""

new_rider = """data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<CartItem>? = null
)"""

content = content.replace(old_rider, new_rider)

old_cart = """data class CartItem(
    @com.google.gson.annotations.SerializedName("name") val name: String? = null,
    @com.google.gson.annotations.SerializedName("quantity") val quantity: Int? = null
)"""

new_cart = """data class CartItem(
    @SerializedName("name") val name: String? = null,
    @SerializedName("quantity") val quantity: Int? = null
)"""

content = content.replace(old_cart, new_cart)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
