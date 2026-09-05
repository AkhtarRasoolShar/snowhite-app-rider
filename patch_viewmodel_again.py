import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will just write a specific patch for fetchAvailableOrders, fetchMyOrders, acceptOrder, rejectOrder, login, register, updateProfile, updateOrderStatus

content = re.sub(
r'(\s*)viewModelScope\.launch\s*\{([\s\S]*?)_isLoading\.value = true\s*try \{([\s\S]*?)\} catch \(e: Exception\) \{([\s\S]*?)\} finally \{([\s\S]*?)\}',
r'\1viewModelScope.launch {\n\1    try {\n\1        _isLoading.value = true\3    } catch (e: Exception) {\n\1        android.util.Log.e("API_ERROR", "Fetch failed", e)\4    } finally {\n\1        _isLoading.value = false\n\1    }',
content)

content = re.sub(
r'(\s*)viewModelScope\.launch\s*\{\s*try \{([\s\S]*?)val response = RetrofitClient.apiService.updateOrderStatus([\s\S]*?)\} catch \(e: Exception\) \{([\s\S]*?)\}',
r'\1viewModelScope.launch {\n\1    try {\n\1        _isLoading.value = true\2val response = RetrofitClient.apiService.updateOrderStatus\3    } catch (e: Exception) {\n\1        android.util.Log.e("API_ERROR", "Fetch failed", e)\4    } finally {\n\1        _isLoading.value = false\n\1    }',
content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

