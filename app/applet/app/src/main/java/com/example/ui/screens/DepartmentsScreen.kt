package com.example.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DepartmentsScreen(onOpenDrawer: () -> Unit) {
    Scaffold(
        containerColor = SoftSlate,
        topBar = {
            TopAppBar(
                title = { Text("Departments & Hubs", color = DeepNavy, fontWeight = FontWeight.Bold) },
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
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item { HubCard("Clifton Main Facility #14 (DHA Phase 5)", "08:00 AM - 10:00 PM", true) }
            item { HubCard("Gulshan Smart Hub #08 (Block 6)", "09:00 AM - 09:00 PM", false) }
            item { HubCard("PECHS Express Drop-off Point #02", "10:00 AM - 08:00 PM", false) }
        }
    }
}

@Composable
fun HubCard(name: String, hours: String, isMain: Boolean) {
    Surface(shape = RoundedCornerShape(16.dp), color = Color.White, shadowElevation = 2.dp, modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            if (isMain) {
                Surface(color = TealAccent.copy(alpha = 0.2f), shape = RoundedCornerShape(4.dp)) {
                    Text("MAIN HUB", color = TealAccent, fontWeight = FontWeight.Bold, fontSize = 10.sp, modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp))
                }
                Spacer(Modifier.height(8.dp))
            }
            Text(name, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium, color = DeepNavy)
            Spacer(Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.AccessTime, contentDescription = "Hours", tint = Color.Gray, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(4.dp))
                Text(hours, color = Color.Gray, style = MaterialTheme.typography.bodySmall)
            }
            Spacer(Modifier.height(16.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = { }, modifier = Modifier.weight(1f)) {
                    Icon(Icons.Default.Call, contentDescription = "Call", modifier = Modifier.size(16.dp))
                    Spacer(Modifier.width(4.dp))
                    Text("Call Store", fontSize = 12.sp)
                }
                Button(onClick = { }, modifier = Modifier.weight(1.5f), colors = ButtonDefaults.buttonColors(containerColor = ElectricBlue)) {
                    Icon(Icons.Default.Map, contentDescription = "Map", modifier = Modifier.size(16.dp))
                    Spacer(Modifier.width(4.dp))
                    Text("Coverage Area", fontSize = 12.sp)
                }
            }
            Spacer(Modifier.height(8.dp))
            TextButton(onClick = { }, modifier = Modifier.fillMaxWidth()) {
                Text("Drop-off Order Here", color = ElectricBlue)
            }
        }
    }
}
