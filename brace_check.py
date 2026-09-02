import sys
with open('app/src/main/java/com/example/MainActivity.kt') as f:
    lines = f.readlines()
open_c = 0
for i, line in enumerate(lines):
    open_c += line.count('{') - line.count('}')
    if open_c == 0:
        pass
    print(f"{i+1}: {open_c}")
