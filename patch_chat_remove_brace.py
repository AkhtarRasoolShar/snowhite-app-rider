import re

with open("app/src/main/java/com/example/ChatUI.kt", "r") as f:
    content = f.read()

target = """                }
            }
        }
        }
    ) { padding ->"""

replacement = """                }
            }
        }
    ) { padding ->"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ChatUI.kt", "w") as f:
    f.write(content)
