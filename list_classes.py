import sys
import zipfile

with zipfile.ZipFile('app/build/outputs/apk/debug/app-debug.apk', 'r') as z:
    for name in z.namelist():
        if name.endswith('.dex'):
            data = z.read(name)
            if b'Lcom/example/MainActivity;' in data:
                print(f"Found in {name}")
                idx = data.find(b'Lcom/example/MainActivity;')
                print(data[max(0, idx-10):idx+40])
