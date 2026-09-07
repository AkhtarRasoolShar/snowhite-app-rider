with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re
old_func = r'''    private fun fetchHubs\(\) \{
        viewModelScope\.launch\(Dispatchers\.IO\) \{
            try \{
                val response = RetrofitClient\.apiService\.getHubs\(\)
                if \(response\.isSuccessful\) \{
                    val data = response\.body\(\)\?\.data
                    if \(data != null\) \{
                        availableHubs = data
                    \}
                \}
            \} catch \(e: Exception\) \{
                android\.util\.Log\.e\("API_ERROR", "Failed to fetch hubs", e\)
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
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }'''

content = re.sub(old_func, new_func, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
