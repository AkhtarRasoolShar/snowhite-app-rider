package com.example
import retrofit2.http.Headers
import android.util.Log
import androidx.navigation.NavController
import androidx.navigation.NavHostController

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.google.gson.GsonBuilder
import com.google.gson.annotations.SerializedName
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query
import java.util.concurrent.TimeUnit

// --- Colors ---
val DarkBlue = Color(0xFF03045E)
val TealAccent = Color(0xFF00B4D8)
val SoftWhite = Color(0xFFF8FAFC)
val ErrorRed = Color(0xFFEF4444)

// --- API Models ---
data class GenericResponse<T>(
    val status: String,
    val message: String,
    val data: T?
)

data class RiderAuthData(
    val id: Int,
    val name: String,
    val phone: String,
    val service_zone: String,
    val status: String
)

data class RiderOrder(
    @SerializedName("order_id") val order_id: Int? = null,
    @SerializedName("pickup_address") val pickup_address: String? = null,
    @SerializedName("total_amount") val total_amount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<CartItem>? = null
)

data class CartItem(
    @SerializedName("name") val name: String? = null,
    @SerializedName("quantity") val quantity: Int? = null
)

data class RiderLoginRequest(val phone: String, val password: String, val is_rider_app: Boolean = true)
data class RiderRegisterRequest(val name: String, val phone: String, val password: String, val service_zone: String)
data class AcceptOrderRequest(val order_id: String, val rider_id: Int)
data class UpdateOrderStatusRequest(val order_id: String, val status: String)

// --- Retrofit Service ---
interface RiderApiService {
    @Headers("Cache-Control: no-cache")
    @POST("routes.php?action=login")
    suspend fun login(@Body request: RiderLoginRequest): Response<GenericResponse<RiderAuthData>>

    @POST("routes.php?action=rider_register")
    suspend fun register(@Body request: RiderRegisterRequest): Response<GenericResponse<RiderAuthData>>

    @GET("routes.php?action=get_available_orders")
    suspend fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: Int): Response<GenericResponse<List<RiderOrder>>>
    
    @POST("routes.php?action=reject_order")
    suspend fun rejectOrder(@Body request: Map<String, Int>): Response<GenericResponse<Unit>>

    @POST("routes.php?action=accept_order")
    suspend fun acceptOrder(@Body request: AcceptOrderRequest): Response<GenericResponse<Unit>>

    @GET("routes.php?action=get_rider_orders")
    suspend fun getRiderOrders(@Query("rider_id") riderId: Int): Response<GenericResponse<List<RiderOrder>>>

    @POST("routes.php?action=update_order_status")
    suspend fun updateOrderStatus(@Body request: UpdateOrderStatusRequest): Response<GenericResponse<Unit>>
}

object RetrofitClient {
    private const val BASE_URL = "https://snow.akfasft.com/api/"
    val gson = GsonBuilder().setLenient().create()
    
    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()
        
    val apiService: RiderApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()
            .create(RiderApiService::class.java)
    }
}

// --- ViewModel ---

object SessionManager {
    fun saveUser(context: Context, data: RiderAuthData) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putInt("rider_id", data.id)
            putString("rider_name", data.name)
            putString("rider_phone", data.phone)
            putString("rider_zones", data.service_zone ?: "")
        }.apply()
    }

    fun logout(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().clear().apply()
    }
}

class RiderViewModel : ViewModel() {
    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _authError = MutableStateFlow<String?>(null)
    val authError = _authError.asStateFlow()
    
    private val _pendingApproval = MutableStateFlow(false)
    val pendingApproval = _pendingApproval.asStateFlow()

    private val _availableOrders = MutableStateFlow<List<RiderOrder>>(emptyList())
    val availableOrders = _availableOrders.asStateFlow()

    private val _myOrders = MutableStateFlow<List<RiderOrder>>(emptyList())
    val myOrders = _myOrders.asStateFlow()

