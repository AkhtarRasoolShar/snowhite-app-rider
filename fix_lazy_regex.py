import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# I will use a simple function replacing script using git history or restoring the original file and patching it.
import subprocess
subprocess.run(['git', 'checkout', 'app/src/main/java/com/example/MainActivity.kt'])

