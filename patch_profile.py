import re
with open("/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add imports
if "import com.example.viewmodel.SnowWhiteViewModel" not in content:
    content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\nimport com.example.viewmodel.SnowWhiteViewModel\nimport androidx.compose.runtime.collectAsState\nimport androidx.compose.runtime.getValue")

# Change signature
content = content.replace("fun ProfileScreen(onOpenDrawer: () -> Unit)", "fun ProfileScreen(viewModel: SnowWhiteViewModel, onOpenDrawer: () -> Unit, onLogout: () -> Unit)")

# Extract fields
content = content.replace("var notificationsEnabled by remember { mutableStateOf(true) }", "var notificationsEnabled by remember { mutableStateOf(true) }\n    val custName by viewModel.customerName.collectAsState()\n    val custPhone by viewModel.customerPhone.collectAsState()")

# Remove dummy
content = content.replace('Text("Zubair Khan",', 'Text(custName,')
content = content.replace('Text("akhtarrasool275@gmail.com",', '// Removed email since backend doesnt provide it')
content = content.replace('Text("+92 300 1234567",', 'Text(if (custPhone.isNotBlank()) custPhone else "No phone provided",')

# Logout
content = content.replace('Button(onClick = { },', 'Button(onClick = onLogout,')

with open("/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
