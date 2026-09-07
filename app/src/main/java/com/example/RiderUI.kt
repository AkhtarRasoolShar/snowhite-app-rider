package com.example

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Reusable Modern Order Card
@Composable
fun ModernOrderCard(
    order: RiderOrder,
    onAccept: () -> Unit,
    onReject: () -> Unit,
    onViewDetails: () -> Unit
) {
    Card(
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(16.dp),
        modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Surface(
                    color = Color(0xFFE3F2FD),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text(
                        text = "Order #${order.orderId}",
                        color = Color(0xFF1565C0),
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        fontSize = 14.sp
                    )
                }
                Text(
                    text = order.status ?: "Pending",
                    color = Color(0xFFE65100),
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp
                )
            }
            Spacer(Modifier.height(12.dp))
            
            Text(text = order.customerName ?: "Customer", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Color(0xFF03045E))
            Spacer(Modifier.height(8.dp))
            
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(4.dp))
                Text(text = order.pickupAddress ?: "Unknown Location", color = Color.Gray, fontSize = 14.sp)
            }
            Spacer(Modifier.height(12.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Total Earning", color = Color.Gray, fontSize = 14.sp)
                Text(text = "PKR ${order.totalAmount ?: "0"}", color = Color(0xFF2E7D32), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
            }
            Spacer(Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(
                    onClick = onReject,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Red),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Reject")
                }
                Button(
                    onClick = onAccept,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Accept")
                }
            }
            Spacer(Modifier.height(8.dp))
            TextButton(onClick = onViewDetails, modifier = Modifier.fillMaxWidth()) {
                Text("View Full Details", color = Color(0xFF00B4D8))
            }
        }
    }
}

