#!/bin/bash
cat << 'INNER_EOF' > /app/applet/app/src/main/java/com/example/network/ApiService.kt
package com.example.network

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

data class ApiResponseWrapper<T>(
    val status: String,
    val data: T
)

@JsonClass(generateAdapter = true)
data class LaundryOrderRequest(
    val customer_id: Int = 1,
    val customer_name: String = "Suhail Ahmed",
    val customer_phone: String = "+92 301 1234567",
    val items: List<LaundryItemRequest>,
    val pickup_slot: String,
    val pickup_address: String,
    val detergent_pref: String,
    val starch_level: String,
    val special_notes: String,
    val estimated_total: Int
)

@JsonClass(generateAdapter = true)
data class LaundryItemRequest(
    val garment_id: String,
    val quantity: Int,
    val service_type: String
)

@JsonClass(generateAdapter = true)
data class OrderResponse(
    val order_id: String? = null,
    @Json(name = "created_at") val date: String? = null,
    val total_amount: Int? = 0,
    val status: String? = null
)

interface ApiService {
    @POST("routes.php?action=create_laundry_order")
    suspend fun createLaundryOrder(@Body request: LaundryOrderRequest): Response<Unit>

    @GET("routes.php?action=get_customer_orders")
    suspend fun getCustomerOrders(@Query("customer_id") customerId: Int = 1): ApiResponseWrapper<List<OrderResponse>>
}
INNER_EOF

cat << 'INNER_EOF' > /app/applet/app/src/main/java/com/example/ui/screens/LiveTrackingScreen.kt
package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.viewmodel.SnowWhiteViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LiveTrackingScreen(
    viewModel: SnowWhiteViewModel,
    onBack: () -> Unit,
    onOpenDrawer: (() -> Unit)? = null
) {
    val orders by viewModel.orders.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val errorMessage by viewModel.errorMessage.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.fetchOrders()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My Laundry Orders") },
                navigationIcon = {
                    if (onOpenDrawer != null) {
                        IconButton(onClick = onOpenDrawer) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    } else {
                        IconButton(onClick = onBack) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.surface)
        ) {
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (errorMessage != null) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("Error: $errorMessage", color = MaterialTheme.colorScheme.error)
                }
            } else if (orders.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("No Order History Yet")
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(orders) { order ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text("Order #${order.order_id ?: "N/A"}", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                                    Surface(
                                        color = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                                        shape = RoundedCornerShape(4.dp)
                                    ) {
                                        Text(order.status ?: "UNKNOWN", modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp), color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelSmall)
                                    }
                                }
                                Spacer(Modifier.height(8.dp))
                                Text("Date: ${order.date ?: "N/A"}", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                                Text("Total: PKR ${order.total_amount ?: 0}", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }
    }
}
INNER_EOF

chmod +x fix_models.sh
./fix_models.sh