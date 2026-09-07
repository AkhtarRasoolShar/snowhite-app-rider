with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

old_func = r'''    fun fetchHubs\(\) \{
        viewModelScope\.launch \{
            try \{
                val response = RetrofitClient\.apiService\.getHubs\(\)
                if \(response\.isSuccessful\) \{
                    val body = response\.body\(\)
                    if \(body\?\.status == "success" && body\.data != null\) \{
                        availableHubs = body\.data
                    \}
                \}
            \} catch \(e: Exception\) \{
                e\.printStackTrace\(\)
            \}
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
                        return@launch
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
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

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
