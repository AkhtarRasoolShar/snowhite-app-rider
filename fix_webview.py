with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_func = "fun printReceipt(context: Context, order: RiderOrder) {"
new_func = """private var keepAliveWebView: android.webkit.WebView? = null

fun printReceipt(context: Context, order: RiderOrder) {"""

content = content.replace(old_func, new_func)

old_print = "val webView = android.webkit.WebView(context)"
new_print = """val webView = android.webkit.WebView(context)
    keepAliveWebView = webView"""

content = content.replace(old_print, new_print)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