    private val _riderId = MutableStateFlow(-1)
    val riderId = _riderId.asStateFlow()
    private val _riderName = MutableStateFlow("")
    val riderName = _riderName.asStateFlow()
    private val _riderPhone = MutableStateFlow("")
    val riderPhone = _riderPhone.asStateFlow()
    private val _riderZone = MutableStateFlow("")
    val riderZone = _riderZone.asStateFlow()
    
    private val _homeAddress = MutableStateFlow("")
    val homeAddress = _homeAddress.asStateFlow()
    private val _bankName = MutableStateFlow("")
    val bankName = _bankName.asStateFlow()
    private val _bankIban = MutableStateFlow("")
    val bankIban = _bankIban.asStateFlow()

    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: ""
        _bankName.value = prefs.getString("bank_name", "") ?: ""
        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
    }

    private fun saveAuthData(context: Context, data: RiderAuthData) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putInt("rider_id", data.id)
            putString("rider_name", data.name)
            putString("rider_phone", data.phone)
            putString("rider_zones", data.service_zone)
        }.apply()
        initSession(context)
    }
    
    fun saveProfileDetails(context: Context, address: String, bank: String, iban: String) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putString("rider_address", address)
            putString("bank_name", bank)
            putString("bank_iban", iban)
        }.apply()
        initSession(context)
        Toast.makeText(context, "Profile Updated", Toast.LENGTH_SHORT).show()
    }

    fun logout(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().clear().apply()
        _riderId.value = -1
    }

    fun clearError() {
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
    }

    fun register(name: String, phone: String, pass: String, zone: String, context: Context) {
        viewModelScope.launch {
            _isLoading.value = true
            _authError.value = null
            _pendingApproval.value = false
            try {
                val response = RetrofitClient.apiService.register(RiderRegisterRequest(name, phone, pass, zone))
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
                _authError.value = "Network Error. Please check connection."
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun fetchAvailableOrders(context: Context) {
        val zone = _riderZone.value
        val riderId = _riderId.value
        if (zone.isEmpty() || riderId == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.getAvailableOrders(zone, riderId)
                if (response.isSuccessful && response.body()?.status == "success") {
                    _availableOrders.value = response.body()?.data ?: emptyList()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch orders", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun fetchMyOrders(context: Context) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.getRiderOrders(id)
                if (response.isSuccessful && response.body()?.status == "success") {
                    _myOrders.value = response.body()?.data ?: emptyList()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch history", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun acceptOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.acceptOrder(AcceptOrderRequest(orderId, id))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Accepted!", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to accept order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun rejectOrder(orderId: Int, context: Context) {
        val id = _riderId.value
        if (id == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val request = mapOf("order_id" to orderId, "rider_id" to id)
                val response = RetrofitClient.apiService.rejectOrder(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Rejected", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to reject order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun updateOrderStatus(orderId: String, newStatus: String, context: Context) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.apiService.updateOrderStatus(UpdateOrderStatusRequest(orderId, newStatus))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Status updated to $newStatus", Toast.LENGTH_SHORT).show()
                    fetchMyOrders(context) // Refresh
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update status", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            }
        }
    }
}

// --- Theme ---
@Composable
fun RiderTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = lightColorScheme(
            primary = DarkBlue,
            secondary = TealAccent,
            background = SoftWhite,
            surface = Color.White
        ),
        content = content
    )
}

// --- UI Components ---
@Composable
fun SnowhiteLogo(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.LocalLaundryService,
            contentDescription = "SnoWhite Logo",
            tint = Color.White,
            modifier = Modifier.size(40.dp)
        )
        Spacer(Modifier.width(12.dp))
        Text(
            text = "SnoWhite",
            fontSize = 32.sp,
            fontWeight = FontWeight.Black,
            color = Color.White
        )
    }
}

@Composable
fun PersistentErrorBanner(error: String) {
    Surface(color = ErrorRed.copy(alpha = 0.1f), shape = RoundedCornerShape(8.dp), modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
        Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.ErrorOutline, contentDescription = "Error", tint = ErrorRed)
            Spacer(Modifier.width(8.dp))
            Text(error, color = ErrorRed, fontSize = 14.sp, fontWeight = FontWeight.Bold)
        }
    }
}