@Composable
fun WalletScreen(viewModel: RiderViewModel) {
    // A simple beautiful Wallet UI
    Column(
        modifier = Modifier.fillMaxSize().background(Color(0xFFF8F9FA)).padding(16.dp)
    ) {
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF03045E)),
            elevation = CardDefaults.cardElevation(8.dp)
        ) {
            Column(modifier = Modifier.padding(24.dp)) {
                Text("Available Balance", color = Color.White.copy(alpha = 0.8f), fontSize = 16.sp)
                Spacer(Modifier.height(8.dp))
                Text("PKR 4,500.00", color = Color.White, fontSize = 36.sp, fontWeight = FontWeight.ExtraBold)
                Spacer(Modifier.height(24.dp))
                Button(
                    onClick = { /* trigger payout request */ },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Request Payout", color = Color.White, fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 4.dp))
                }
            }
        }
        Spacer(Modifier.height(24.dp))
        Text("Recent Transactions", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Color(0xFF03045E))
        Spacer(Modifier.height(16.dp))
        
        // Mock Transactions
        val txns = listOf("Order #101" to "PKR 350", "Order #102" to "PKR 450", "Payout" to "-PKR 500")
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(txns) { txn ->
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(12.dp),
                    elevation = CardDefaults.cardElevation(2.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(txn.first, fontWeight = FontWeight.Medium)
                        Text(txn.second, color = if (txn.second.startsWith("-")) Color.Red else Color(0xFF2E7D32), fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
    }
}

@Composable
fun OrderDetailsSheetContent(
    order: RiderOrder,
    isHistory: Boolean,
    onAccept: (() -> Unit)? = null,
    onReject: (() -> Unit)? = null,
    onUpdateStatus: ((String) -> Unit)? = null,
    onPrint: (() -> Unit)? = null,
    onChat: (() -> Unit)? = null
) {
    val context = androidx.compose.ui.platform.LocalContext.current
    Column(modifier = Modifier.fillMaxWidth().padding(24.dp).padding(bottom = 32.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Column {
                Text(if (isHistory) "Active Order Details" else "Review Order", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
                Spacer(Modifier.height(8.dp))
                Surface(color = Color(0xFFE3F2FD), shape = RoundedCornerShape(8.dp)) {
                    Text("Order #${order.orderId ?: 0}", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), color = Color(0xFF1565C0), fontWeight = FontWeight.Bold)
                }
            }
            if (isHistory && onPrint != null) {
                IconButton(onClick = onPrint, modifier = Modifier.background(Color(0xFFF8F9FA), androidx.compose.foundation.shape.CircleShape)) {
                    Icon(androidx.compose.material.icons.Icons.Default.Print, contentDescription = "Print Receipt", tint = Color(0xFF00B4D8))
                }
            }
        }
        Spacer(Modifier.height(24.dp))
        
        // Customer Section
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF8F9FA)),
            elevation = CardDefaults.cardElevation(0.dp),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Customer Contact", fontSize = 14.sp, color = Color.Gray)
                Spacer(Modifier.height(8.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column {
                        Text(order.customerName ?: "Unknown Customer", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color(0xFF03045E))
                        Text(order.customerPhone ?: "No Phone", color = Color.DarkGray)
                    }
                    if (order.customerPhone != null && order.customerPhone.isNotEmpty()) {
                        IconButton(
                            onClick = {
                                val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:${order.customerPhone}"))
                                context.startActivity(intent)
                            },
                            modifier = Modifier.background(Color(0xFF2E7D32).copy(alpha=0.1f), androidx.compose.foundation.shape.CircleShape)
                        ) {
                            Icon(Icons.Default.Phone, contentDescription = "Call", tint = Color(0xFF2E7D32))
                        }
                    }
                }
            }
        }
        Spacer(Modifier.height(16.dp))
        
        // Pickup Address Section
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF8F9FA)),
            elevation = CardDefaults.cardElevation(0.dp),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Pickup Address", fontSize = 14.sp, color = Color.Gray)
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.LocationOn, contentDescription = "Location", tint = Color.Gray, modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(
                        text = order.pickupAddress ?: "Unknown Location", 
                        fontSize = 14.sp, 
                        modifier = Modifier.weight(1f),
                        color = Color(0xFF1E293B)
                    )
                    
                    // NATIVE GOOGLE MAPS INTENT BUTTON
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
                            .background(Color(0xFFE0F2FE), shape = androidx.compose.foundation.shape.CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Place, // Or Navigation icon
                            contentDescription = "Navigate",
                            tint = Color(0xFF0284C7)
                        )
                    }
                }
            }
        }
        Spacer(Modifier.height(24.dp))
        
        Text("Total Amount: PKR ${order.totalAmount ?: "0"}", color = Color(0xFF2E7D32), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
        Spacer(Modifier.height(16.dp))
        
        val orderItems = order.items
        if (!orderItems.isNullOrEmpty()) {
            Text("Garments Breakdown", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF03045E))
            Spacer(Modifier.height(8.dp))
            LazyColumn(
                modifier = Modifier.fillMaxWidth().heightIn(max = 200.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(orderItems) { item ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFFF8F9FA), RoundedCornerShape(8.dp))
                            .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(text = "${item.quantity ?: 1}x", color = Color(0xFF00B4D8), fontWeight = FontWeight.Bold)
                        Text(text = item.name ?: "Laundry Garment", color = Color(0xFF03045E), modifier = Modifier.padding(start = 8.dp))
                    }
                }
            }
            Spacer(Modifier.height(24.dp))
        } else {
            Text("No items listed.", color = Color.Gray)
            Spacer(Modifier.height(24.dp))
        }
        
        if (isHistory && onUpdateStatus != null) {
            val statusMap = listOf("Pending" to "Collected", "Collected" to "In Process", "In Process" to "Out for Delivery", "Out for Delivery" to "Delivered")
            val currentStatus = order.status ?: "Pending"
            val nextStatus = statusMap.find { it.first == currentStatus }?.second
            
            if (nextStatus != null) {
                Button(
                    onClick = { onUpdateStatus(nextStatus) },
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Mark as $nextStatus", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(12.dp))
            }
            if (onChat != null) {
                OutlinedButton(
                    onClick = onChat,
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Icon(Icons.Default.Email, contentDescription = "Chat", modifier = Modifier.padding(end = 8.dp))
                    Text("Chat with Customer", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            }
        } else if (!isHistory && onAccept != null && onReject != null) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedButton(
                    onClick = onReject,
                    modifier = Modifier.weight(1f).height(56.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Red),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Reject", fontSize = 16.sp)
                }
                Button(
                    onClick = onAccept,
                    modifier = Modifier.weight(1f).height(56.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text("Accept", fontSize = 16.sp)
                }
            }
        }
    }
}
