import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Use regex to find and remove the OrderChatScreen function in MainActivity
pattern = r'@OptIn\(ExperimentalMaterial3Api::class\)\s*@Composable\s*fun OrderChatScreen.*?\} // End items\s*\}\s*\}\s*\}'
# Actually regex is risky. Let's just find the exact index.

start_str = "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun OrderChatScreen"
start_idx = content.find(start_str)

if start_idx != -1:
    # Find the matching closing brace. 
    # Let's write a simple bracket matcher
    idx = start_idx
    open_count = 0
    found_first = False
    
    while idx < len(content):
        if content[idx] == '{':
            open_count += 1
            found_first = True
        elif content[idx] == '}':
            open_count -= 1
            
        if found_first and open_count == 0:
            break
        idx += 1
        
    end_idx = idx + 1
    content = content[:start_idx] + content[end_idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Removed OrderChatScreen from MainActivity")
else:
    print("OrderChatScreen not found")

