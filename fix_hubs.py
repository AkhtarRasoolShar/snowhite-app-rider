with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

old_fetch = r'''                // Fallback in case of HTTP 500 or Network Error
                availableHubs = listOf\(
                    Hub\(1, "Clifton"\),
                    Hub\(2, "Tariq Road"\),
                    Hub\(3, "DHA"\),
                    Hub\(4, "Gulshan"\)
                \)'''

new_fetch = '''                // Fallback in case of HTTP 500 or Network Error
                availableHubs = listOf(
                    Hub(1, "Clifton"),
                    Hub(2, "Tariq Road"),
                    Hub(3, "DHA"),
                    Hub(4, "Gulshan")
                )
                // Clear the error message since we are using fallback data successfully
                errorMessage = null'''

content = re.sub(old_fetch, new_fetch, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
