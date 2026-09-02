with open("/app/applet/app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    content = f.read()

content = content.replace(
    "val colorScheme = when {",
    "val colorScheme = LightColorScheme /* Enforce Light Theme */\n    /* when {"
)
content = content.replace(
    "        else -> LightColorScheme\n    }",
    "        else -> LightColorScheme\n    } */"
)

with open("/app/applet/app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(content)