private var keepAliveWebView: android.webkit.WebView? = null

fun printReceipt(context: Context, order: RiderOrder) {
    val printManager = context.getSystemService(Context.PRINT_SERVICE) as android.print.PrintManager
    val webView = android.webkit.WebView(context)
    keepAliveWebView = webView
    
    val itemsHtml = order.items?.joinToString("") { 
        "<tr><td style='padding:8px; border-bottom:1px solid #ddd;'>${it.name ?: "Item"}</td><td style='padding:8px; border-bottom:1px solid #ddd;'>${it.quantity ?: 1}x</td></tr>"
    } ?: "<tr><td colspan='2'>No items</td></tr>"
    
    val htmlDocument = """
        <html>
        <head>
            <style>
                body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 20px; color: #03045E; }
                .header { text-align: center; margin-bottom: 20px; }
                .title { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
                .subtitle { font-size: 14px; color: #666; margin-bottom: 20px; }
                .details { margin-bottom: 20px; font-size: 16px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th { background-color: #00B4D8; color: white; padding: 10px; text-align: left; }
                .total { font-size: 18px; font-weight: bold; text-align: right; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">Snowhite Captain</div>
                <div class="subtitle">Receipt - Order #${order.order_id ?: "N/A"}</div>
            </div>
            <div class="details">
                <p><strong>Date:</strong> ${order.date ?: "N/A"}</p>
                <p><strong>Address:</strong> ${order.pickup_address ?: "N/A"}</p>
            </div>
            <table>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                </tr>
                $itemsHtml
            </table>
            <div class="total">
                Total: PKR ${order.total_amount ?: "0"}
            </div>
        </body>
        </html>
    """.trimIndent()
    
    webView.webViewClient = object : android.webkit.WebViewClient() {
        override fun onPageFinished(view: android.webkit.WebView, url: String) {
            val printAdapter = view.createPrintDocumentAdapter("Receipt_${order.order_id}")
            printManager.print("Receipt_${order.order_id}", printAdapter, android.print.PrintAttributes.Builder().build())
        }
    }
    
    webView.loadDataWithBaseURL(null, htmlDocument, "text/HTML", "UTF-8", null)
}

// --- Screens ---

@Composable
fun AuthFlow(viewModel: RiderViewModel, navController: NavHostController) {
    var isLogin by remember { mutableStateOf(true) }
    
    if (isLogin) {
        LoginScreen(viewModel, navController, onNavigateToRegister = { isLogin = false })
    } else {
        RegisterScreen(viewModel, onNavigateToLogin = { isLogin = true })
    }
}

