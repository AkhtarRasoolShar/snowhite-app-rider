import sys

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix SnowWhiteLogo
old_logo = """@Composable
fun SnowWhiteLogo(modifier: Modifier = Modifier) {
    AsyncImage(
        model = "https://snowhite.com.pk/wp-content/uploads/2021/04/snowhite-logo.png",
        contentDescription = "SnowWhite Logo",
        contentScale = ContentScale.Fit,
        modifier = modifier
    )
}"""

new_logo = """@Composable
fun SnowWhiteLogo(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.LocalLaundryService,
            contentDescription = "SnoWhite Logo",
            tint = Color.White,
            modifier = Modifier.size(40.dp)
        )
        Spacer(Modifier.width(12.dp))
        Text(
            text = "SnoWhite",
            fontSize = 32.sp,
            fontWeight = FontWeight.Black,
            color = Color.White
        )
    }
}"""
content = content.replace(old_logo, new_logo)

# Fix Background URLs
old_url = '"https://images.unsplash.com/photo-1545060894-7b57f0f6c271?q=80&w=1000"'
new_url = '"https://images.pexels.com/photos/5591581/pexels-photo-5591581.jpeg?auto=compress&cs=tinysrgb&w=1080"'
content = content.replace(old_url, new_url)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

print("Logo updated:", old_logo not in content and new_logo in content)
print("URL updated:", new_url in content)
