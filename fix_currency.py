with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace('"${viewModel.appSettings ?: "PKR"} $totalEarnings"', '"PKR $totalEarnings"')
content = content.replace('"${viewModel.appSettings ?: "PKR"} ${order.totalAmount}"', '"PKR ${order.totalAmount}"')

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
