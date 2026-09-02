fun ProfileScreen(viewModel: RiderViewModel) {
    val context = LocalContext.current
    val name by viewModel.riderName.collectAsState()
    val zone by viewModel.riderZone.collectAsState()
    
    var address by remember { mutableStateOf(viewModel.homeAddress.value) }
    var bankName by remember { mutableStateOf(viewModel.bankName.value) }
    var bankIban by remember { mutableStateOf(viewModel.bankIban.value) }

    Box(modifier = Modifier.fillMaxSize().background(SoftWhite)) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1080&auto=format&fit=crop",
            contentDescription = "Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize(),
            alpha = 0.05f
        )
        Column(modifier = Modifier.fillMaxSize()) {
        Surface(color = Color.White, shadowElevation = 4.dp, modifier = Modifier.fillMaxWidth()) {
            Row(modifier = Modifier.padding(16.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                SnowWhiteLogo(modifier = Modifier.height(40.dp))
                Spacer(Modifier.width(12.dp))
                Text("Captain Profile", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = DarkBlue)
            }
        }
        
        LazyColumn(contentPadding = PaddingValues(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxSize()) {
            item {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.AccountCircle, contentDescription = "Avatar", tint = DarkBlue, modifier = Modifier.size(64.dp))
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text(name, fontWeight = FontWeight.Bold, fontSize = 20.sp, color = DarkBlue)
                        Text("Hubs: $zone", color = TealAccent, fontWeight = FontWeight.Bold)
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
}
