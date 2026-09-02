with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Imports
target_imports = """import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.google.gson.GsonBuilder"""
replace_imports = """import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.google.gson.GsonBuilder
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.rememberCameraPositionState
import com.google.maps.android.compose.CameraPositionState
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import retrofit2.http.PATCH"""
content = content.replace(target_imports, replace_imports)

# 2. Data classes and Retrofit Interface
target_api = """data class AcceptOrderRequest(val order_id: String, val rider_id: Int)

// --- Retrofit Interface ---
interface RiderApiService {"""
replace_api = """data class AcceptOrderRequest(val order_id: String, val rider_id: Int)
data class UpdateStatusRequest(val rider_id: Int, val status: String)

// --- Retrofit Interface ---
interface RiderApiService {"""
content = content.replace(target_api, replace_api)

target_endpoint = """    @POST("routes.php?action=accept_order")
    suspend fun acceptOrder(@Body request: AcceptOrderRequest): Response<GenericResponse<Unit>>
}"""
replace_endpoint = """    @POST("routes.php?action=accept_order")
    suspend fun acceptOrder(@Body request: AcceptOrderRequest): Response<GenericResponse<Unit>>

    @PATCH("routes.php?action=update_status")
    suspend fun updateStatus(@Body request: UpdateStatusRequest): Response<GenericResponse<Unit>>
}"""
content = content.replace(target_endpoint, replace_endpoint)


# 3. Viewmodel: add isOnline, init, toggle
target_vm_vars = """    private val _riderAddress = MutableStateFlow("")
    val riderAddress = _riderAddress.asStateFlow()
    
    private val _riderId = MutableStateFlow(-1)"""
replace_vm_vars = """    private val _riderAddress = MutableStateFlow("")
    val riderAddress = _riderAddress.asStateFlow()
    
    private val _isOnline = MutableStateFlow(false)
    val isOnline = _isOnline.asStateFlow()
    
    private val _riderId = MutableStateFlow(-1)"""
content = content.replace(target_vm_vars, replace_vm_vars)

target_vm_init = """        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
        _riderAddress.value = prefs.getString("rider_address", "") ?: ""
    }"""
replace_vm_init = """        _bankIban.value = prefs.getString("bank_iban", "") ?: ""
        _riderAddress.value = prefs.getString("rider_address", "") ?: ""
        _isOnline.value = prefs.getBoolean("is_online", false)
    }"""
content = content.replace(target_vm_init, replace_vm_init)

target_vm_toggle = """    fun acceptOrder(order: RiderOrderResponse, context: Context) {"""
replace_vm_toggle = """    fun toggleOnlineStatus(context: Context, online: Boolean) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().putBoolean("is_online", online).apply()
        _isOnline.value = online
        
        viewModelScope.launch {
            try {
                val statusString = if (online) "online" else "offline"
                RetrofitClient.apiService.updateStatus(UpdateStatusRequest(_riderId.value, statusString))
            } catch (e: Exception) {
                // Background update failed, real app might retry, but state is locally updated
            }
        }
    }

    fun acceptOrder(order: RiderOrderResponse, context: Context) {"""
content = content.replace(target_vm_toggle, replace_vm_toggle)


# 4. UI: RadarScreen Top bar switch & GoogleMap
target_radar_top = """        Surface(
            color = Color.White,
            shadowElevation = 4.dp,
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                SnowWhiteLogo(modifier = Modifier.height(40.dp))
                Spacer(Modifier.height(8.dp))
                Surface(
                    color = DarkBlue.copy(alpha = 0.1f),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        Icon(Icons.Default.LocationOn, contentDescription = "Hub", tint = DarkBlue, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Active Hubs: ${zone.uppercase()}", color = DarkBlue, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    }
                }
            }
        }"""
replace_radar_top = """        val isOnline by viewModel.isOnline.collectAsState()
        
        Surface(
            color = Color.White,
            shadowElevation = 4.dp,
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    SnowWhiteLogo(modifier = Modifier.height(32.dp))
                    
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(if (isOnline) "ONLINE" else "OFFLINE", 
                             color = if (isOnline) TealAccent else Color.Gray, 
                             fontWeight = FontWeight.Bold, 
                             fontSize = 12.sp)
                        Spacer(Modifier.width(8.dp))
                        Switch(
                            checked = isOnline,
                            onCheckedChange = { viewModel.toggleOnlineStatus(context, it) },
                            colors = SwitchDefaults.colors(checkedThumbColor = TealAccent, checkedTrackColor = TealAccent.copy(alpha=0.3f))
                        )
                    }
                }
                Spacer(Modifier.height(8.dp))
                Surface(
                    color = DarkBlue.copy(alpha = 0.1f),
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        Icon(Icons.Default.LocationOn, contentDescription = "Hub", tint = DarkBlue, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Active Hubs: ${zone.uppercase()}", color = DarkBlue, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    }
                }
            }
        }"""
content = content.replace(target_radar_top, replace_radar_top)


target_radar_map = """        // Placeholder Map Box
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
                .background(Color(0xFFE2E8F0)),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.Map, contentDescription = "Map", tint = Color.Gray, modifier = Modifier.size(48.dp))
                Spacer(Modifier.height(8.dp))
                Text("Live Map Integration Pending", color = Color.Gray, fontWeight = FontWeight.Bold)
            }
        }"""
replace_radar_map = """        // Google Map Box
        val karachi = LatLng(24.8607, 67.0011)
        val cameraPositionState = rememberCameraPositionState {
            position = CameraPosition.fromLatLngZoom(karachi, 12f)
        }
        
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
                .background(Color(0xFFE2E8F0))
        ) {
            GoogleMap(
                modifier = Modifier.fillMaxSize(),
                cameraPositionState = cameraPositionState
            )
        }"""
content = content.replace(target_radar_map, replace_radar_map)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
