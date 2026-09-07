package com.example

import java.util.Locale
import androidx.compose.ui.text.style.TextAlign

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

import androidx.compose.runtime.getValue

import androidx.compose.runtime.setValue

import androidx.compose.ui.Modifier



import android.Manifest

import android.content.Context

import android.content.Intent

import android.content.pm.PackageManager

import android.location.Geocoder

import android.location.Location

import android.net.Uri

import android.os.Build

import android.os.Bundle

import android.util.Log

import android.widget.Toast

import androidx.activity.ComponentActivity

import androidx.activity.compose.setContent

import androidx.activity.enableEdgeToEdge

import androidx.activity.result.contract.ActivityResultContracts

import androidx.activity.compose.rememberLauncherForActivityResult

import androidx.compose.animation.*

import androidx.compose.foundation.*

import androidx.compose.foundation.layout.*

import androidx.compose.foundation.lazy.*

import androidx.compose.foundation.lazy.grid.*

import androidx.compose.foundation.shape.*

import androidx.compose.material.icons.Icons

import androidx.compose.material.icons.automirrored.filled.*

import androidx.compose.material.icons.filled.*

import androidx.compose.material3.*

import androidx.compose.runtime.*

import androidx.compose.ui.Alignment

import androidx.compose.ui.graphics.Color

import androidx.compose.ui.layout.ContentScale

import androidx.compose.ui.platform.LocalContext

import androidx.compose.ui.text.font.FontWeight

import androidx.compose.ui.text.style.TextOverflow

import androidx.compose.ui.unit.dp

import androidx.compose.ui.unit.sp

import androidx.compose.ui.text.input.PasswordVisualTransformation

import androidx.compose.ui.input.pointer.pointerInput

import androidx.compose.foundation.gestures.detectTapGestures

import androidx.core.app.ActivityCompat

import androidx.core.view.WindowCompat

import androidx.lifecycle.viewmodel.compose.viewModel

import androidx.navigation.NavController

import androidx.navigation.NavHostController

import androidx.navigation.compose.*

import androidx.work.*

import coil.compose.AsyncImage


import com.google.android.gms.location.LocationServices


import retrofit2.Response

import retrofit2.http.*

import retrofit2.Retrofit

import retrofit2.converter.gson.GsonConverterFactory

import com.google.gson.annotations.SerializedName

import com.google.gson.Gson


import retrofit2.http.Headers

import java.util.concurrent.TimeUnit

import kotlin.reflect.KProperty

// --- Colors ---
val DarkBlue = Color(0xFF03045E)
val TealAccent = Color(0xFF00B4D8)
val SoftWhite = Color(0xFFF8FAFC)
val ErrorRed = Color(0xFFEF4444)

// --- API Models ---
data class GenericResponse<T>(
    @SerializedName("status") val status: String? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("data") val data: T? = null
)



data class TypingStatus(
    @SerializedName("is_typing") val is_typing: Boolean? = null
)

data class ChatMessage(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("order_id") val orderId: Int? = null,
    @SerializedName("sender_type") val senderType: String? = null,
    @SerializedName("sender_id") val senderId: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("created_at") val createdAt: String? = null,
    @SerializedName("status") var status: String? = null, // e.g., sent, delivered, seen
    @SerializedName("is_read") val isRead: String? = "0"
)

data class SendMessageRequest(
    @SerializedName("order_id") val orderId: Int,
    @SerializedName("sender_type") val senderType: String,
    @SerializedName("sender_id") val senderId: Int,
    @SerializedName("message") val message: String
)

data class RiderAuthData(
    @SerializedName("id") val id: Int = -1,
    @SerializedName("name") val name: String? = null,
    @SerializedName("phone") val phone: String? = null,
    @SerializedName("service_zone") val service_zone: String? = null,
    @SerializedName("status") val status: String? = null,
    val whatsapp_number: String? = null
)

data class RiderOrder(
    @SerializedName("order_id") val orderId: String? = null,
    @SerializedName("pickup_address") val pickupAddress: String? = null,
    @SerializedName("total_amount") val totalAmount: String? = null,
    @SerializedName("date") val date: String? = null,
    @SerializedName("status") val status: String? = null,
    @SerializedName("items") val items: List<OrderItem>? = emptyList(),
    @SerializedName("zone") val zone: String? = null,
    @SerializedName("customer_name") val customerName: String? = null,
    @SerializedName("customer_phone") val customerPhone: String? = null,
    var distanceInMeters: Float? = null
)

data class OrderItem(
    @SerializedName("name") val name: String? = null,
    @SerializedName("quantity") val quantity: String? = null
)

data class RiderLoginRequest(@SerializedName("phone") val phone: String? = null, val password: String, val is_rider_app: Boolean = true)
data class RiderRegisterRequest(
    @SerializedName("name") val name: String? = null,
    @SerializedName("phone") val phone: String? = null,
    val password: String,
    @SerializedName("service_zone") val service_zone: List<String>? = null,
    @SerializedName("email") val email: String? = null
)
data class Hub(
    @SerializedName("id") val id: Int? = null,
    @SerializedName("name") val name: String? = null
)

data class AppSettings(
    val app_name: String? = null,
    val logo_url: String? = null
)

data class AcceptOrderRequest(val order_id: String, val rider_id: String)
data class UpdateOrderStatusRequest(val order_id: String, val status: String)

// --- Retrofit Service ---
interface RiderApiService {
    @Headers("Cache-Control: no-cache")
    @POST("routes.php?action=login")
    suspend fun login(@Body request: RiderLoginRequest): Response<GenericResponse<RiderAuthData>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=rider_register")
    suspend fun register(@Body request: RiderRegisterRequest): Response<GenericResponse<RiderAuthData>>

    @GET("routes.php?action=get_hubs")
    suspend fun getHubs(): Response<GenericResponse<List<Hub>>>

