with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Name
old_name = r'onValueChange = \{ name = it \}'
new_name = 'onValueChange = { name = it; viewModel.errorMessage = null }'
content = content.replace(old_name, new_name)

# Phone
old_phone = r'onValueChange = \{ phone = it; viewModel\.clearError\(\) \}'
new_phone = 'onValueChange = { phone = it; viewModel.clearError(); viewModel.errorMessage = null }'
content = content.replace(old_phone, new_phone)

# Password
old_password = r'onValueChange = \{ password = it; viewModel\.clearError\(\) \}'
new_password = 'onValueChange = { password = it; viewModel.clearError(); viewModel.errorMessage = null }'
content = content.replace(old_password, new_password)

# Email
old_email = r'onValueChange = \{ viewModel\.email = it; viewModel\.clearError\(\) \}'
new_email = 'onValueChange = { viewModel.email = it; viewModel.clearError(); viewModel.errorMessage = null }'
content = content.replace(old_email, new_email)

# Checkbox
old_checkbox = r'''onCheckedChange = \{ isChecked ->
                                        viewModel\.selectedHubs = if \(isChecked\) viewModel\.selectedHubs \+ hubName else viewModel\.selectedHubs - hubName
                                    \}'''
new_checkbox = '''onCheckedChange = { isChecked ->
                                        viewModel.selectedHubs = if (isChecked) viewModel.selectedHubs + hubName else viewModel.selectedHubs - hubName
                                        viewModel.errorMessage = null
                                    }'''
content = re.sub(old_checkbox, new_checkbox, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
