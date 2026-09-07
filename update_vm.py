with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Add state variables inside RiderViewModel
vm_start = content.find("class RiderViewModel : ViewModel() {")
if vm_start != -1:
    insertion_point = content.find("\n", vm_start) + 1
    new_vars = '''
    var email by androidx.compose.runtime.mutableStateOf("")
    var availableHubs by androidx.compose.runtime.mutableStateOf<List<Hub>>(emptyList())
    var selectedHubs by androidx.compose.runtime.mutableStateOf<Set<String>>(emptySet())
    var appSettings by androidx.compose.runtime.mutableStateOf(AppSettings())

    init {
        fetchHubs()
    }

    private fun fetchHubs() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val response = RetrofitClient.apiService.getHubs()
                if (response.isSuccessful) {
                    val data = response.body()?.data
                    if (data != null) {
                        availableHubs = data
                    }
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Failed to fetch hubs", e)
            }
        }
    }
'''
    if "var availableHubs by" not in content:
        content = content[:insertion_point] + new_vars + content[insertion_point:]

# Update the register function in RiderViewModel
# The old signature: fun register(name: String, phone: String, pass: String, zone: String, context: Context)
old_register_regex = r'fun register\(name: String, phone: String, pass: String, zone: String, context: Context\) \{.*?(?=fun fetchAvailableOrders)'
new_register_str = '''fun register(name: String, phone: String, pass: String, zones: List<String>, email: String, context: Context) {
        viewModelScope.launch {
            _authError.value = null
            _pendingApproval.value = false
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.register(RiderRegisterRequest(name, phone, pass, zones, email))
                if (response.isSuccessful) {
                    val body = response.body()
                    if (body?.status == "success" && body.data != null) {
                        _pendingApproval.value = true
                        _authError.value = "Registration Successful. Awaiting Admin Approval."
                    } else {
                        _authError.value = body?.message ?: "Registration Failed."
                    }
                } else {
                    _authError.value = "Server error. Try again."
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                _authError.value = "Network Error. Please check connection."
            } finally {
                _isLoading.value = false
            }
        }
    }

    '''
content = re.sub(old_register_regex, new_register_str, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
