with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """
import retrofit2.Response
import retrofit2.http.*
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import com.google.gson.annotations.SerializedName
import com.google.gson.Gson
"""

content = content.replace("import retrofit2.http.Headers", imports + "\nimport retrofit2.http.Headers")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
