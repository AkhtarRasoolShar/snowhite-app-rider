with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if 'HttpLoggingInterceptor' not in content:
    content = content.replace(
        'import okhttp3.OkHttpClient',
        'import okhttp3.OkHttpClient\nimport okhttp3.logging.HttpLoggingInterceptor'
    )
    
    old_client = """    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()"""
        
    new_client = """    private val logging = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
    private val client = OkHttpClient.Builder()
        .addInterceptor(logging)
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()"""
        
    content = content.replace(old_client, new_client)
    
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
