with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Add isFetchingHubs to RiderViewModel
content = content.replace('var errorMessage by androidx.compose.runtime.mutableStateOf<String?>(null)', 'var isFetchingHubs by androidx.compose.runtime.mutableStateOf(false)\n    var errorMessage by androidx.compose.runtime.mutableStateOf<String?>(null)')

old_func = r'''    fun fetchHubs\(\) \{
        viewModelScope\.launch \{
            try \{
                val response = RetrofitClient\.apiService\.getHubs\(\)
                if \(response\.isSuccessful\) \{
                    val body = response\.body\(\)
                    if \(body\?\.status == "success" && body\.data != null\) \{
                        availableHubs = body\.data
                        errorMessage = null
                        return@launch
                    \} else \{
                        errorMessage = body\?\.message \?: "Failed to fetch hubs\."
                    \}
                \} else \{
                    errorMessage = "Server Error: \$\{response\.code\(\)\}"
                \}
            \} catch \(e: Exception\) \{
                e\.printStackTrace\(\)
                errorMessage = "Network Error: Could not connect to server\."
            \}
            
            // Fallback in case of HTTP 500 or Network Error
            availableHubs = listOf\(
                Hub\(1, "Clifton"\),
                Hub\(2, "Tariq Road"\),
                Hub\(3, "DHA"\),
                Hub\(4, "Gulshan"\)
            \)
        \}
    \}'''

new_func = '''    fun fetchHubs() {
        isFetchingHubs = true
        viewModelScope.launch {
            try {
                try {
                    val response = RetrofitClient.apiService.getHubs()
                    if (response.isSuccessful) {
                        val body = response.body()
                        if (body?.status == "success" && body.data != null) {
                            availableHubs = body.data
                            errorMessage = null
                            return@launch
                        } else {
                            errorMessage = body?.message ?: "Failed to fetch hubs."
                        }
                    } else {
                        errorMessage = "Server Error: ${response.code()}"
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                    errorMessage = "Network Error: Could not connect to server."
                }
                
                // Fallback in case of HTTP 500 or Network Error
                availableHubs = listOf(
                    Hub(1, "Clifton"),
                    Hub(2, "Tariq Road"),
                    Hub(3, "DHA"),
                    Hub(4, "Gulshan")
                )
            } finally {
                isFetchingHubs = false
            }
        }
    }'''

content = re.sub(old_func, new_func, content, flags=re.DOTALL)

old_ui = r'''                        Text\("Select Active Hubs:", fontWeight = FontWeight\.Bold, color = DarkBlue, modifier = Modifier\.fillMaxWidth\(\), textAlign = TextAlign\.Start\)
                        
                        viewModel\.availableHubs\.forEach \{ hub ->'''

new_ui = '''                        Text("Select Active Hubs:", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
                        
                        if (viewModel.isFetchingHubs) {
                            Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                                CircularProgressIndicator(color = TealAccent)
                            }
                        } else {
                        viewModel.availableHubs.forEach { hub ->'''

content = re.sub(old_ui, new_ui, content, flags=re.DOTALL)

# Also close the `else {` block we opened in the UI.
old_ui_close = r'''                                Text\(hubName, color = DarkBlue\)
                            \}
                        \}
                        
                        Spacer\(Modifier\.height\(24\.dp\)\)'''

new_ui_close = '''                                Text(hubName, color = DarkBlue)
                            }
                        }
                        }
                        
                        Spacer(Modifier.height(24.dp))'''

content = re.sub(old_ui_close, new_ui_close, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