    @GET("routes.php?action=get_available_orders")
    suspend fun getAvailableOrders(@Query("zone") zone: String, @Query("rider_id") riderId: Int): Response<GenericResponse<List<RiderOrder>>>
    
    @Headers("Content-Type: application/json")
    @POST("routes.php?action=reject_order")
    suspend fun rejectOrder(@Body request: Map<String, String>): Response<GenericResponse<Unit>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=accept_order")
    suspend fun acceptOrder(@Body request: AcceptOrderRequest): Response<GenericResponse<Unit>>

    @GET("routes.php?action=get_rider_orders")
    suspend fun getRiderOrders(@Query("rider_id") riderId: Int): Response<GenericResponse<List<RiderOrder>>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=update_rider_profile")
    suspend fun updateProfile(@Body request: Map<String, String>): Response<GenericResponse<Unit>>

    @GET("routes.php?action=get_chat_messages")
    suspend fun getChatMessages(@Query("order_id") orderId: Int): retrofit2.Response<GenericResponse<List<ChatMessage>>>

    @GET("routes.php?action=get_typing_status")
    suspend fun getTypingStatus(@Query("order_id") orderId: Int, @Query("sender_type") senderType: String): retrofit2.Response<GenericResponse<TypingStatus>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=update_typing_status")
    suspend fun updateTypingStatus(@Body request: Map<String, String>): retrofit2.Response<GenericResponse<Unit>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=send_chat_message")
    suspend fun sendChatMessage(@Body requestBody: okhttp3.RequestBody): retrofit2.Response<GenericResponse<Any>>

    @Headers("Content-Type: application/json")
    @POST("routes.php?action=update_order_status")
    suspend fun updateOrderStatus(@Body request: UpdateOrderStatusRequest): Response<GenericResponse<Unit>>
}

object RetrofitClient {
    private const val BASE_URL = "https://snow.akfasft.com/api/"
    val gson = GsonBuilder().setLenient().create()
    
    private val logging = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
    private val client = OkHttpClient.Builder()
        .addInterceptor(logging)
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
            putString("whatsapp_number", data.whatsapp_number ?: "")
            putString("rider_zones", data.service_zone ?: "")
        }.apply()
    }

    fun logout(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().clear().apply()
    }
}

class RiderViewModel : ViewModel() {

    var email by androidx.compose.runtime.mutableStateOf("")
    var isFetchingHubs by androidx.compose.runtime.mutableStateOf(false)
    var errorMessage by androidx.compose.runtime.mutableStateOf<String?>(null)
    var availableHubs by androidx.compose.runtime.mutableStateOf<List<Hub>>(emptyList())
    var selectedHubs by androidx.compose.runtime.mutableStateOf<Set<String>>(emptySet())
    var appSettings by androidx.compose.runtime.mutableStateOf(AppSettings())

    init {
        fetchHubs()
    }

    fun fetchHubs() {
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
    }
    private val _riderId = MutableStateFlow<Int>(-1)
    val riderId: StateFlow<Int> = _riderId
    
    private val _riderName = MutableStateFlow("")
    val riderName: StateFlow<String> = _riderName
    
    private val _riderPhone = MutableStateFlow("")
    val riderPhone: StateFlow<String> = _riderPhone
    
    private val _whatsappNumber = MutableStateFlow("")
    val whatsappNumber: StateFlow<String> = _whatsappNumber
    
    private val _riderZone = MutableStateFlow("")
    val riderZone: StateFlow<String> = _riderZone
    
    private val _homeAddress = MutableStateFlow("")
    val homeAddress: StateFlow<String> = _homeAddress
    
    private val _bankName = MutableStateFlow("")
    val bankName: StateFlow<String> = _bankName
    
    private val _bankIban = MutableStateFlow("")
    val bankIban: StateFlow<String> = _bankIban
    
    private val _quickReply1 = MutableStateFlow("I am on my way!")
    val quickReply1: StateFlow<String> = _quickReply1
    
    private val _quickReply2 = MutableStateFlow("I have arrived at the pickup location.")
    val quickReply2: StateFlow<String> = _quickReply2

    private val _availableOrders = MutableStateFlow<List<RiderOrder>>(emptyList())
    val availableOrders: StateFlow<List<RiderOrder>> = _availableOrders
    
    private val _myOrders = MutableStateFlow<List<RiderOrder>>(emptyList())
    val myOrders: StateFlow<List<RiderOrder>> = _myOrders

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading
    
    private val _authError = MutableStateFlow<String?>(null)
    val authError: StateFlow<String?> = _authError

    private val _pendingApproval = MutableStateFlow(false)
    
    private val _sortOption = MutableStateFlow("Newest")
    val sortOption: StateFlow<String> = _sortOption

    fun setSortOption(option: String) {
        _sortOption.value = option
    }

