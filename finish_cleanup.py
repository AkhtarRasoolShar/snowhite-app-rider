with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# 1. Update LoginScreen Header
old_login_header = r'''SnowhiteLogo\(modifier = Modifier\.height\(60\.dp\)\.fillMaxWidth\(\)\)\s*Spacer\(Modifier\.height\(16\.dp\)\)\s*Text\("Captain Portal", fontSize = 24\.sp, fontWeight = FontWeight\.ExtraBold, color = Color\.White\)\s*Spacer\(Modifier\.height\(32\.dp\)\)'''

new_login_header = '''Column(horizontalAlignment = Alignment.CenterHorizontally) {
                if (!viewModel.appSettings.logo_url.isNullOrEmpty()) {
                    coil.compose.AsyncImage(
                        model = viewModel.appSettings.logo_url,
                        contentDescription = "App Logo",
                        modifier = Modifier.size(60.dp)
                    )
                } else {
                    Icon(Icons.Default.LocalShipping, contentDescription = null, modifier = Modifier.size(60.dp), tint = Color.White)
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = viewModel.appSettings.app_name ?: "Captain Portal",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Text("Rider Login", color = Color.White.copy(alpha = 0.8f))
            }
            Spacer(Modifier.height(32.dp))'''

content = re.sub(old_login_header, new_login_header, content, flags=re.DOTALL)


# 2. Update Receipt HTML
content = content.replace('<div class="title">Snowhite Captain</div>', '<div class="title">${viewModel.appSettings.app_name ?: "Captain Portal"}</div>')


# 3. Remove SnowhiteLogo function (around 15 lines)
snowhite_func = r'''@Composable\s*fun SnowhiteLogo\(modifier: Modifier = Modifier\) \{.*?(?=@Composable)'''
content = re.sub(snowhite_func, '', content, flags=re.DOTALL)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
