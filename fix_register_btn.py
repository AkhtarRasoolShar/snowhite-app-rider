with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

old_btn = r'''                        Spacer\(Modifier\.height\(24\.dp\)\)
                        Button\(
                            onClick = \{ viewModel\.register\(name, phone, password, viewModel\.selectedHubs\.toList\(\), viewModel\.email, context\) \},
                            modifier = Modifier\.fillMaxWidth\(\)\.height\(50\.dp\),
                            colors = ButtonDefaults\.buttonColors\(containerColor = Color\(0xFF03045E\)\),
                            enabled = !isLoading && name\.isNotBlank\(\) && phone\.isNotBlank\(\) && password\.isNotBlank\(\) && viewModel\.selectedHubs\.isNotEmpty\(\)
                        \) \{
                            if \(isLoading\) CircularProgressIndicator\(color = Color\.White, modifier = Modifier\.size\(24\.dp\)\)
                            else Text\("REGISTER", color = Color\.White, fontWeight = FontWeight\.Bold\)
                        \}'''

new_btn = '''                        Spacer(Modifier.height(24.dp))
                        
                        val isFormValid = name.isNotBlank() && phone.isNotBlank() && password.isNotBlank() && viewModel.email.isNotBlank() && viewModel.selectedHubs.isNotEmpty()
                        
                        Button(
                            onClick = {
                                if (isFormValid) {
                                    viewModel.register(name, phone, password, viewModel.selectedHubs.toList(), viewModel.email, context)
                                } else {
                                    android.widget.Toast.makeText(context, "Please fill all fields and select at least one hub.", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.fillMaxWidth().height(50.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = if (isFormValid) Color(0xFF03045E) else Color.Gray),
                            enabled = !isLoading
                        ) {
                            if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                            else Text("REGISTER", color = Color.White, fontWeight = FontWeight.Bold)
                        }'''

content = re.sub(old_btn, new_btn, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
