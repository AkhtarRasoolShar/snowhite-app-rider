with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I will find QuickRepliesScreen and qualify the Modifiers
start = content.find("fun QuickRepliesScreen")
end = content.find("fun onCreate", start)
sub = content[start:end]
sub = sub.replace("Modifier.", "androidx.compose.ui.Modifier.")
# Some might become androidx.compose.ui.androidx.compose.ui.Modifier, let's fix that
sub = sub.replace("androidx.compose.ui.androidx.compose.ui.Modifier", "androidx.compose.ui.Modifier")

content = content[:start] + sub + content[end:]

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
