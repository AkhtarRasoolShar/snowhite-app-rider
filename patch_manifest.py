import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target = '            android:theme="@style/Theme.MyApplication"\n        android:enableOnBackInvokedCallback="true">'
replacement = '            android:theme="@style/Theme.MyApplication"\n            android:windowSoftInputMode="adjustResize"\n            android:enableOnBackInvokedCallback="true">'

if target in content:
    content = content.replace(target, replacement)
else:
    print("Not found, trying alternative")
    target2 = 'android:theme="@style/Theme.MyApplication"'
    replacement2 = 'android:theme="@style/Theme.MyApplication"\n            android:windowSoftInputMode="adjustResize"'
    content = content.replace(target2, replacement2)

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
