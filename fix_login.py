import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace the login method in RiderViewModel
login_start = content.find('fun login(phone: String, pass: String, context: Context)')
# Find the end of the method
brace_count = 0
in_method = False
login_end = -1
for i in range(login_start, len(content)):
    if content[i] == '{':
        brace_count += 1
        in_method = True
    elif content[i] == '}':
        brace_count -= 1
        if in_method and brace_count == 0:
            login_end = i + 1
            break

new_login = """fun clearError() {
        _authError.value = null
    }

    fun login(phone: String, pass: String, context: Context, onSuccess: () -> Unit) {
        viewModelScope.launch {
            SessionManager.logout(context)
            _riderId.value = -1
            _isLoading.value = true
            _authError.value = null
            try {
                val res = RetrofitClient.apiService.login(RiderLoginRequest(phone, pass))
                Log.d("API_RESPONSE", "Response: $res")
                if (res.isSuccessful) {
                    val body = res.body()
                    Log.d("API_RESPONSE", "Body: $body")
                    if (body?.status == "success" && body.data != null) {
                        SessionManager.saveUser(context, body.data)
                        // Trigger initialization to load the session state in ViewModel
                        initSession(context)
                        onSuccess()
                    } else {
                        _authError.value = body?.message ?: "Unknown error occurred"
                    }
                } else {
                    _authError.value = "Server error. Try again."
                }
            } catch (e: Exception) {
                Log.e("API_ERROR", "Error: ${e.message}")
                _authError.value = "Network Error. Please check connection."
            } finally {
                _isLoading.value = false
            }
        }
    }"""

content = content[:login_start] + new_login + content[login_end:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
