with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# 1. Update the Header Block
old_header = r'''Spacer\(Modifier\.height\(24\.dp\)\)\s*SnowhiteLogo\(modifier = Modifier\.height\(50\.dp\)\.fillMaxWidth\(\)\)\s*Spacer\(Modifier\.height\(16\.dp\)\)\s*Text\("Captain Portal", fontSize = 24\.sp, fontWeight = FontWeight\.ExtraBold, color = Color\.White\)\s*Spacer\(Modifier\.height\(32\.dp\)\)'''

new_header = '''Spacer(Modifier.height(24.dp))
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                        coil.compose.AsyncImage(
                            model = viewModel.appSettings.logo_url,
                            contentDescription = "App Logo",
                            modifier = Modifier.size(60.dp)
                        )
                    } else {
                        Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(60.dp), tint = Color.White)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = viewModel.appSettings.app_name ?: "Captain Portal",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Text("Rider Registration", color = Color.White.copy(alpha = 0.8f))
                }
                Spacer(Modifier.height(32.dp))'''

content = re.sub(old_header, new_header, content, flags=re.DOTALL)

# 2. Update the RegisterScreen signature and var declarations to use ViewModel state for email/hubs
# The vars:
#    var name by remember { mutableStateOf("") }
#    var phone by remember { mutableStateOf("") }
#    var password by remember { mutableStateOf("") }
#    var zone by remember { mutableStateOf("") }
#    var expandedZone by remember { mutableStateOf(false) }
#       
#    val zones = listOf("Clifton", "Tariq Road", "DHA", "Gulshan")

old_vars = r'''var name by remember \{ mutableStateOf\(""\) \}\s*var phone by remember \{ mutableStateOf\(""\) \}\s*var password by remember \{ mutableStateOf\(""\) \}\s*var zone by remember \{ mutableStateOf\(""\) \}\s*var expandedZone by remember \{ mutableStateOf\(false\) \}\s*val zones = listOf\("Clifton", "Tariq Road", "DHA", "Gulshan"\)'''

new_vars = '''var name by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    '''
content = re.sub(old_vars, new_vars, content, flags=re.DOTALL)

# 3. Add Email Field and update hubs rendering
old_form = r'''OutlinedTextField\(\s*value = password,\s*onValueChange = \{ password = it; viewModel\.clearError\(\) \},\s*label = \{ Text\("Password"\) \},\s*modifier = Modifier\.fillMaxWidth\(\),\s*visualTransformation = PasswordVisualTransformation\(\)\s*\)\s*Spacer\(Modifier\.height\(16\.dp\)\)\s*Text\("Select Active Hubs:", fontWeight = FontWeight\.Bold, color = DarkBlue, modifier = Modifier\.fillMaxWidth\(\), textAlign = TextAlign\.Start\)\s*var selectedZones by remember \{ mutableStateOf\(setOf<String>\(\)\) \}\s*zones\.forEach \{ selection ->\s*Row\(verticalAlignment = Alignment\.CenterVertically, modifier = Modifier\.fillMaxWidth\(\)\) \{\s*Checkbox\(\s*checked = selectedZones\.contains\(selection\),\s*onCheckedChange = \{ isChecked ->\s*selectedZones = if \(isChecked\) selectedZones \+ selection else selectedZones - selection\s*\},\s*colors = CheckboxDefaults\.colors\(checkedColor = TealAccent\)\s*\)\s*Text\(selection, color = DarkBlue\)\s*\}\s*\}\s*Spacer\(Modifier\.height\(24\.dp\)\)\s*val joinedZones = selectedZones\.joinToString\(", "\)\s*Button\(\s*onClick = \{ viewModel\.register\(name, phone, password, joinedZones, context\) \},\s*modifier = Modifier\.fillMaxWidth\(\)\.height\(50\.dp\),\s*colors = ButtonDefaults\.buttonColors\(containerColor = Color\(0xFF03045E\)\),\s*enabled = !isLoading && name\.isNotBlank\(\) && phone\.isNotBlank\(\) && password\.isNotBlank\(\) && selectedZones\.isNotEmpty\(\)\s*\)'''

new_form = '''OutlinedTextField(
                            value = password,
                            onValueChange = { password = it; viewModel.clearError() },
                            label = { Text("Password") },
                            modifier = Modifier.fillMaxWidth(),
                            visualTransformation = PasswordVisualTransformation(),
                            singleLine = true
                        )
                        Spacer(Modifier.height(16.dp))
                        OutlinedTextField(
                            value = viewModel.email,
                            onValueChange = { viewModel.email = it; viewModel.clearError() },
                            label = { Text("Email") },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                        Spacer(Modifier.height(16.dp))
                        
                        Text("Select Active Hubs:", fontWeight = FontWeight.Bold, color = DarkBlue, modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
                        
                        viewModel.availableHubs.forEach { hub ->
                            val hubName = hub.name ?: "Unknown"
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                                Checkbox(
                                    checked = viewModel.selectedHubs.contains(hubName),
                                    onCheckedChange = { isChecked ->
                                        viewModel.selectedHubs = if (isChecked) viewModel.selectedHubs + hubName else viewModel.selectedHubs - hubName
                                    },
                                    colors = CheckboxDefaults.colors(checkedColor = TealAccent)
                                )
                                Text(hubName, color = DarkBlue)
                            }
                        }
                        
                        Spacer(Modifier.height(24.dp))
                        Button(
                            onClick = { viewModel.register(name, phone, password, viewModel.selectedHubs.toList(), viewModel.email, context) },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF03045E)),
                            enabled = !isLoading && name.isNotBlank() && phone.isNotBlank() && password.isNotBlank() && viewModel.selectedHubs.isNotEmpty()
                        )'''
content = re.sub(old_form, new_form, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
