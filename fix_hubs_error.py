with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Add errorMessage variable to RiderViewModel
content = content.replace('var availableHubs by androidx.compose.runtime.mutableStateOf<List<Hub>>(emptyList())', 'var errorMessage by androidx.compose.runtime.mutableStateOf<String?>(null)\n    var availableHubs by androidx.compose.runtime.mutableStateOf<List<Hub>>(emptyList())')

old_func = r'''    fun fetchHubs\(\) \{
        viewModelScope\.launch \{
            try \{
                val response = RetrofitClient\.apiService\.getHubs\(\)
                if \(response\.isSuccessful\) \{
                    val body = response\.body\(\)
                    if \(body\?\.status == "success" && body\.data != null\) \{
                        availableHubs = body\.data
                        return@launch
                    \}
                \}
            \} catch \(e: Exception\) \{
                e\.printStackTrace\(\)
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
        viewModelScope.launch {
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
        }
    }'''

content = re.sub(old_func, new_func, content, flags=re.DOTALL)

# Add errorMessage display to UI
old_ui = r'''                        Text\("Select Active Hubs:", fontWeight = FontWeight\.Bold, color = DarkBlue, modifier = Modifier\.fillMaxWidth\(\), textAlign = TextAlign\.Start\)'''
new_ui = '''                        viewModel.errorMessage?.let {
                            PersistentErrorBanner(it)
                            Spacer(Modifier.height(8.dp))
                        }
                        Text("Select Active Hubs:", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)'''

content = re.sub(old_ui, new_ui, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
