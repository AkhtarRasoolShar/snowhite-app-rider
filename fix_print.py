with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('printReceipt(context, selectedOrderForUpdate!!)', 'printReceipt(context, selectedOrderForUpdate!!, viewModel.appSettings.app_name ?: "Captain Portal")')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
