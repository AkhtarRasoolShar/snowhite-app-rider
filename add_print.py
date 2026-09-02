with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

print_func = """
fun printReceipt(context: Context, order: RiderOrder) {
    val printManager = context.getSystemService(Context.PRINT_SERVICE) as android.print.PrintManager
    val webView = android.webkit.WebView(context)
    
    val itemsHtml = order.items?.joinToString("") { 
        "<tr><td style='padding:8px; border-bottom:1px solid #ddd;'>${it.name ?: "Item"}</td><td style='padding:8px; border-bottom:1px solid #ddd;'>${it.quantity ?: 1}x</td></tr>"
    } ?: "<tr><td colspan='2'>No items</td></tr>"
    
    val htmlDocument = \"\"\"
        <html>
        <head>
            <style>
                body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 20px; color: #03045E; }
                .header { text-align: center; margin-bottom: 20px; }
                .title { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
                .subtitle { font-size: 14px; color: #666; margin-bottom: 20px; }
                .details { margin-bottom: 20px; font-size: 16px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th { background-color: #00B4D8; color: white; padding: 10px; text-align: left; }
                .total { font-size: 18px; font-weight: bold; text-align: right; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">SnowWhite Captain</div>
                <div class="subtitle">Receipt - Order #${order.order_id ?: "N/A"}</div>
            </div>
            <div class="details">
                <p><strong>Date:</strong> ${order.date ?: "N/A"}</p>
                <p><strong>Address:</strong> ${order.pickup_address ?: "N/A"}</p>
            </div>
            <table>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                </tr>
                $itemsHtml
            </table>
            <div class="total">
                Total: PKR ${order.total_amount ?: "0"}
            </div>
        </body>
        </html>
    \"\"\".trimIndent()
    
    webView.webViewClient = object : android.webkit.WebViewClient() {
        override fun onPageFinished(view: android.webkit.WebView, url: String) {
            val printAdapter = view.createPrintDocumentAdapter("Receipt_${order.order_id}")
            printManager.print("Receipt_${order.order_id}", printAdapter, android.print.PrintAttributes.Builder().build())
        }
    }
    
    webView.loadDataWithBaseURL(null, htmlDocument, "text/HTML", "UTF-8", null)
}

// --- Screens ---
"""
content = content.replace("// --- Screens ---", print_func)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
