with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
seen = set()

for line in lines:
    if line.startswith("import "):
        if line not in seen:
            seen.add(line)
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(new_lines)
