import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

imports = """import com.google.android.gms.location.LocationServices
import android.location.Geocoder
import android.location.Location
import java.util.Locale
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import android.Manifest
"""

if "import com.google.android.gms.location.LocationServices" not in content:
    content = content.replace("import android.os.Bundle", imports + "import android.os.Bundle")

old_fetch = """    fun fetchAvailableOrders(context: Context) {
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
    }"""

new_fetch = """    fun fetchAvailableOrders(context: Context) {
        val zone = _riderZone.value
        val riderId = _riderId.value
        if (zone.isEmpty() || riderId == -1) return
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val response = RetrofitClient.apiService.getAvailableOrders(zone, riderId)
                if (response.isSuccessful && response.body()?.status == "success") {
                    val newOrders = response.body()?.data ?: emptyList()
                    _availableOrders.value = newOrders
                    calculateDistances(context, newOrders)
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

    private fun calculateDistances(context: Context, orders: List<RiderOrder>) {
        if (orders.isEmpty()) return
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return
        
        val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
        fusedLocationClient.lastLocation.addOnSuccessListener { location ->
            if (location != null) {
                viewModelScope.launch(Dispatchers.IO) {
                    val geocoder = Geocoder(context, Locale.getDefault())
                    val updatedOrders = orders.map { order ->
                        val address = order.pickup_address
                        if (!address.isNullOrEmpty()) {
                            try {
                                val results = geocoder.getFromLocationName(address, 1)
                                if (!results.isNullOrEmpty()) {
                                    val loc = results[0]
                                    val resultsArray = FloatArray(1)
                                    Location.distanceBetween(
                                        location.latitude, location.longitude,
                                        loc.latitude, loc.longitude,
                                        resultsArray
                                    )
                                    order.copy(distanceInMeters = resultsArray[0])
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
    }"""

content = content.replace(old_fetch, new_fetch)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
