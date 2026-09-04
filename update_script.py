import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Update RiderAuthData
if "val whatsapp_number: String? = null" not in content:
    content = content.replace(
        "val status: String\n)",
        "val status: String,\n    val whatsapp_number: String? = null\n)"
    )

# Update RiderApiService
if "routes.php?action=update_rider_profile" not in content:
    content = content.replace(
        "suspend fun getRiderOrders(@Query(\"rider_id\") riderId: Int): Response<GenericResponse<List<RiderOrder>>>",
        "suspend fun getRiderOrders(@Query(\"rider_id\") riderId: Int): Response<GenericResponse<List<RiderOrder>>>\n\n    @POST(\"routes.php?action=update_rider_profile\")\n    suspend fun updateProfile(@Body request: Map<String, String>): Response<GenericResponse<Unit>>"
    )

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
