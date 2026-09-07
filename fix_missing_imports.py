with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import com.google.gson.GsonBuilder
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.*
import androidx.compose.ui.window.*
import androidx.compose.foundation.interaction.*
"""

content = content.replace("package com.example\n", "package com.example\n" + imports)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
