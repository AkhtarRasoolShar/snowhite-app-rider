with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Update printReceipt to take appName
old_func = r'fun printReceipt\(context: Context, order: RiderOrder\) \{'
new_func = r'fun printReceipt(context: Context, order: RiderOrder, appName: String) {'
content = re.sub(old_func, new_func, content)

content = content.replace('${viewModel.appSettings.app_name ?: "Captain Portal"}', '${appName}')

# Find where printReceipt is called and pass the appName
old_call = r'printReceipt\(context, order\)'
new_call = r'printReceipt(context, order, viewModel.appSettings.app_name ?: "Captain Portal")'
content = re.sub(old_call, new_call, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
