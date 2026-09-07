with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace RiderRegisterRequest
old_request = 'data class RiderRegisterRequest(@SerializedName("name") val name: String? = null, @SerializedName("phone") val phone: String? = null, val password: String, @SerializedName("service_zone") val service_zone: String? = null)'
new_request = '''data class RiderRegisterRequest(
    @SerializedName("name") val name: String? = null,
    @SerializedName("phone") val phone: String? = null,
    val password: String,
    @SerializedName("service_zone") val service_zone: List<String>? = null,
    @SerializedName("email") val email: String? = null
)'''
content = content.replace(old_request, new_request)

# Add new data classes right after RiderRegisterRequest
if "data class Hub" not in content:
    new_classes = '''
data class Hub(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("name") val name: String? = null
)

data class AppSettings(
    val app_name: String? = null,
    val logo_url: String? = null
)
'''
    content = content.replace(new_request, new_request + new_classes)

# Add getHubs to RiderApiService
api_insertion = '''    @GET("routes.php?action=get_available_orders")'''
new_api = '''    @GET("routes.php?action=get_hubs")
    suspend fun getHubs(): Response<GenericResponse<List<Hub>>>

    @GET("routes.php?action=get_available_orders")'''
if "get_hubs" not in content:
    content = content.replace(api_insertion, new_api)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
