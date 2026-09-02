#!/bin/bash
cat << 'INNER_EOF' > /app/applet/app/src/main/java/com/example/ui/screens/LiveTrackingScreen.kt
package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.network.OrderResponse
import com.example.viewmodel.SnowWhiteViewModel
import kotlinx.coroutines.launch

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

    var selectedOrder by remember { mutableStateOf<OrderResponse?>(null) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val coroutineScope = rememberCoroutineScope()

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
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
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
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { selectedOrder = order },
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text("Order #${order.order_id ?: "N/A"}", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                                    Surface(
                                        color = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                                        shape = RoundedCornerShape(4.dp)
                                    ) {
                                        Text(order.status ?: "UNKNOWN", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                                    }
                                }
                                Spacer(Modifier.height(8.dp))
                                Text("Date: ${order.date ?: "N/A"}", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                                Spacer(Modifier.height(12.dp))
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text("Total: PKR ${order.total_amount ?: 0}", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text("View Details", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                                        Icon(Icons.Default.ChevronRight, contentDescription = "View Details", tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        if (selectedOrder != null) {
            ModalBottomSheet(
                onDismissRequest = { selectedOrder = null },
                sheetState = sheetState,
                containerColor = Color.White
            ) {
                OrderDetailsSheetContent(
                    order = selectedOrder!!,
                    onClose = {
                        coroutineScope.launch {
                            try {
                                sheetState.hide()
                            } catch (e: Exception) {
                                // Ignore animation errors
                            }
                        }.invokeOnCompletion {
                            selectedOrder = null
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun OrderDetailsSheetContent(order: OrderResponse, onClose: () -> Unit) {
    LazyColumn(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text("Order #${order.order_id ?: "N/A"}", fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.titleLarge)
                    Text("Date: ${order.date ?: "N/A"}", color = Color.Gray, style = MaterialTheme.typography.bodyMedium)
                }
                Surface(
                    color = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                    shape = RoundedCornerShape(4.dp)
                ) {
                    Text(order.status ?: "UNKNOWN", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(8.dp))
            HorizontalDivider()
        }

        item {
            Text("Order Status Tracker", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(12.dp))
            
            val currentStatus = order.status?.uppercase() ?: ""
            val step1 = true
            val step2 = currentStatus != "COLLECTING" && currentStatus != "PENDING"
            val step3 = step2 && currentStatus != "RECEIVED" && currentStatus != "RECEIVED AT HUB"
            val step4 = currentStatus == "DELIVERED" || currentStatus == "OUT_FOR_DELIVERY" || currentStatus == "OUT FOR DELIVERY"
            
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                VerticalProgressStep("1", "Collecting / Received", step1)
                VerticalProgressStep("2", "Received at Hub", step2)
                VerticalProgressStep("3", "In Washing / Processing", step3)
                VerticalProgressStep("4", "Out for Delivery / Delivered", step4)
            }
            Spacer(Modifier.height(8.dp))
            HorizontalDivider()
        }

        item {
            Text("Items Breakdown", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(8.dp))
            if (order.items.isNullOrEmpty()) {
                Text("No item details available.", color = Color.Gray, style = MaterialTheme.typography.bodyMedium)
            } else {
                order.items?.forEach { item ->
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("${item.qty ?: 0}x ${item.item ?: "Unknown Item"}", style = MaterialTheme.typography.bodyMedium)
                        Text("PKR ${item.price ?: 0}", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
                    }
                }
            }
            Spacer(Modifier.height(8.dp))
            HorizontalDivider()
        }

        item {
            Text("Summary", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(8.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Pickup Slot:", color = Color.Gray)
                Text(order.pickup_slot ?: "N/A", fontWeight = FontWeight.Medium)
            }
            Spacer(Modifier.height(8.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Total Amount:", color = Color.Gray, style = MaterialTheme.typography.titleMedium)
                Text("PKR ${order.total_amount ?: 0}", fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.titleLarge)
            }
            Spacer(Modifier.height(24.dp))
        }

        item {
            Button(
                onClick = onClose,
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurfaceVariant)
            ) {
                Text("Close Details", fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(32.dp))
        }
    }
}

@Composable
fun VerticalProgressStep(stepNum: String, label: String, isComplete: Boolean) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Box(
            modifier = Modifier
                .size(28.dp)
                .clip(CircleShape)
                .background(if (isComplete) MaterialTheme.colorScheme.primary else Color.LightGray),
            contentAlignment = Alignment.Center
        ) {
            if (isComplete) {
                Icon(Icons.Default.Check, contentDescription = "Complete", tint = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(18.dp))
            } else {
                Text(stepNum, color = Color.DarkGray, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
            }
        }
        Spacer(Modifier.width(12.dp))
        Text(
            text = label, 
            style = MaterialTheme.typography.bodyLarge, 
            color = if (isComplete) MaterialTheme.colorScheme.onSurface else Color.Gray, 
            fontWeight = if (isComplete) FontWeight.Bold else FontWeight.Normal
        )
    }
}
INNER_EOF
chmod +x fix_bottom_sheet.sh
./fix_bottom_sheet.sh