@Composable
fun LoginScreen(viewModel: RiderViewModel, navController: NavController, onNavigateToRegister: () -> Unit) {
    val context = LocalContext.current
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080",
            contentDescription = "Laundry Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.65f)))
        
        Column(
            modifier = Modifier.fillMaxSize().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            SnowhiteLogo(modifier = Modifier.height(60.dp).fillMaxWidth())
            Spacer(Modifier.height(16.dp))
            Text("Captain Portal", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color.White)
            Spacer(Modifier.height(32.dp))
            
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(24.dp)) {
                    authError?.let { PersistentErrorBanner(it) }

                    OutlinedTextField(
                        value = phone,
                        onValueChange = { phone = it; viewModel.clearError() },
                        label = { Text("Phone Number") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    Spacer(Modifier.height(16.dp))
                    OutlinedTextField(
                        value = password,
                        onValueChange = { password = it; viewModel.clearError() },
                        label = { Text("Password") },
                        modifier = Modifier.fillMaxWidth(),
                        visualTransformation = PasswordVisualTransformation(),
                        singleLine = true
                    )
                    Spacer(Modifier.height(24.dp))
                    Button(
                        onClick = { viewModel.login(phone, password, context, onSuccess = { navController.navigate("dashboard") { popUpTo(0) } }) },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF03045E)),
                        enabled = !isLoading && phone.isNotBlank() && password.isNotBlank()
                    ) {
                        if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        else Text("LOGIN", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            TextButton(onClick = onNavigateToRegister) {
                Text("New Rider? Apply Here", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterScreen(viewModel: RiderViewModel, onNavigateToLogin: () -> Unit) {
    val context = LocalContext.current
    var name by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var zone by remember { mutableStateOf("") }
    var expandedZone by remember { mutableStateOf(false) }
    
    val zones = listOf("Clifton", "Tariq Road", "DHA", "Gulshan")
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080",
            contentDescription = "Laundry Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.65f)))
        
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            item {
                Spacer(Modifier.height(24.dp))
                SnowhiteLogo(modifier = Modifier.height(50.dp).fillMaxWidth())
                Spacer(Modifier.height(16.dp))
                Text("Captain Portal", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color.White)
                Spacer(Modifier.height(32.dp))
                
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(24.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(24.dp)) {
                        authError?.let { PersistentErrorBanner(it) }
                        
                        OutlinedTextField(
                            value = name,
                            onValueChange = { name = it },
                            label = { Text("Full Name") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(Modifier.height(16.dp))
                        OutlinedTextField(
                            value = phone,
                            onValueChange = { phone = it; viewModel.clearError() },
                            label = { Text("Phone Number") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(Modifier.height(16.dp))
                        OutlinedTextField(
                            value = password,
                            onValueChange = { password = it; viewModel.clearError() },
                            label = { Text("Password") },
                            modifier = Modifier.fillMaxWidth(),
                            visualTransformation = PasswordVisualTransformation()
                        )
                        Spacer(Modifier.height(16.dp))
                        
                        Text("Select Active Hubs:", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
                        var selectedZones by remember { mutableStateOf(setOf<String>()) }
                        zones.forEach { selection ->
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                                Checkbox(
                                    checked = selectedZones.contains(selection),
                                    onCheckedChange = { isChecked ->
                                        selectedZones = if (isChecked) selectedZones + selection else selectedZones - selection
                                    },
                                    colors = CheckboxDefaults.colors(checkedColor = TealAccent)
                                )
                                Text(selection, color = DarkBlue)
                            }
                        }
                        
                        Spacer(Modifier.height(24.dp))
                        val joinedZones = selectedZones.joinToString(", ")
                        Button(
                            onClick = { viewModel.register(name, phone, password, joinedZones, context) },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF03045E)),
                            enabled = !isLoading && name.isNotBlank() && phone.isNotBlank() && password.isNotBlank() && selectedZones.isNotEmpty()
                        ) {
                            if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                            else Text("REGISTER", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
                
                Spacer(Modifier.height(24.dp))
                TextButton(onClick = onNavigateToLogin) {
                    Text("Back to Login", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(24.dp))
            }
        }
    }
}

@Composable
fun MainAppScreen(viewModel: RiderViewModel) {
    val navController = rememberNavController()
    Scaffold(
        bottomBar = {
            NavigationBar(containerColor = Color.White, tonalElevation = 8.dp) {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route
                
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Radar, contentDescription = "Radar") },
                    label = { Text("Radar") },
                    selected = currentRoute == "radar",
                    onClick = { navController.navigate("radar") { launchSingleTop = true } },
                    colors = NavigationBarItemDefaults.colors(selectedIconColor = TealAccent, selectedTextColor = TealAccent)
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.List, contentDescription = "History") },
                    label = { Text("History") },
                    selected = currentRoute == "history",
                    onClick = { navController.navigate("history") { launchSingleTop = true } },
                    colors = NavigationBarItemDefaults.colors(selectedIconColor = TealAccent, selectedTextColor = TealAccent)
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                    label = { Text("Profile") },
                    selected = currentRoute == "profile",
                    onClick = { navController.navigate("profile") { launchSingleTop = true } },
                    colors = NavigationBarItemDefaults.colors(selectedIconColor = TealAccent, selectedTextColor = TealAccent)
                )
            }
        }
    ) { padding ->
        NavHost(navController = navController, startDestination = "radar", modifier = Modifier.padding(padding)) {
            composable("radar") { RadarScreen(viewModel) }
            composable("history") { HistoryScreen(viewModel) }
            composable("profile") { ProfileScreen(viewModel) }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val orders by viewModel.availableOrders.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }

    val infiniteTransition = rememberInfiniteTransition()
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulsingDot"
    )

    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1545060894-7b57f0f6c271?q=80&w=1000",
            contentDescription = "Laundry Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.85f)))
        
        Column(modifier = Modifier.fillMaxSize()) {
            // Glassmorphism Header
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                color = Color.White.copy(alpha = 0.6f),
                shape = RoundedCornerShape(24.dp),
                border = BorderStroke(1.dp, Color.White.copy(alpha = 0.8f)),
                shadowElevation = 0.dp
            ) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.LocationOn,
                        contentDescription = "Radar",
                        tint = Color(0xFF00B4D8),
                        modifier = Modifier.size(28.dp)
                    )
                    Spacer(Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            "Searching in: ${zone.uppercase()}",
                            fontWeight = FontWeight.ExtraBold,
                            fontSize = 18.sp,
                            color = Color(0xFF03045E)
                        )
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(8.dp)
                                    .background(Color.Green.copy(alpha = alpha), CircleShape)
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                "Live Radar Active",
                                color = Color.Gray,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                    IconButton(
                        onClick = { viewModel.fetchAvailableOrders(context) },
                        modifier = Modifier.background(Color.White, CircleShape).size(40.dp)
                    ) {
                        Icon(Icons.Default.Refresh, contentDescription = "Refresh", tint = Color(0xFF00B4D8))
                    }
                }
            }
            
            if (isLoading && orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    SophisticatedLoadingIndicator()
                }
            } else if (orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.Search, 
                            contentDescription = "Empty", 
                            tint = Color.Gray.copy(alpha = 0.5f), 
                            modifier = Modifier.size(80.dp)
                        )
                        Spacer(Modifier.height(16.dp))
                        Text(
                            "No new orders right now.\nKeep your radar on!", 
                            color = Color.DarkGray, 
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium,
                            textAlign = TextAlign.Center
                        )
                        Spacer(Modifier.height(24.dp))
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(orders) { order ->
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().height(IntrinsicSize.Min)) {
                                // Subtle Left Border
                                Box(
                                    modifier = Modifier
                                        .width(6.dp)
                                        .fillMaxHeight()
                                        .background(Color(0xFF03045E))
                                )
                                Column(modifier = Modifier.padding(16.dp).weight(1f)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            "Order #${order.order_id}",
                                            fontWeight = FontWeight.ExtraBold,
                                            color = Color(0xFF03045E),
                                            fontSize = 18.sp
                                        )
                                        Text(
                                            "PKR ${order.total_amount ?: "0"}",
                                            color = Color(0xFF00B4D8),
                                            fontWeight = FontWeight.ExtraBold,
                                            fontSize = 18.sp
                                        )
                                    }
                                    Spacer(Modifier.height(12.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(
                                            Icons.Default.DateRange,
                                            contentDescription = "Date",
                                            tint = Color.Gray,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Spacer(Modifier.width(8.dp))
                                        Text(
                                            order.date ?: "Just now",
                                            color = Color.DarkGray,
                                            fontSize = 14.sp
                                        )
                                    }
                                    Spacer(Modifier.height(6.dp))
                                    Row(verticalAlignment = Alignment.Top) {
                                        Icon(
                                            Icons.Default.LocationOn,
                                            contentDescription = "Location",
                                            tint = Color.Gray,
                                            modifier = Modifier.size(16.dp).padding(top = 2.dp)
                                        )
                                        Spacer(Modifier.width(8.dp))
                                        Text(
                                            order.pickup_address ?: "N/A",
                                            color = Color.DarkGray,
                                            fontSize = 14.sp,
                                            lineHeight = 20.sp
                                        )
                                    }
                                    Spacer(Modifier.height(16.dp))
                                    Button(
                                        onClick = { selectedOrderForReview = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(12.dp),
                                        modifier = Modifier.fillMaxWidth(),
                                        contentPadding = PaddingValues(vertical = 14.dp)
                                    ) {
                                        Text("REVIEW ORDER", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        if (selectedOrderForReview != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForReview = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
                    Text("Order #${selectedOrderForReview!!.order_id}", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                    Spacer(Modifier.height(8.dp))
                    Text("Total Amount: PKR ${selectedOrderForReview!!.total_amount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(24.dp))
                    
                    val orderItems = selectedOrderForReview!!.items
                    if (!orderItems.isNullOrEmpty()) {
                        Text("Order Items", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                        Spacer(Modifier.height(8.dp))
                        LazyColumn(
                            modifier = Modifier.fillMaxWidth().heightIn(max = 250.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(orderItems) { item ->
                                ListItem(
                                    colors = ListItemDefaults.colors(containerColor = Color(0xFFF8F9FA)),
                                    headlineContent = { Text(item.name ?: "Unknown Item", fontWeight = FontWeight.Medium, color = Color(0xFF03045E)) },
                                    leadingContent = { 
                                        Box(
                                            modifier = Modifier.background(Color(0xFF00B4D8).copy(alpha = 0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 12.dp, vertical = 6.dp),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text("${item.quantity ?: 1}x", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                                        }
                                    }
                                )
                            }
                        }
                        Spacer(Modifier.height(24.dp))
                    } else {
                        Text("No items listed.", color = Color.Gray)
                        Spacer(Modifier.height(24.dp))
                    }
                    
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        Button(
                            onClick = { 
                                val orderId = selectedOrderForReview!!.order_id
                                if (orderId != null) {
                                    viewModel.rejectOrder(orderId, context)
                                }
                                selectedOrderForReview = null
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                            border = BorderStroke(1.dp, Color.Red),
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp),
                            contentPadding = PaddingValues(vertical = 14.dp)
                        ) {
                            Text("REJECT", color = Color.Red, fontWeight = FontWeight.Bold)
                        }
                        
                        Button(
                            onClick = { 
                                val orderIdStr = selectedOrderForReview!!.order_id?.toString() ?: ""
                                viewModel.acceptOrder(orderIdStr, context)
                                selectedOrderForReview = null
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                            modifier = Modifier.weight(1f),
                            shape = RoundedCornerShape(12.dp),
                            contentPadding = PaddingValues(vertical = 14.dp)
                        ) {
                            Text("ACCEPT", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val orders by viewModel.myOrders.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }

    LaunchedEffect(Unit) {
        viewModel.fetchMyOrders(context)
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.92f)))
        
        Column(modifier = Modifier.fillMaxSize()) {
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color(0xFF00B4D8))
                }
            } else if (orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Default.HourglassEmpty, contentDescription = "Empty", tint = Color.LightGray, modifier = Modifier.size(64.dp))
                        Spacer(Modifier.height(16.dp))
                        Text("No orders in your history.", color = Color.Gray)
                    }
                }
            } else {
                LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxSize()) {
                    items(orders) { order ->
                        val currentStatus = order.status ?: "Pending"
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp), 
                            colors = CardDefaults.cardColors(containerColor = Color.White), 
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.clickable { selectedOrderForUpdate = order }
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text("Order #${order.order_id}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E), fontSize = 16.sp)
                                    Spacer(Modifier.height(4.dp))
                                    Text("PKR ${order.total_amount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                                    Spacer(Modifier.height(8.dp))
                                    Text("Status: $currentStatus", color = Color.Gray, fontSize = 14.sp)
                                }
                                Column(horizontalAlignment = Alignment.End) {
                                    IconButton(
                                        onClick = { printReceipt(context, order) },
                                        modifier = Modifier.background(SoftWhite, RoundedCornerShape(8.dp))
                                    ) {
                                        Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print", tint = Color(0xFF03045E))
                                    }
                                    Spacer(Modifier.height(12.dp))
                                    Button(
                                        onClick = { selectedOrderForUpdate = order },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                        shape = RoundedCornerShape(8.dp),
                                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
                                    ) {
                                        Text("Update", fontSize = 12.sp, color = Color.White)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        if (selectedOrderForUpdate != null) {
            val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForUpdate = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Column {
                            Text("Update Order Status", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                            Spacer(Modifier.height(8.dp))
                            Text("Order #${selectedOrderForUpdate!!.order_id}", color = Color.Gray)
                        }
                        IconButton(onClick = { printReceipt(context, selectedOrderForUpdate!!) }) {
                            Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print Receipt", tint = Color(0xFF00B4D8))
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                    
                    val orderItems = selectedOrderForUpdate!!.items
                    if (!orderItems.isNullOrEmpty()) {
                        Text("Order Items", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                        Spacer(Modifier.height(8.dp))
                        LazyColumn(
                            modifier = Modifier.fillMaxWidth().heightIn(max = 250.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(orderItems) { item ->
                                ListItem(
                                    colors = ListItemDefaults.colors(containerColor = SoftWhite),
                                    headlineContent = { Text(item.name ?: "Unknown Item", fontWeight = FontWeight.Medium, color = Color(0xFF03045E)) },
                                    leadingContent = { 
                                        Box(
                                            modifier = Modifier.background(Color(0xFF00B4D8).copy(alpha = 0.2f), RoundedCornerShape(8.dp)).padding(horizontal = 12.dp, vertical = 6.dp),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text("${item.quantity ?: 1}x", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                                        }
                                    }
                                )
                            }
                        }
                        Spacer(Modifier.height(24.dp))
                    }
                    
                    Text("Select New Status", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                    Spacer(Modifier.height(16.dp))
                    
                    val statuses = listOf("Pending", "Accepted", "Out for Pickup", "Picked Up", "Washing", "Ready for Delivery", "Out for Delivery", "Delivered")
                    var expandedStatus by remember { mutableStateOf(false) }
                    
                    ExposedDropdownMenuBox(
                        expanded = expandedStatus,
                        onExpandedChange = { expandedStatus = it }
                    ) {
                        OutlinedTextField(
                            value = selectedOrderForUpdate!!.status ?: "Pending",
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Status") },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedStatus) },
                            modifier = Modifier.menuAnchor().fillMaxWidth(),
                            colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Color(0xFF00B4D8))
                        )
                        ExposedDropdownMenu(
                            expanded = expandedStatus,
                            onDismissRequest = { expandedStatus = false }
                        ) {
                            statuses.forEach { st ->
                                DropdownMenuItem(
                                    text = { Text(st) },
                                    onClick = { 
                                        viewModel.updateOrderStatus(selectedOrderForUpdate!!.order_id?.toString() ?: "", st, context)
                                        expandedStatus = false
                                        selectedOrderForUpdate = null
                                    }
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ProfileScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val name by viewModel.riderName.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    
    var address by remember { mutableStateOf(viewModel.homeAddress.value) }
    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(model = "https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080", contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
        Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.92f)))
        AsyncImage(
            model = "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1080&auto=format&fit=crop",
            contentDescription = "Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize(),
            alpha = 0.05f
        )
        Column(modifier = Modifier.fillMaxSize()) {
        Surface(color = Color.White, shadowElevation = 4.dp, modifier = Modifier.fillMaxWidth()) {
            Row(modifier = Modifier.padding(16.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                SnowhiteLogo(modifier = Modifier.height(40.dp))
                Spacer(Modifier.width(12.dp))
                Text("Captain Profile", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = DarkBlue)
            }
        }
        
        LazyColumn(contentPadding = PaddingValues(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxSize()) {
            item {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.AccountCircle, contentDescription = "Avatar", tint = DarkBlue, modifier = Modifier.size(64.dp))
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text(name, fontWeight = FontWeight.Bold, fontSize = 20.sp, color = DarkBlue)
                        Text("Hubs: $zone", color = TealAccent, fontWeight = FontWeight.Bold)
                    }
                }
                Spacer(Modifier.height(24.dp))
                
                Text("Home Address", color = DarkBlue, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = address,
                    onValueChange = { address = it },
                    placeholder = { Text("Enter personal address") },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(Modifier.height(16.dp))
                Text("Bank Details for Payouts", color = DarkBlue, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = bankName,
                    onValueChange = { bankName = it },
                    placeholder = { Text("Bank Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = bankIban,
                    onValueChange = { bankIban = it },
                    placeholder = { Text("IBAN / Account Number") },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(Modifier.height(16.dp))
                Button(
                    onClick = { viewModel.saveProfileDetails(context, address, bankName, bankIban) },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = TealAccent)
                ) {
                    Text("Save Details", color = Color.White, fontWeight = FontWeight.Bold)
                }
                
                Spacer(Modifier.height(32.dp))
                HorizontalDivider(color = Color.LightGray)
                Spacer(Modifier.height(16.dp))
                
                Button(
                    onClick = {
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/923001234567"))
                        try { context.startActivity(intent) } catch (e: Exception) { Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show() }
                    },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF25D366))
                ) {
                    Icon(Icons.Default.SupportAgent, contentDescription = "Help", tint = Color.White)
                    Spacer(Modifier.width(8.dp))
                    Text("Customer Support / Help", color = Color.White, fontWeight = FontWeight.Bold)
                }
                
                Spacer(Modifier.height(16.dp))
                Button(
                    onClick = { viewModel.logout(context) },
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = ErrorRed)
                ) {
                    Icon(Icons.Default.PowerSettingsNew, contentDescription = "Logout", tint = Color.White)
                    Spacer(Modifier.width(8.dp))
                    Text("Go Offline / Logout", color = Color.White, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

}

// --- Main Activity ---
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            RiderTheme {
                val viewModel: RiderViewModel = viewModel()
                val context = LocalContext.current
                
                val navController = rememberNavController()
                
                LaunchedEffect(Unit) {
                    viewModel.initSession(context)
                }
                val riderId by viewModel.riderId.collectAsState()
                
                LaunchedEffect(riderId) {
                    if (riderId != -1) {
                        navController.navigate("dashboard") { popUpTo(0) }
                    } else {
                        navController.navigate("auth") { popUpTo(0) }
                    }
                }
                
                NavHost(navController = navController, startDestination = "auth") {
                    composable("auth") {
                        AuthFlow(viewModel, navController)
                    }
                    composable("dashboard") {
                        MainAppScreen(viewModel)
                    }
                }
            }
        }
            }
    }


@Composable
fun SophisticatedLoadingIndicator() {
    val infiniteTransition = rememberInfiniteTransition(label = "loading")
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotation"
    )
    val scale by infiniteTransition.animateFloat(
        initialValue = 0.8f,
        targetValue = 1.2f,
        animationSpec = infiniteRepeatable(
            animation = tween(800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "scale"
    )

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.size(80.dp)) {
            // Outer rotating ring
            CircularProgressIndicator(
                modifier = Modifier.fillMaxSize().graphicsLayer { rotationZ = rotation },
                color = Color(0xFF00B4D8),
                strokeWidth = 3.dp,
                trackColor = Color(0xFF03045E).copy(alpha = 0.1f)
            )
            // Inner rotating ring (opposite direction)
            CircularProgressIndicator(
                modifier = Modifier.size(50.dp).graphicsLayer { rotationZ = -rotation },
                color = Color(0xFF03045E),
                strokeWidth = 4.dp,
                strokeCap = StrokeCap.Round
            )
            // Center pulsing icon
            Icon(
                Icons.Default.LocationOn,
                contentDescription = null,
                tint = Color(0xFF00B4D8),
                modifier = Modifier.size(24.dp).graphicsLayer {
                    scaleX = scale
                    scaleY = scale
                }
            )
        }
        Spacer(Modifier.height(24.dp))
        Text(
            "Scanning for orders...",
            color = Color(0xFF03045E),
            fontWeight = FontWeight.SemiBold,
            fontSize = 16.sp,
            modifier = Modifier.graphicsLayer { alpha = if (scale < 1f) scale else 2f - scale }
        )
    }
}
