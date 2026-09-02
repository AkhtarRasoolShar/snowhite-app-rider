import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

def print_func(name):
    print(f"--- {name} ---")
    start = content.find(f"fun {name}")
    end = content.find("fun ", start + 10)
    if end == -1: end = len(content)
    print(content[start:start+500])

print_func("RadarScreen")
print_func("HistoryScreen")
print_func("ProfileScreen")

