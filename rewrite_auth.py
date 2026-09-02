import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update RiderApiService
api_old = """    @POST("routes.php?action=login")
    suspend fun login(@Body request: RiderLoginRequest): Response<GenericResponse<RiderAuthData>>"""
api_new = """    @Headers("Cache-Control: no-cache")
    @POST("routes.php?action=login")
    suspend fun login(@Body request: RiderLoginRequest): Response<GenericResponse<RiderAuthData>>"""
content = content.replace(api_old, api_new)

# 2. Add SessionManager
if 'object SessionManager' not in content:
    session_manager = """
object SessionManager {
    fun saveUser(context: Context, data: RiderAuthData) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putInt("rider_id", data.id)
            putString("rider_name", data.name)
            putString("rider_phone", data.phone)
            putString("rider_zones", data.service_zone ?: "")
        }.apply()
    }

    fun logout(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().clear().apply()
    }
}
"""
    # Insert before RiderViewModel
    content = content.replace("class RiderViewModel : ViewModel() {", session_manager + "\nclass RiderViewModel : ViewModel() {")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
