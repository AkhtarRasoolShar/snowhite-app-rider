import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Update ViewModel State
if "_whatsappNumber" not in content:
    content = content.replace(
        "val riderPhone = _riderPhone.asStateFlow()",
        "val riderPhone = _riderPhone.asStateFlow()\n    private val _whatsappNumber = MutableStateFlow(\"\")\n    val whatsappNumber = _whatsappNumber.asStateFlow()"
    )

# Update initSession
if "prefs.getString(\"whatsapp_number\"" not in content:
    content = content.replace(
        "_riderPhone.value = prefs.getString(\"rider_phone\", \"\") ?: \"\"",
        "_riderPhone.value = prefs.getString(\"rider_phone\", \"\") ?: \"\"\n        _whatsappNumber.value = prefs.getString(\"whatsapp_number\", \"\") ?: \"\""
    )

# Update saveAuthData
if "putString(\"whatsapp_number\"" not in content:
    content = content.replace(
        "putString(\"rider_phone\", data.phone)",
        "putString(\"rider_phone\", data.phone)\n            putString(\"whatsapp_number\", data.whatsapp_number ?: \"\")"
    )

# Add updateWhatsApp method to ViewModel
if "fun updateWhatsApp" not in content:
    update_whatsapp_code = """
    fun updateWhatsApp(context: Context, whatsapp: String) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val request = mapOf("rider_id" to id.toString(), "whatsapp_number" to whatsapp)
                val response = RetrofitClient.apiService.updateProfile(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
                    prefs.edit().putString("whatsapp_number", whatsapp).apply()
                    _whatsappNumber.value = whatsapp
                    Toast.makeText(context, "Profile Updated!", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update profile", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }
"""
    content = content.replace("fun clearError() {", update_whatsapp_code + "\n    fun clearError() {")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
