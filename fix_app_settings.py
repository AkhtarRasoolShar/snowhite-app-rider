with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('val appSettings by androidx.compose.runtime.mutableStateOf(AppSettings())', 'var appSettings by androidx.compose.runtime.mutableStateOf(AppSettings())')
content = content.replace('viewModel.appSettings.currency', 'viewModel.appSettings')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
