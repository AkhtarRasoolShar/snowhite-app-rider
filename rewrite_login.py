import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix LoginScreen fields to clear error
content = content.replace("onValueChange = { phone = it }", "onValueChange = { phone = it; viewModel.clearError() }")
content = content.replace("onValueChange = { password = it }", "onValueChange = { password = it; viewModel.clearError() }")

# Fix LoginScreen Button click
old_btn = "viewModel.login(phone, password, context)"
new_btn = "viewModel.login(phone, password, context, onSuccess = { /* App state automatically switches based on riderId */ })"
content = content.replace(old_btn, new_btn)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
