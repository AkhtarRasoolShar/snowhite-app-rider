with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

if 'logging-interceptor' not in content:
    content = content.replace(
        'dependencies {',
        'dependencies {\n    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")'
    )
    with open('app/build.gradle.kts', 'w') as f:
        f.write(content)
