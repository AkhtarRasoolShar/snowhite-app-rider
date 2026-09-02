import sys
import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Extract LoginScreen
login_start = content.find('@Composable\nfun LoginScreen')
if login_start == -1:
    print("LoginScreen not found")
    sys.exit(1)

# Find the end of LoginScreen
brace_count = 0
in_function = False
login_end = -1
for i in range(login_start, len(content)):
    if content[i] == '{':
        brace_count += 1
        in_function = True
    elif content[i] == '}':
        brace_count -= 1
        if in_function and brace_count == 0:
            login_end = i + 1
            break

# Extract RegisterScreen
register_start = content.find('@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun RegisterScreen')
if register_start == -1:
    print("RegisterScreen not found")
    sys.exit(1)

brace_count = 0
in_function = False
register_end = -1
for i in range(register_start, len(content)):
    if content[i] == '{':
        brace_count += 1
        in_function = True
    elif content[i] == '}':
        brace_count -= 1
        if in_function and brace_count == 0:
            register_end = i + 1
            break

login_replacement = """@Composable
fun LoginScreen(viewModel: RiderViewModel, onNavigateToRegister: () -> Unit) {
    val context = LocalContext.current
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1545060894-7b57f0f6c271?q=80&w=1000",
            contentDescription = "Laundry Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.65f)))
        
        Column(
            modifier = Modifier.fillMaxSize().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            SnowWhiteLogo(modifier = Modifier.height(60.dp).fillMaxWidth())
            Spacer(Modifier.height(16.dp))
            Text("Captain Portal", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color.White)
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
                        onValueChange = { phone = it },
                        label = { Text("Phone Number") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    Spacer(Modifier.height(16.dp))
                    OutlinedTextField(
                        value = password,
                        onValueChange = { password = it },
                        label = { Text("Password") },
                        modifier = Modifier.fillMaxWidth(),
                        visualTransformation = PasswordVisualTransformation(),
                        singleLine = true
                    )
                    Spacer(Modifier.height(24.dp))
                    Button(
                        onClick = { viewModel.login(phone, password, context) },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F172A)),
                        enabled = !isLoading && phone.isNotBlank() && password.isNotBlank()
                    ) {
                        if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                        else Text("LOGIN", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            TextButton(onClick = onNavigateToRegister) {
                Text("New Rider? Apply Here", color = Color(0xFF14B8A6), fontWeight = FontWeight.Bold)
            }
        }
    }
}"""

register_replacement = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterScreen(viewModel: RiderViewModel, onNavigateToLogin: () -> Unit) {
    val context = LocalContext.current
    var name by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var zone by remember { mutableStateOf("") }
    var expandedZone by remember { mutableStateOf(false) }
    
    val zones = listOf("Clifton", "Tariq Road", "DHA", "Gulshan")
    val isLoading by viewModel.isLoading.collectAsState()
    val authError by viewModel.authError.collectAsState()

    Box(modifier = Modifier.fillMaxSize()) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1545060894-7b57f0f6c271?q=80&w=1000",
            contentDescription = "Laundry Background",
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.65f)))
        
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            item {
                Spacer(Modifier.height(24.dp))
                SnowWhiteLogo(modifier = Modifier.height(50.dp).fillMaxWidth())
                Spacer(Modifier.height(16.dp))
                Text("Captain Portal", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = Color.White)
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
                            onValueChange = { phone = it },
                            label = { Text("Phone Number") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(Modifier.height(16.dp))
                        OutlinedTextField(
                            value = password,
                            onValueChange = { password = it },
                            label = { Text("Password") },
                            modifier = Modifier.fillMaxWidth(),
                            visualTransformation = PasswordVisualTransformation()
                        )
                        Spacer(Modifier.height(16.dp))
                        
                        Text("Select Active Hubs:", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
                        var selectedZones by remember { mutableStateOf(setOf<String>()) }
                        zones.forEach { selection ->
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                                Checkbox(
                                    checked = selectedZones.contains(selection),
                                    onCheckedChange = { isChecked ->
                                        selectedZones = if (isChecked) selectedZones + selection else selectedZones - selection
                                    },
                                    colors = CheckboxDefaults.colors(checkedColor = TealAccent)
                                )
                                Text(selection, color = DarkBlue)
                            }
                        }
                        
                        Spacer(Modifier.height(24.dp))
                        val joinedZones = selectedZones.joinToString(", ")
                        Button(
                            onClick = { viewModel.register(name, phone, password, joinedZones, context) },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F172A)),
                            enabled = !isLoading && name.isNotBlank() && phone.isNotBlank() && password.isNotBlank() && selectedZones.isNotEmpty()
                        ) {
                            if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                            else Text("REGISTER", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
                
                Spacer(Modifier.height(24.dp))
                TextButton(onClick = onNavigateToLogin) {
                    Text("Back to Login", color = Color(0xFF14B8A6), fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(24.dp))
            }
        }
    }
}"""

# Perform replacements backwards so indices don't shift
content = content[:register_start] + register_replacement + content[register_end:]
content = content[:login_start] + login_replacement + content[login_end:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

print("Replacement successful")
