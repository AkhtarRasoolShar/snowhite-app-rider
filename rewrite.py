code = """package com.example

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
import androidx.compose.ui.graphics.Color
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
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.google.gson.GsonBuilder
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
val DarkBlue = Color(0xFF0F172A)
val TealAccent = Color(0xFF14B8A6)
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

data class RiderOrderResponse(
    val order_id: String,
    val address: String?,
    val total_amount: String?,
    val status: String?
)

data class RiderLoginRequest(val phone: String, val password: String, val is_rider_app: Boolean = true)
data class RiderRegisterRequest(val name: String, val phone: String, val password: String, val service_zone: String)
data class AcceptOrderRequest(val order_id: String, val rider_id: Int)
data class UpdateOrderStatusRequest(val order_id: String, val status: String)

// --- Retrofit Service ---
interface RiderApiService {
    @POST("routes.php?action=login")
    suspend fun login(@Body request: RiderLoginRequest): Response<GenericResponse<RiderAuthData>>

    @POST("routes.php?action=rider_register")
    suspend fun register(@Body request: RiderRegisterRequest): Response<GenericResponse<RiderAuthData>>

    @GET("routes.php?action=get_available_orders")
    suspend fun getAvailableOrders(@Query("zone") zone: String): Response<GenericResponse<List<RiderOrderResponse>>>

    @POST("routes.php?action=accept_order")
    suspend fun acceptOrder(@Body request: AcceptOrderRequest): Response<GenericResponse<Unit>>

    @GET("routes.php?action=get_rider_orders")
    suspend fun getRiderOrders(@Query("rider_id") riderId: Int): Response<GenericResponse<List<RiderOrderResponse>>>

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
class RiderViewModel : ViewModel() {
    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _authError = MutableStateFlow<String?>(null)
    val authError = _authError.asStateFlow()
    
    private val _pendingApproval = MutableStateFlow(false)
    val pendingApproval = _pendingApproval.asStateFlow()

    private val _availableOrders = MutableStateFlow<List<RiderOrderResponse>>(emptyList())
    val availableOrders = _availableOrders.asStateFlow()

    private val _myOrders = MutableStateFlow<List<RiderOrderResponse>>(emptyList())
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

    fun login(phone: String, pass: String, context: Context) {
        viewModelScope.launch {
            _isLoading.value = true
            _authError.value = null
            _pendingApproval.value = false
            try {
                val response = RetrofitClient.apiService.login(RiderLoginRequest(phone, pass))
                if (response.isSuccessful) {
                    val body = response.body()
                    if (body?.status == "success" && body.data != null) {
                        if (body.data.status.equals("active", ignoreCase = true) || body.data.status.equals("approved", ignoreCase = true)) {
                            saveAuthData(context, body.data)
                        } else {
                            _pendingApproval.value = true
                            _authError.value = "Account Pending Approval by Superadmin."
                        }
                    } else {
                        _authError.value = body?.message ?: "Login Failed."
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
        if (zone.isEmpty()) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.getAvailableOrders(zone)
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
fun SnowWhiteLogo(modifier: Modifier = Modifier) {
    AsyncImage(
        model = "https://snowhite.com.pk/wp-content/uploads/2021/04/snowhite-logo.png",
        contentDescription = "SnowWhite Logo",
        contentScale = ContentScale.Fit,
        modifier = modifier
    )
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

// --- Screens ---
@Composable
fun AuthFlow(viewModel: RiderViewModel) {
    var isLogin by remember { mutableStateOf(true) }
    
    if (isLogin) {
        LoginScreen(viewModel, onNavigateToRegister = { isLogin = false })
    } else {
        RegisterScreen(viewModel, onNavigateToLogin = { isLogin = true })
    }
}

@Composable
fun LoginScreen(viewModel: RiderViewModel, onNavigateToRegister: () -> Unit) {
    val context = LocalContext.current
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize().background(SoftWhite).padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        SnowWhiteLogo(modifier = Modifier.height(60.dp).fillMaxWidth())
        Spacer(Modifier.height(32.dp))
        Text("Captain Portal", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = DarkBlue)
        Spacer(Modifier.height(24.dp))
        
        authError?.let { PersistentErrorBanner(it) }

        OutlinedTextField(
            value = phone,
            onValueChange = { phone = it },
            label = { Text("Phone Number") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        Spacer(Modifier.height(16.dp))
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation(),
            singleLine = true
        )
        Spacer(Modifier.height(24.dp))
        Button(
            onClick = { viewModel.login(phone, password, context) },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = DarkBlue),
            enabled = !isLoading && phone.isNotBlank() && password.isNotBlank()
        ) {
            if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
            else Text("LOGIN", color = Color.White, fontWeight = FontWeight.Bold)
        }
        Spacer(Modifier.height(16.dp))
        TextButton(onClick = onNavigateToRegister) {
            Text("New Rider? Apply Here", color = TealAccent)
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

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(SoftWhite).padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        item {
            Spacer(Modifier.height(48.dp))
            SnowWhiteLogo(modifier = Modifier.height(50.dp).fillMaxWidth())
            Spacer(Modifier.height(24.dp))
            Text("Captain Application", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = DarkBlue)
            Spacer(Modifier.height(24.dp))
            
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
                onValueChange = { phone = it },
                label = { Text("Phone Number") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                modifier = Modifier.fillMaxWidth(),
                visualTransformation = PasswordVisualTransformation()
            )
            Spacer(Modifier.height(16.dp))
            
            ExposedDropdownMenuBox(
                expanded = expandedZone,
                onExpandedChange = { expandedZone = it }
            ) {
                OutlinedTextField(
                    value = zone.ifEmpty { "Select Zone" },
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Primary Hub") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedZone) },
                    modifier = Modifier.menuAnchor().fillMaxWidth()
                )
                ExposedDropdownMenu(
                    expanded = expandedZone,
                    onDismissRequest = { expandedZone = false }
                ) {
                    zones.forEach { selection ->
                        DropdownMenuItem(
                            text = { Text(selection) },
                            onClick = {
                                zone = selection
                                expandedZone = false
                            }
                        )
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            Button(
                onClick = { viewModel.register(name, phone, password, zone, context) },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                colors = ButtonDefaults.buttonColors(containerColor = DarkBlue),
                enabled = !isLoading && name.isNotBlank() && phone.isNotBlank() && password.isNotBlank() && zone.isNotBlank()
            ) {
                if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                else Text("SUBMIT APPLICATION", color = Color.White, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(16.dp))
            TextButton(onClick = onNavigateToLogin) {
                Text("Back to Login", color = TealAccent)
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

@Composable
fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val orders by viewModel.availableOrders.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }

    Column(modifier = Modifier.fillMaxSize().background(SoftWhite)) {
        Surface(color = Color.White, shadowElevation = 4.dp, modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                SnowWhiteLogo(modifier = Modifier.height(40.dp))
                Spacer(Modifier.height(12.dp))
                Surface(color = DarkBlue.copy(alpha = 0.1f), shape = RoundedCornerShape(16.dp)) {
                    Row(modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.LocationOn, contentDescription = "Hub", tint = DarkBlue, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Active Hubs: ${zone.uppercase()}", color = DarkBlue, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    }
                }
            }
        }
        
        Box(modifier = Modifier.fillMaxWidth().height(180.dp).background(DarkBlue), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.Radar, contentDescription = "Map", tint = TealAccent, modifier = Modifier.size(64.dp))
                Spacer(Modifier.height(8.dp))
                Text("Live Map Integration Pending", color = Color.White, fontWeight = FontWeight.Bold)
            }
        }

        if (isLoading && orders.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = DarkBlue)
            }
        } else if (orders.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.HourglassEmpty, contentDescription = "Empty", tint = Color.LightGray, modifier = Modifier.size(64.dp))
                    Spacer(Modifier.height(16.dp))
                    Text("No orders available in your zone.", color = Color.Gray)
                    Spacer(Modifier.height(16.dp))
                    Button(
                        onClick = { viewModel.fetchAvailableOrders(context) },
                        colors = ButtonDefaults.buttonColors(containerColor = DarkBlue)
                    ) { Text("Refresh Radar") }
                }
            }
        } else {
            LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxSize()) {
                items(orders) { order ->
                    Card(elevation = CardDefaults.cardElevation(defaultElevation = 2.dp), colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(12.dp)) {
                        Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Order #${order.order_id}", fontWeight = FontWeight.Bold, color = DarkBlue, fontSize = 16.sp)
                                Text("PKR ${order.total_amount ?: "0"}", fontWeight = FontWeight.ExtraBold, color = TealAccent, fontSize = 18.sp)
                            }
                            Spacer(Modifier.height(8.dp))
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Place, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(8.dp))
                                Text(order.address ?: "No Address Provided", color = Color.DarkGray, fontSize = 14.sp)
                            }
                            Spacer(Modifier.height(16.dp))
                            Button(
                                onClick = { viewModel.acceptOrder(order.order_id, context) },
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = TealAccent),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Text("ACCEPT DELIVERY", color = Color.White, fontWeight = FontWeight.Bold)
                            }
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

    LaunchedEffect(Unit) {
        viewModel.fetchMyOrders(context)
    }

    Column(modifier = Modifier.fillMaxSize().background(SoftWhite)) {
        Surface(color = Color.White, shadowElevation = 4.dp, modifier = Modifier.fillMaxWidth()) {
            Text("My Assigned Orders", color = DarkBlue, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.padding(16.dp))
        }
        
        if (isLoading && orders.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = DarkBlue)
            }
        } else if (orders.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("No orders in history.", color = Color.Gray)
            }
        } else {
            LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxSize()) {
                items(orders) { order ->
                    var expandedStatus by remember { mutableStateOf(false) }
                    val statuses = listOf("COLLECTING", "RECEIVED_AT_HUB", "IN_WASHING", "OUT_FOR_DELIVERY", "DELIVERED")
                    val currentStatus = order.status ?: "COLLECTING"

                    Card(elevation = CardDefaults.cardElevation(defaultElevation = 2.dp), colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(12.dp)) {
                        Row(modifier = Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Order #${order.order_id}", fontWeight = FontWeight.Bold, color = DarkBlue, fontSize = 16.sp)
                                Spacer(Modifier.height(4.dp))
                                Text("PKR ${order.total_amount ?: "0"}", color = TealAccent, fontWeight = FontWeight.Bold)
                                Spacer(Modifier.height(8.dp))
                                
                                ExposedDropdownMenuBox(
                                    expanded = expandedStatus,
                                    onExpandedChange = { expandedStatus = it }
                                ) {
                                    OutlinedTextField(
                                        value = currentStatus,
                                        onValueChange = {},
                                        readOnly = true,
                                        label = { Text("Update Status") },
                                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedStatus) },
                                        modifier = Modifier.menuAnchor().fillMaxWidth(0.9f),
                                        textStyle = LocalTextStyle.current.copy(fontSize = 12.sp, color = TealAccent, fontWeight = FontWeight.Bold)
                                    )
                                    ExposedDropdownMenu(
                                        expanded = expandedStatus,
                                        onDismissRequest = { expandedStatus = false }
                                    ) {
                                        statuses.forEach { st ->
                                            DropdownMenuItem(
                                                text = { Text(st) },
                                                onClick = { 
                                                    viewModel.updateOrderStatus(order.order_id, st, context)
                                                    expandedStatus = false 
                                                }
                                            )
                                        }
                                    }
                                }
                            }
                            IconButton(
                                onClick = { Toast.makeText(context, "Connecting to Bluetooth Printer...", Toast.LENGTH_SHORT).show() },
                                modifier = Modifier.background(SoftWhite, RoundedCornerShape(8.dp))
                            ) {
                                Icon(Icons.Default.Print, contentDescription = "Print", tint = DarkBlue)
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

    Column(modifier = Modifier.fillMaxSize().background(SoftWhite)) {
        Surface(color = Color.White, shadowElevation = 4.dp, modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                SnowWhiteLogo(modifier = Modifier.height(40.dp))
            }
        }
        
        LazyColumn(contentPadding = PaddingValues(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxSize()) {
            item {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.AccountCircle, contentDescription = "Avatar", tint = DarkBlue, modifier = Modifier.size(64.dp))
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text(name, fontWeight = FontWeight.Bold, fontSize = 20.sp, color = DarkBlue)
                        Text("Hub: $zone", color = TealAccent, fontWeight = FontWeight.Bold)
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

// --- Main Activity ---
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            RiderTheme {
                val viewModel: RiderViewModel = viewModel()
                val context = LocalContext.current
                
                LaunchedEffect(Unit) {
                    viewModel.initSession(context)
                }
                
                val riderId by viewModel.riderId.collectAsState()
                
                if (riderId == -1) {
                    AuthFlow(viewModel)
                } else {
                    MainAppScreen(viewModel)
                }
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(code)
