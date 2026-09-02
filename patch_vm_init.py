import re
with open("/app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt", "r") as f:
    content = f.read()

# Replace repository and stateflow initializations
old_init = """    private val repository = LaundryRepository(
        RetrofitClient.apiService,
        application.getSharedPreferences("CustomerPrefs", Context.MODE_PRIVATE)
    )

    private val _isLoggedIn = MutableStateFlow(repository.isLoggedIn())
    val isLoggedIn = _isLoggedIn.asStateFlow()

    private val _customerName = MutableStateFlow(repository.getCustomerName())
    val customerName = _customerName.asStateFlow()

    private val _customerPhone = MutableStateFlow(repository.getCustomerPhone())
    val customerPhone = _customerPhone.asStateFlow()"""

new_init = """    private val repository by lazy {
        LaundryRepository(
            RetrofitClient.apiService,
            application.getSharedPreferences("CustomerPrefs", Context.MODE_PRIVATE)
        )
    }

    private val _isLoggedIn = MutableStateFlow(false)
    val isLoggedIn = _isLoggedIn.asStateFlow()

    private val _customerName = MutableStateFlow("Guest")
    val customerName = _customerName.asStateFlow()

    private val _customerPhone = MutableStateFlow("")
    val customerPhone = _customerPhone.asStateFlow()

    init {
        viewModelScope.launch {
            try {
                _isLoggedIn.value = repository.isLoggedIn()
                _customerName.value = repository.getCustomerName()
                _customerPhone.value = repository.getCustomerPhone()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

content = content.replace(old_init, new_init)

with open("/app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt", "w") as f:
    f.write(content)
