with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

if "android.permission.ACCESS_FINE_LOCATION" not in content:
    content = content.replace(
        '<uses-permission android:name="android.permission.INTERNET" />',
        '<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />\n    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />'
    )
    with open('app/src/main/AndroidManifest.xml', 'w') as f:
        f.write(content)
