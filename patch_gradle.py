with open("/app/applet/app/build.gradle.kts", "r") as f:
    content = f.read()

if "converter-gson" not in content:
    content = content.replace("dependencies {", "dependencies {\n  implementation(\"com.squareup.retrofit2:converter-gson:2.11.0\")\n  implementation(\"com.google.code.gson:gson:2.10.1\")\n  implementation(\"io.coil-kt:coil-compose:2.6.0\")")
    with open("/app/applet/app/build.gradle.kts", "w") as f:
        f.write(content)
