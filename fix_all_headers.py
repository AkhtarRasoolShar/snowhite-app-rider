with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

import re
# Find all @POST that have @Body
pattern = r'(\s*)@POST\("routes\.php\?action=([^"]+)"\)\s*suspend fun [^)]+\(@Body'

def replacer(match):
    # Only add @Headers if it is not already there
    indent = match.group(1)
    full_match = match.group(0)
    
    # Let's just do a simpler search and replace for each post
    return full_match

lines = content.split('\n')
new_lines = []
for i, line in enumerate(lines):
    if '@POST' in line and 'routes.php' in line:
        if i > 0 and '@Headers' not in lines[i-1]:
            # extract indent
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(indent + '@Headers("Content-Type: application/json")')
    new_lines.append(line)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write('\n'.join(new_lines))