    private fun calculateHaversineDistance(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Float {
        val R = 6371e3 // Earth radius in meters
        val phi1 = Math.toRadians(lat1)
        val phi2 = Math.toRadians(lat2)
        val deltaPhi = Math.toRadians(lat2 - lat1)
        val deltaLambda = Math.toRadians(lon2 - lon1)
        val a = kotlin.math.sin(deltaPhi / 2) * kotlin.math.sin(deltaPhi / 2) +
                kotlin.math.cos(phi1) * kotlin.math.cos(phi2) *
                kotlin.math.sin(deltaLambda / 2) * kotlin.math.sin(deltaLambda / 2)
        val c = 2 * kotlin.math.atan2(kotlin.math.sqrt(a), kotlin.math.sqrt(1 - a))
        return (R * c).toFloat()
    }
    val pendingApproval: StateFlow<Boolean> = _pendingApproval
    
    sealed class PendingAction {
        data class AcceptOrder(val orderId: String) : PendingAction()
        data class RejectOrder(val orderId: String) : PendingAction()
        data class UpdateOrderStatus(val orderId: String, val newStatus: String) : PendingAction()
    }
    
    private val pendingActions = mutableListOf<PendingAction>()

    fun initSession(context: Context) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        _riderId.value = prefs.getInt("rider_id", -1)
        _riderName.value = prefs.getString("rider_name", "") ?: ""
        _riderPhone.value = prefs.getString("rider_phone", "") ?: ""
        _whatsappNumber.value = prefs.getString("whatsapp_number", "") ?: ""
        _riderZone.value = prefs.getString("rider_zones", "") ?: ""
        _homeAddress.value = prefs.getString("rider_address", "") ?: ""
        _bankName.value = prefs.getString("bank_name", "") ?: ""
        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
        _quickReply1.value = prefs.getString("quick_reply_1", "I am on my way!") ?: "I am on my way!"
        _quickReply2.value = prefs.getString("quick_reply_2", "I have arrived at the pickup location.") ?: "I have arrived at the pickup location."
        
        try {
            val connectivityManager = context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
            val request = android.net.NetworkRequest.Builder()
                .addCapability(android.net.NetworkCapabilities.NET_CAPABILITY_INTERNET)
                .build()
            connectivityManager.registerNetworkCallback(request, object : android.net.ConnectivityManager.NetworkCallback() {
                override fun onAvailable(network: android.net.Network) {
                    retryPendingActions(context)
                }
            })
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun retryPendingActions(context: Context) {
        val actionsToRetry = pendingActions.toList()
        pendingActions.clear()
        actionsToRetry.forEach { action ->
            when (action) {
                is PendingAction.AcceptOrder -> acceptOrder(action.orderId, context)
                is PendingAction.RejectOrder -> rejectOrder(action.orderId, context)
                is PendingAction.UpdateOrderStatus -> updateOrderStatus(action.orderId, action.newStatus, context)
            }
        }
    }

    fun updateWhatsApp(context: Context, whatsapp: String) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val request = mapOf("rider_id" to id.toString(), "whatsapp_number" to whatsapp)
                val response = RetrofitClient.apiService.updateProfile(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
                    prefs.edit().putString("whatsapp_number", whatsapp).apply()
                    _whatsappNumber.value = whatsapp
                    Toast.makeText(context, "Profile Updated!", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update profile", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun clearError() {
        _authError.value = null
    }

    fun login(phone: String, pass: String, context: Context, onSuccess: () -> Unit) {
        viewModelScope.launch {
            SessionManager.logout(context)
            _riderId.value = -1
            _authError.value = null
            try {
                _isLoading.value = true
                val res = RetrofitClient.apiService.login(RiderLoginRequest(phone, pass))
                android.util.Log.d("API_RESPONSE", "Response: $res")
                if (res.isSuccessful) {
                    val body = res.body()
                    android.util.Log.d("API_RESPONSE", "Body: $body")
                    if (body?.status == "success" && body.data != null) {
                        SessionManager.saveUser(context, body.data)
                        // Trigger initialization to load the session state in ViewModel
                        initSession(context)
                        onSuccess()
                    } else {
                        _authError.value = body?.message ?: "Invalid Credentials"
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

    fun register(name: String, phone: String, pass: String, zones: List<String>, email: String, context: Context) {
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

    fun fetchAvailableOrders(context: Context) {
        val zone = _riderZone.value
        val riderId = _riderId.value
        if (zone.isEmpty() || riderId == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.getAvailableOrders(zone, riderId)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val newOrders = response.body()?.data ?: emptyList()
                    _availableOrders.value = newOrders
                    calculateDistances(context, newOrders)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch orders", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    private fun calculateDistances(context: Context, orders: List<RiderOrder>) {
        if (orders.isEmpty()) return
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return
        
        val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
        fusedLocationClient.lastLocation.addOnSuccessListener { location ->
            if (location != null) {
                viewModelScope.launch(Dispatchers.IO) {
                    val geocoder = Geocoder(context, Locale.getDefault())
                    val updatedOrders = orders.map { order ->
                        val address = order.pickupAddress
                        if (!address.isNullOrEmpty()) {
                            try {
                                val results = geocoder.getFromLocationName(address, 1)
                                if (!results.isNullOrEmpty()) {
                                    val loc = results[0]
                                    val distance = calculateHaversineDistance(
                                        location.latitude, location.longitude,
                                        loc.latitude, loc.longitude
                                    )
                                    order.copy(distanceInMeters = distance)
                                } else order
                            } catch (e: Exception) { order }
                        } else order
                    }
                    withContext(Dispatchers.Main) {
                        _availableOrders.value = updatedOrders
                    }
                }
            }
        }
    }

    fun fetchMyOrders(context: Context) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.getRiderOrders(id)
                if (response.isSuccessful && response.body()?.status == "success") {
                    _myOrders.value = response.body()?.data ?: emptyList()
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch history", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun acceptOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.acceptOrder(AcceptOrderRequest(orderId, id.toString()))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Accepted!", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to accept order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Order acceptance queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.AcceptOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun rejectOrder(orderId: String, context: Context) {
        val id = _riderId.value
        if (id == -1) {
            _isLoading.value = false
            return
        }
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val request = mapOf("order_id" to orderId.toString(), "rider_id" to id.toString())
                val response = RetrofitClient.apiService.rejectOrder(request)
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Order Rejected", Toast.LENGTH_SHORT).show()
                    fetchAvailableOrders(context)
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to reject order", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Order rejection queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.RejectOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun updateOrderStatus(orderId: String, newStatus: String, context: Context) {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = RetrofitClient.apiService.updateOrderStatus(UpdateOrderStatusRequest(orderId, newStatus))
                if (response.isSuccessful && response.body()?.status == "success") {
                    Toast.makeText(context, "Status updated to $newStatus", Toast.LENGTH_SHORT).show()
                    fetchMyOrders(context) // Refresh
                } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update status", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Status update queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.UpdateOrderStatus(orderId, newStatus)
                if (!pendingActions.contains(action)) pendingActions.add(action)
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun saveProfileDetails(context: Context, address: String, bankName: String, bankIban: String, qr1: String, qr2: String) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putString("rider_address", address)
            putString("bank_name", bankName)
            putString("bank_iban", bankIban)
            putString("quick_reply_1", qr1)
            putString("quick_reply_2", qr2)
        }.apply()
        _homeAddress.value = address
        _bankName.value = bankName
        _bankIban.value = bankIban
        _quickReply1.value = qr1
        _quickReply2.value = qr2
        Toast.makeText(context, "Profile Saved Locally", Toast.LENGTH_SHORT).show()
    }
    
    fun logout(context: Context) {
        SessionManager.logout(context)
        _riderId.value = -1
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

fun printReceipt(context: Context, order: RiderOrder, appName: String) {
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
                <div class="title">${appName}</div>
                <div class="subtitle">Receipt - Order #${order.orderId ?: "N/A"}</div>
            </div>
            <div class="details">
                <p><strong>Date:</strong> ${order.date ?: "N/A"}</p>
                <p><strong>Address:</strong> ${order.pickupAddress ?: "N/A"}</p>
            </div>
            <table>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                </tr>
                $itemsHtml
            </table>
            <div class="total">
                Total: PKR ${order.totalAmount ?: "0"}
            </div>
        </body>
        </html>
    """.trimIndent()
    
    webView.webViewClient = object : android.webkit.WebViewClient() {
        override fun onPageFinished(view: android.webkit.WebView, url: String) {
            val printAdapter = view.createPrintDocumentAdapter("Receipt_${order.orderId}")
            printManager.print("Receipt_${order.orderId}", printAdapter, android.print.PrintAttributes.Builder().build())
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
            modifier = Modifier.fillMaxSize().imePadding().padding(24.dp).verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                    coil.compose.AsyncImage(
                        model = viewModel.appSettings.logo_url,
                        contentDescription = "App Logo",
                        modifier = Modifier.size(60.dp)
                    )
                } else {
                    Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(60.dp), tint = Color.White)
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = viewModel.appSettings.app_name ?: "Captain Portal",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Text("Rider Login", color = Color.White.copy(alpha = 0.8f))
            }
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
            modifier = Modifier.fillMaxSize().imePadding().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            item {
                Spacer(Modifier.height(24.dp))
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                        coil.compose.AsyncImage(
                            model = viewModel.appSettings.logo_url,
                            contentDescription = "App Logo",
                            modifier = Modifier.size(60.dp)
                        )
                    } else {
                        Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(60.dp), tint = Color.White)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = viewModel.appSettings.app_name ?: "Captain Portal",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Text("Rider Registration", color = Color.White.copy(alpha = 0.8f))
                }
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
                            visualTransformation = PasswordVisualTransformation(),
                            singleLine = true
                        )
                        Spacer(Modifier.height(16.dp))
                        OutlinedTextField(
                            value = viewModel.email,
                            onValueChange = { viewModel.email = it; viewModel.clearError() },
                            label = { Text("Email") },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                        Spacer(Modifier.height(16.dp))
                        
                        viewModel.errorMessage?.let {
                            PersistentErrorBanner(it)
                            Spacer(Modifier.height(8.dp))
                        }
                        Text("Select Active Hubs:", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
                        
                        if (viewModel.isFetchingHubs) {
                            Box(modifier = Modifier.fillMaxWidth().padding(16.dp), contentAlignment = Alignment.Center) {
                                CircularProgressIndicator(color = TealAccent)
                            }
                        } else {
                        viewModel.availableHubs.forEach { hub ->
                            val hubName = hub.name ?: "Unknown"
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                                Checkbox(
                                    checked = viewModel.selectedHubs.contains(hubName),
                                    onCheckedChange = { isChecked ->
                                        viewModel.selectedHubs = if (isChecked) viewModel.selectedHubs + hubName else viewModel.selectedHubs - hubName
                                        viewModel.errorMessage = null
                                    },
                                    colors = CheckboxDefaults.colors(checkedColor = TealAccent)
                                )
                                Text(hubName, color = DarkBlue)
                            }
                        }
                        }
                        
                        Spacer(Modifier.height(24.dp))
                        
                        val isFormValid = name.isNotBlank() && phone.isNotBlank() && password.isNotBlank() && viewModel.email.isNotBlank() && viewModel.selectedHubs.isNotEmpty()
                        
                        Button(
                            onClick = {
                                if (isFormValid) {
                                    viewModel.register(name, phone, password, viewModel.selectedHubs.toList(), viewModel.email, context)
                                } else {
                                    android.widget.Toast.makeText(context, "Please fill all fields and select at least one hub.", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = if (isFormValid) Color(0xFF03045E) else Color.Gray),
                            enabled = !isLoading
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
fun RiderDashboardScreen(viewModel: RiderViewModel, onNavigateToRadar: () -> Unit) {
    val riderName by viewModel.riderName.collectAsState()
    val myOrders by viewModel.myOrders.collectAsState()
    
    val completedOrders = myOrders.count { it.status == "DELIVERED" }
    val totalEarnings = myOrders.filter { it.status == "DELIVERED" }.sumOf { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
    
    // Take the 5 most recent orders for the dashboard
    val recentOrders = myOrders.take(5)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF8FAFC)) 
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {
        // --- HEADER SECTION ---
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp, top = 8.dp)
        ) {
            Column {
                Text("Welcome back,", color = Color(0xFF64748B), fontSize = 14.sp)
                Text(text = riderName.ifEmpty { "Captain" }, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color(0xFF0F172A))
            }
        }

        // --- STATS CARDS SECTION ---
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            // Earnings Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF0EA5E9))
            ) {
                Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White)
                    Column {
                        Text("Total Earnings", color = Color.White.copy(alpha = 0.8f), fontSize = 12.sp)
                        Text("PKR $totalEarnings", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            // Completed Orders Card
            Card(
                modifier = Modifier.weight(1f).height(120.dp),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF10B981))
                    Column {
                        Text("Completed Orders", color = Color.Gray, fontSize = 12.sp)
                        Text("$completedOrders", color = Color(0xFF0F172A), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // --- QUICK ACTION (RADAR) ---
        Text("Quick Actions", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A), modifier = Modifier.padding(bottom = 12.dp))
        Button(
            onClick = { onNavigateToRadar() },
            modifier = Modifier.fillMaxWidth().height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0B192C)),
            shape = RoundedCornerShape(12.dp)
        ) {
            Icon(Icons.Default.Radar, contentDescription = null, tint = Color.White)
            Spacer(modifier = Modifier.width(12.dp))
            Text("Go to Radar (Find Orders)", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }

        Spacer(modifier = Modifier.height(32.dp))

        // --- RECENT ORDERS (HISTORY) SECTION ---
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Recent Orders", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
        }

        if (recentOrders.isEmpty()) {
            Box(modifier = Modifier.fillMaxWidth().padding(top = 32.dp), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.ListAlt, contentDescription = null, modifier = Modifier.size(48.dp), tint = Color.LightGray)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text("No recent orders found.", color = Color.Gray, fontSize = 14.sp)
                }
            }
        } else {
            recentOrders.forEach { order ->
                // Determine Status Colors dynamically
                val statusColor = when (order.status) {
                    "DELIVERED" -> Color(0xFF10B981) // Green
                    "PENDING", "COLLECTING" -> Color(0xFFF59E0B) // Orange
                    "RECEIVED_AT_HUB", "WASHING", "READY_FOR_DELIVERY" -> Color(0xFF3B82F6) // Blue
                    else -> Color.Gray
                }

                val statusText = order.status?.replace("_", " ") ?: "UNKNOWN"

                Card(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Order #${order.orderId}", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color(0xFF0F172A))
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(order.date ?: "", fontSize = 12.sp, color = Color.Gray)
                        }
                        
                        Column(horizontalAlignment = Alignment.End) {
                            Text(
                                text = "PKR ${order.totalAmount}", 
                                fontWeight = FontWeight.ExtraBold, 
                                fontSize = 16.sp, 
                                color = Color(0xFF0F172A)
                            )
                            Spacer(modifier = Modifier.height(6.dp))
                            
                            // Status Badge
                            Text(
                                text = statusText, 
                                fontSize = 10.sp, 
                                color = statusColor, 
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier
                                    .background(statusColor.copy(alpha = 0.15f), RoundedCornerShape(6.dp))
                                    .padding(horizontal = 8.dp, vertical = 4.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun MainAppScreen(viewModel: RiderViewModel) {
    val navController = rememberNavController()
    val isLoading by viewModel.isLoading.collectAsState()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    
    Scaffold(
        contentWindowInsets = WindowInsets.ime,
        bottomBar = {
            if (currentRoute != null && !currentRoute.startsWith("chat/")) {
                NavigationBar(containerColor = Color.White) {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Dashboard, contentDescription = "Dashboard") },
                    label = { Text("Dashboard") },
                    selected = currentRoute == "dashboard",
                    onClick = { navController.navigate("dashboard") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.LocationSearching, contentDescription = "Radar") },
                    label = { Text("Radar") },
                    selected = currentRoute == "radar",
                    onClick = { navController.navigate("radar") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
                NavigationBarItem(
                    icon = { Icon(Icons.AutoMirrored.Filled.List, contentDescription = "History") },
                    label = { Text("History") },
                    selected = currentRoute == "history",
                    onClick = { navController.navigate("history") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                    label = { Text("Profile") },
                    selected = currentRoute == "profile",
                    onClick = { navController.navigate("profile") { launchSingleTop = true; restoreState = true } },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF00B4D8),
                        selectedTextColor = Color(0xFF00B4D8),
                        indicatorColor = Color.Transparent,
                        unselectedIconColor = Color.Gray,
                        unselectedTextColor = Color.Gray
                    )
                )
            }
            }
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding).fillMaxSize()) {
            NavHost(navController = navController, startDestination = "dashboard", modifier = Modifier.fillMaxSize()) {
            composable("dashboard") { RiderDashboardScreen(viewModel, onNavigateToRadar = { navController.navigate("radar") { launchSingleTop = true; restoreState = true } }) }
            composable("radar") { RadarScreen(viewModel) }
            composable("history") { HistoryScreen(viewModel, navController) }
                        composable("wallet") { WalletScreen(viewModel) }
            composable("chat/{orderId}") { backStackEntry ->
                val orderId = backStackEntry.arguments?.getString("orderId")?.toIntOrNull() ?: 0
                val riderId by viewModel.riderId.collectAsState()
                OrderChatScreen(
                    orderId = orderId,
                    mySenderType = "rider",
                    mySenderId = riderId,
                    onBack = { navController.popBackStack() }
                )
            }
            composable("profile") { ProfileScreen(viewModel, navController) }
            composable("quickReplies") { QuickRepliesScreen(viewModel, navController) }
        }
        
        androidx.compose.animation.AnimatedVisibility(
            visible = isLoading,
            enter = androidx.compose.animation.fadeIn(),
            exit = androidx.compose.animation.fadeOut()
        ) {
            Box(modifier = Modifier.fillMaxSize().background(Color.White.copy(alpha = 0.5f)).pointerInput(Unit) { detectTapGestures { } }, contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFF00B4D8))
            }
        }
    }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RadarScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions(),
        onResult = { permissions: Map<String, Boolean> ->
            if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
                viewModel.fetchAvailableOrders(context)
            }
        }
    )
    
    LaunchedEffect(Unit) {
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            permissionLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
        }
    }

    val orders by viewModel.availableOrders.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    var selectedOrderForReview by remember { mutableStateOf<RiderOrder?>(null) }
    val radarSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val sortOption by viewModel.sortOption.collectAsState()
    var expandedSortMenu by remember { mutableStateOf(false) }
    
    val sortedOrders = remember(orders, sortOption) {
        when (sortOption) {
            "Total Amount" -> orders.sortedByDescending { it.totalAmount?.toDoubleOrNull() ?: 0.0 }
            "Distance (Haversine)" -> orders.sortedBy { it.distanceInMeters ?: Float.MAX_VALUE }
            "Hub" -> orders.sortedBy { it.zone ?: "" }
            else -> orders.sortedByDescending { it.orderId?.toIntOrNull() ?: 0 }
        }
    }

    LaunchedEffect(Unit) {
        viewModel.fetchAvailableOrders(context)
    }

    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Premium Header
            Surface(
                color = Color.White,
                shadowElevation = 2.dp,
                shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(24.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(10.dp).background(Color(0xFF00C853), CircleShape))
                                Spacer(Modifier.width(8.dp))
                                Text("Online & Searching", color = Color.Gray, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                            }
                            Spacer(Modifier.height(8.dp))
                            Text(zone.uppercase(), fontWeight = FontWeight.ExtraBold, fontSize = 22.sp, color = Color(0xFF1E293B))
                        }
                        IconButton(
                            onClick = { viewModel.fetchAvailableOrders(context) },
                            modifier = Modifier.background(Color(0xFFF1F5F9), CircleShape)
                        ) {
                            Icon(Icons.Default.Refresh, contentDescription = "Refresh", tint = Color(0xFF00B4D8))
                        }
                    }
                }
            }
            
            // Available & Sorting
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "${sortedOrders.size} Requests",
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF1E293B),
                    fontSize = 18.sp
                )
                Box {
                    Surface(
                        shape = RoundedCornerShape(20.dp),
                        color = Color.White,
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0)),
                        modifier = Modifier.clickable { expandedSortMenu = true }
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.Sort, contentDescription = "Sort", tint = Color(0xFF64748B), modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(6.dp))
                            Text(sortOption, color = Color(0xFF334155), fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                        }
                    }
                    DropdownMenu(
                        expanded = expandedSortMenu,
                        onDismissRequest = { expandedSortMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Newest") },
                            onClick = { viewModel.setSortOption("Newest"); expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Total Amount") },
                            onClick = { viewModel.setSortOption("Total Amount"); expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Distance (Haversine)") },
                            onClick = { viewModel.setSortOption("Distance (Haversine)"); expandedSortMenu = false }
                        )
                        DropdownMenuItem(
                            text = { Text("Hub (Zone)") },
                            onClick = { viewModel.setSortOption("Hub"); expandedSortMenu = false }
                        )
                    }
                }
            }

            if (sortedOrders.isEmpty() && !isLoading) {
                Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.Radar, 
                            contentDescription = "Searching", 
                            tint = Color.LightGray, 
                            modifier = Modifier.size(64.dp)
                        )
                        Spacer(Modifier.height(16.dp))
                        Text(
                            "No new requests nearby", 
                            color = Color.Gray, 
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium
                        )
                    }
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(horizontal = 20.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.weight(1f).fillMaxWidth()
                ) {
                    items(
                        items = sortedOrders,
                        key = { it.orderId ?: 0 }
                    ) { order ->
                        Card(
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForReview = order }
                        ) {
                            Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        "Order #${order.orderId}",
                                        fontWeight = FontWeight.Black,
                                        color = Color(0xFF0F172A),
                                        fontSize = 16.sp
                                    )
                                    Text(
                                        "PKR ${order.totalAmount ?: "0"}",
                                        color = Color(0xFF00B4D8),
                                        fontWeight = FontWeight.Black,
                                        fontSize = 16.sp
                                    )
                                }
                                Spacer(Modifier.height(8.dp))
                                
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.AccessTime, contentDescription = "Date", tint = Color(0xFF64748B), modifier = Modifier.size(14.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text(order.date ?: "Just now", color = Color(0xFF64748B), fontSize = 13.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                HorizontalDivider(color = Color(0xFFF1F5F9))
                                Spacer(Modifier.height(12.dp))
                                
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(Icons.Default.Place, contentDescription = "Location", tint = Color(0xFF64748B), modifier = Modifier.size(20.dp))
                                    Spacer(Modifier.width(12.dp))
                                    Text(
                                        text = order.pickupAddress ?: "N/A", 
                                        fontSize = 14.sp, 
                                        modifier = Modifier.weight(1f),
                                        color = Color(0xFF334155),
                                        maxLines = 2,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                    
                                    IconButton(
                                        onClick = {
                                            try {
                                                val gmmIntentUri = android.net.Uri.parse("geo:0,0?q=${android.net.Uri.encode(order.pickupAddress ?: "")}")
                                                val mapIntent = android.content.Intent(android.content.Intent.ACTION_VIEW, gmmIntentUri)
                                                mapIntent.setPackage("com.google.android.apps.maps")
                                                context.startActivity(mapIntent)
                                            } catch (e: Exception) {
                                                android.widget.Toast.makeText(context, "Google Maps is not installed", android.widget.Toast.LENGTH_SHORT).show()
                                            }
                                        },
                                        modifier = Modifier
                                            .size(40.dp)
                                            .background(Color(0xFFE0F2FE), shape = CircleShape)
                                    ) {
                                        Icon(
                                            imageVector = Icons.Default.Directions,
                                            contentDescription = "Navigate",
                                            tint = Color(0xFF0284C7),
                                            modifier = Modifier.size(20.dp)
                                        )
                                    }
                                }
                                
                                Spacer(Modifier.height(16.dp))
                                Button(
                                    onClick = { selectedOrderForReview = order },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                    shape = RoundedCornerShape(12.dp),
                                    modifier = Modifier.fillMaxWidth().height(48.dp)
                                ) {
                                    Text("REVIEW & ACCEPT", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (selectedOrderForReview != null) {
        ModalBottomSheet(
            onDismissRequest = { selectedOrderForReview = null },
            sheetState = radarSheetState,
            containerColor = Color.White,
            modifier = Modifier.fillMaxHeight(0.9f)
        ) {
            OrderDetailsSheetContent(
                order = selectedOrderForReview!!,
                isHistory = false,
                onAccept = {
                    viewModel.acceptOrder(selectedOrderForReview!!.orderId.toString(), context)
                    selectedOrderForReview = null
                },
                onReject = {
                    viewModel.rejectOrder(selectedOrderForReview!!.orderId ?: "", context)
                    selectedOrderForReview = null
                }
            )
        }
    }
}

@Composable
fun StatusBadge(status: String) {
    val formattedStatus = status.replace("_", " ")
        .lowercase()
        .split(" ")
        .joinToString(" ") { it.replaceFirstChar { char -> char.uppercase() } }
    
    val (bgColor, textColor) = when (status.uppercase()) {
        "DELIVERED" -> Color(0xFFE8F5E9) to Color(0xFF2E7D32)
        "OUT_FOR_DELIVERY" -> Color(0xFFE3F2FD) to Color(0xFF1565C0)
        "IN_WASHING", "RECEIVED_AT_HUB" -> Color(0xFFFFF3E0) to Color(0xFFEF6C00)
        "COLLECTING", "PENDING" -> Color(0xFFEDE7F6) to Color(0xFF4527A0)
        else -> Color(0xFFF5F5F5) to Color(0xFF616161)
    }

    Box(
        modifier = Modifier
            .background(bgColor, RoundedCornerShape(8.dp))
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(
            text = formattedStatus,
            color = textColor,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(viewModel: RiderViewModel, navController: androidx.navigation.NavController) {
    val context = LocalContext.current
    val orders by viewModel.myOrders.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    var selectedOrderForUpdate by remember { mutableStateOf<RiderOrder?>(null) }
    val historySheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showStatusDialogForOrder by remember { mutableStateOf<RiderOrder?>(null) }

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
            if (orders.isEmpty()) {
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
                        androidx.compose.material3.ElevatedCard(
                            elevation = CardDefaults.elevatedCardElevation(defaultElevation = 4.dp), 
                            colors = CardDefaults.elevatedCardColors(containerColor = Color.White), 
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier.fillMaxWidth().clickable { selectedOrderForUpdate = order }
                        ) {
                            Column(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Top) {
                                    Column {
                                        Text("Order #${order.orderId}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E), fontSize = 16.sp)
                                        Spacer(Modifier.height(4.dp))
                                        Text(order.date ?: "N/A", color = Color.Gray, fontSize = 12.sp)
                                    }
                                    Text("PKR ${order.totalAmount ?: "0"}", color = Color(0xFF00B4D8), fontWeight = FontWeight.ExtraBold, fontSize = 16.sp)
                                }
                                
                                Spacer(Modifier.height(12.dp))
                                StatusBadge(status = currentStatus)
                                Spacer(Modifier.height(16.dp))
                                
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Button(
                                            onClick = { showStatusDialogForOrder = order },
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                            shape = RoundedCornerShape(8.dp),
                                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                                        ) {
                                            Text("Update Status", fontSize = 12.sp, color = Color.White, fontWeight = FontWeight.Bold)
                                        }
                                        androidx.compose.material3.OutlinedButton(
                                            onClick = { selectedOrderForUpdate = order },
                                            shape = RoundedCornerShape(8.dp),
                                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                                        ) {
                                            Text("View Details", fontSize = 12.sp, color = Color(0xFF03045E))
                                        }
                                    }
                                    IconButton(
                                        onClick = { navController.navigate("chat/${order.orderId}") },
                                        modifier = Modifier.background(Color(0xFFE3F2FD), androidx.compose.foundation.shape.CircleShape).size(40.dp)
                                    ) {
                                        Icon(androidx.compose.material.icons.Icons.Default.Email, contentDescription = "Chat", tint = Color(0xFF1565C0), modifier = Modifier.size(20.dp))
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        if (showStatusDialogForOrder != null) {
            val order = showStatusDialogForOrder!!
            androidx.compose.material3.AlertDialog(
                onDismissRequest = { showStatusDialogForOrder = null },
                title = { Text("Update Order #${order.orderId}", fontWeight = FontWeight.Bold, color = Color(0xFF03045E)) },
                text = {
                    Column {
                        val statuses = listOf("RECEIVED_AT_HUB", "IN_WASHING", "OUT_FOR_DELIVERY", "DELIVERED")
                        statuses.forEach { status ->
                            Button(
                                onClick = { 
                                    viewModel.updateOrderStatus(order.orderId.toString(), status, context)
                                    showStatusDialogForOrder = null
                                },
                                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                                shape = RoundedCornerShape(8.dp)
                            ) {
                                Text(status, color = Color.White)
                            }
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showStatusDialogForOrder = null }) {
                        Text("Cancel", color = Color.Gray)
                    }
                },
                containerColor = Color.White
            )
        }

        if (selectedOrderForUpdate != null) {
            ModalBottomSheet(
                onDismissRequest = { selectedOrderForUpdate = null },
                sheetState = historySheetState,
                containerColor = Color.White
            ) {
                OrderDetailsSheetContent(
                    order = selectedOrderForUpdate!!,
                    isHistory = true,
                    onUpdateStatus = { nextStatus ->
                        viewModel.updateOrderStatus(selectedOrderForUpdate!!.orderId.toString(), nextStatus, context)
                        selectedOrderForUpdate = null
                    },
                    onPrint = { printReceipt(context, selectedOrderForUpdate!!, viewModel.appSettings.app_name ?: "Captain Portal") },
                    onChat = {
                        navController.navigate("chat/${selectedOrderForUpdate!!.orderId}")
                    }
                )
            }
        }
    }
}

@Composable
fun ProfileScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
    val name by viewModel.riderName.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    
    var address by remember { mutableStateOf(viewModel.homeAddress.value) }
    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }
    var whatsapp by remember { mutableStateOf(if (viewModel.whatsappNumber.value.isNotEmpty()) viewModel.whatsappNumber.value else viewModel.riderPhone.value) }

    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Header
            Surface(
                color = Color.White,
                shadowElevation = 2.dp,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .background(Color(0xFFE0F2FE), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            if (name.isNotEmpty()) name.take(1).uppercase() else "U",
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF00B4D8)
                        )
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(name.ifEmpty { "Driver" }, fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = Color(0xFF1E293B))
                    Spacer(Modifier.height(4.dp))
                    Surface(color = Color(0xFFF1F5F9), shape = RoundedCornerShape(12.dp)) {
                        Text("Hub: ${zone.ifEmpty { "N/A" }}", modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp), color = Color(0xFF475569), fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                    }
                }
            }
            
            LazyColumn(
                contentPadding = PaddingValues(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                item {
                    Text("Account Details", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(Modifier.height(8.dp))
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            OutlinedTextField(
                                value = address,
                                onValueChange = { address = it },
                                label = { Text("Home Address") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                            Spacer(Modifier.height(12.dp))
                            OutlinedTextField(
                                value = whatsapp,
                                onValueChange = { whatsapp = it },
                                label = { Text("WhatsApp Number") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                        }
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    Text("Bank Information", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(Modifier.height(8.dp))
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            OutlinedTextField(
                                value = bankName,
                                onValueChange = { bankName = it },
                                label = { Text("Bank Name") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                            Spacer(Modifier.height(12.dp))
                            OutlinedTextField(
                                value = bankIban,
                                onValueChange = { bankIban = it },
                                label = { Text("IBAN / Account Number") },
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(12.dp)
                            )
                        }
                    }
                    
                    Spacer(Modifier.height(32.dp))
                    Button(
                        onClick = { 
                            viewModel.saveProfileDetails(context, address, bankName, bankIban, viewModel.quickReply1.value, viewModel.quickReply2.value)
                            viewModel.updateWhatsApp(context, whatsapp) 
                        },
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text("SAVE CHANGES", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    Text("Preferences & Support", color = Color(0xFF64748B), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Spacer(Modifier.height(8.dp))
                    
                    OutlinedButton(
                        onClick = { navController.navigate("quickReplies") },
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        shape = RoundedCornerShape(12.dp),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE2E8F0))
                    ) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = Color(0xFF334155), modifier = Modifier.size(20.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Manage Quick Replies", color = Color(0xFF334155), fontWeight = FontWeight.SemiBold)
                    }
                    
                    Spacer(Modifier.height(12.dp))
                    Button(
                        onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/923001234567"))
                            try { context.startActivity(intent) } catch (e: Exception) { Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show() }
                        },
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF25D366)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(Icons.Default.SupportAgent, contentDescription = "Help", tint = Color.White)
                        Spacer(Modifier.width(8.dp))
                        Text("Customer Support", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    
                    Spacer(Modifier.height(24.dp))
                    TextButton(
                        onClick = { viewModel.logout(context) },
                        modifier = Modifier.fillMaxWidth().height(52.dp)
                    ) {
                        Icon(Icons.Default.PowerSettingsNew, contentDescription = "Logout", tint = Color(0xFFEF4444))
                        Spacer(Modifier.width(8.dp))
                        Text("Sign Out", color = Color(0xFFEF4444), fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.height(32.dp))
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuickRepliesScreen(viewModel: RiderViewModel, navController: NavHostController) {
    val context = LocalContext.current
    var reply1 by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(viewModel.quickReply1.value) }
    var reply2 by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(viewModel.quickReply2.value) }

    Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA))) {
        Column(modifier = Modifier.fillMaxSize().padding(24.dp)) {
            Text("Manage Quick Replies", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E293B))
            Spacer(Modifier.height(24.dp))
            
            OutlinedTextField(
                value = reply1,
                onValueChange = { reply1 = it },
                label = { Text("Quick Reply 1") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(
                value = reply2,
                onValueChange = { reply2 = it },
                label = { Text("Quick Reply 2") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(32.dp))
            
            Button(
                onClick = { 
                    viewModel.saveProfileDetails(context, viewModel.homeAddress.value, viewModel.bankName.value, viewModel.bankIban.value, reply1, reply2)
                    navController.popBackStack()
                },
                modifier = Modifier.fillMaxWidth().height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("SAVE REPLIES", color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
    }
}

// --- Main Activity ---
class MainActivity : androidx.activity.ComponentActivity() {
    override fun onCreate(savedInstanceState: android.os.Bundle?) {
        super.onCreate(savedInstanceState)
        
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.app.ActivityCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                androidx.core.app.ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }

        val workRequest = androidx.work.PeriodicWorkRequestBuilder<com.example.OrderPollingWorker>(15, java.util.concurrent.TimeUnit.MINUTES).build()
        androidx.work.WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "OrderPolling",
            androidx.work.ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )

        enableEdgeToEdge()
        androidx.core.view.WindowCompat.setDecorFitsSystemWindows(window, false)
        setContent {
            RiderTheme {
                val viewModel: RiderViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
                val context = LocalContext.current
                
                val navController = androidx.navigation.compose.rememberNavController()
                
                androidx.compose.runtime.LaunchedEffect(Unit) {
                    viewModel.initSession(context)
                }
                val riderId by viewModel.riderId.collectAsState()
                
                androidx.compose.runtime.LaunchedEffect(riderId) {
                    if (riderId != -1) {
                        navController.navigate("dashboard") { popUpTo(0) }
                    } else {
                        navController.navigate("auth") { popUpTo(0) }
                    }
                }
                
                androidx.navigation.compose.NavHost(navController = navController, startDestination = "auth") {
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
