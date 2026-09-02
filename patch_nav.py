import re
with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'onClick = { navController.navigate("orders") { popUpTo("home"); launchSingleTop = true } },',
    'onClick = { if (isLoggedIn) navController.navigate("orders") { popUpTo("home"); launchSingleTop = true } else navController.navigate("login") },'
)
content = content.replace(
    'onClick = { navController.navigate("profile") { popUpTo("home"); launchSingleTop = true } },',
    'onClick = { if (isLoggedIn) navController.navigate("profile") { popUpTo("home"); launchSingleTop = true } else navController.navigate("login") },'
)

# And fix the drawer header!
drawer_bad = """                        ModalDrawerSheet(drawerContainerColor = Color.White) {
                            Column(modifier = Modifier.padding(16.dp).fillMaxHeight()) {
                                Text("SnowWhite", fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = DeepNavyMain, modifier = Modifier.padding(bottom = 16.dp))
                                
                                // User profile snapshot
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 24.dp)) {
                                    Surface(shape = CircleShape, color = ElectricBlueMain, modifier = Modifier.size(48.dp)) {
                                        Icon(Icons.Default.Person, contentDescription = "Avatar", tint = Color.White, modifier = Modifier.padding(12.dp))
                                    }
                                    Spacer(Modifier.width(16.dp))
                                    Column {
                                        Text("Zubair Khan", fontWeight = FontWeight.Bold, color = DeepNavyMain)
                                        Text("+92 300 1234567", style = MaterialTheme.typography.bodySmall, color = Color.Gray)
                                        Text("Home, Office", style = MaterialTheme.typography.bodySmall, color = TealAccentMain)
                                    }
                                }
                                HorizontalDivider(modifier = Modifier.padding(bottom = 8.dp))"""

drawer_good = """                        ModalDrawerSheet(drawerContainerColor = Color.White) {
                            val custName by viewModel.customerName.collectAsState()
                            val custPhone by viewModel.customerPhone.collectAsState()
                            Column(modifier = Modifier.padding(16.dp).fillMaxHeight()) {
                                Text("SnowWhite", fontWeight = FontWeight.ExtraBold, fontSize = 24.sp, color = DeepNavyMain, modifier = Modifier.padding(bottom = 16.dp))
                                
                                // User profile snapshot
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 24.dp)) {
                                    Surface(shape = CircleShape, color = ElectricBlueMain, modifier = Modifier.size(48.dp)) {
                                        Icon(Icons.Default.Person, contentDescription = "Avatar", tint = Color.White, modifier = Modifier.padding(12.dp))
                                    }
                                    Spacer(Modifier.width(16.dp))
                                    Column {
                                        Text(custName, fontWeight = FontWeight.Bold, color = DeepNavyMain)
                                        if (custPhone.isNotBlank()) {
                                            Text(custPhone, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
                                        }
                                        Text("Home, Office", style = MaterialTheme.typography.bodySmall, color = TealAccentMain)
                                    }
                                }
                                HorizontalDivider(modifier = Modifier.padding(bottom = 8.dp))"""

content = content.replace(drawer_bad, drawer_good)

with open("/app/applet/app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
