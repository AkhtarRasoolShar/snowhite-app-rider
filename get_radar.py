with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start = content.find("fun RadarScreen(viewModel: RiderViewModel)")
end = content.find("fun StatusBadge(status: String)", start)
print(content[start:end])
