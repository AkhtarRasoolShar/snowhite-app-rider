with open("/app/applet/app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    content = f.read()

import re
content = re.sub(
    r"val colorScheme =[\s\S]*?MaterialTheme\(",
    "val colorScheme = LightColorScheme\n  MaterialTheme(",
    content
)

with open("/app/applet/app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(content)
