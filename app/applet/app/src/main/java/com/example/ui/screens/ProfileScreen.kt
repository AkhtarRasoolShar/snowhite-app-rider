package com.example.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(onOpenDrawer: () -> Unit) {
    var notificationsEnabled by remember { mutableStateOf(true) }
    
    Scaffold(
        containerColor = SoftSlate,
        topBar = {
            TopAppBar(
                title = { Text("Profile & Settings", color = DeepNavy, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onOpenDrawer) { 
                        Icon(Icons.Default.Menu, contentDescription = "Menu", tint = DeepNavy) 
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.padding(padding).fillMaxSize(), 
            contentPadding = PaddingValues(16.dp), 
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            item {
                Surface(shape = RoundedCornerShape(16.dp), color = Color.White, shadowElevation = 2.dp, modifier = Modifier.fillMaxWidth()) {
                    Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Surface(shape = CircleShape, color = ElectricBlue, modifier = Modifier.size(64.dp)) {
                            Icon(Icons.Default.Person, contentDescription = "Avatar", tint = Color.White, modifier = Modifier.padding(16.dp))
                        }
                        Spacer(Modifier.width(16.dp))
                        Column {
                            Text("Zubair Khan", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleLarge, color = DeepNavy)
                            Text("akhtarrasool275@gmail.com", color = Color.Gray, style = MaterialTheme.typography.bodyMedium)
                            Text("+92 300 1234567", color = Color.Gray, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                }
            }

            item {
                Text("App Preferences", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium, color = DeepNavy, modifier = Modifier.padding(bottom = 8.dp))
                Surface(shape = RoundedCornerShape(16.dp), color = Color.White, shadowElevation = 2.dp, modifier = Modifier.fillMaxWidth()) {
                    Column {
                        ListItem(
                            headlineContent = { Text("Notifications") },
                            supportingContent = { Text("SMS / Push alerts for laundry status") },
                            trailingContent = { Switch(checked = notificationsEnabled, onCheckedChange = { notificationsEnabled = it }) }
                        )
                        HorizontalDivider()
                        ListItem(
                            headlineContent = { Text("Language") },
                            supportingContent = { Text("English") },
                            trailingContent = { Icon(Icons.Default.Language, contentDescription = "Lang") },
                            modifier = Modifier.clickable { }
                        )
                    }
                }
            }

            item {
                Text("Saved Payment Methods", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium, color = DeepNavy, modifier = Modifier.padding(bottom = 8.dp))
                Surface(shape = RoundedCornerShape(16.dp), color = Color.White, shadowElevation = 2.dp, modifier = Modifier.fillMaxWidth()) {
                    Column {
                        ListItem(
                            headlineContent = { Text("Cash on Delivery") },
                            leadingContent = { Icon(Icons.Default.Money, contentDescription = "COD", tint = ElectricBlue) },
                            modifier = Modifier.clickable { }
                        )
                        HorizontalDivider()
                        ListItem(
                            headlineContent = { Text("JazzCash / EasyPaisa") },
                            leadingContent = { Icon(Icons.Default.AccountBalanceWallet, contentDescription = "Wallet", tint = TealAccent) },
                            modifier = Modifier.clickable { }
                        )
                        HorizontalDivider()
                        ListItem(
                            headlineContent = { Text("Credit/Debit Card") },
                            leadingContent = { Icon(Icons.Default.CreditCard, contentDescription = "Card", tint = DeepNavy) },
                            modifier = Modifier.clickable { }
                        )
                    }
                }
            }

            item {
                Surface(shape = RoundedCornerShape(16.dp), color = Color.White, shadowElevation = 2.dp, modifier = Modifier.fillMaxWidth()) {
                    Column {
                        ListItem(headlineContent = { Text("Terms of Service") }, modifier = Modifier.clickable { })
                        HorizontalDivider()
                        ListItem(headlineContent = { Text("Privacy Policy") }, modifier = Modifier.clickable { })
                    }
                }
            }
            
            item {
                Button(onClick = { }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                    Text("Log Out")
                }
            }
        }
    }
}
