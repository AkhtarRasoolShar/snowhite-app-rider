with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import re

# Login Screen
old_login_col = r'''        Column\(
            modifier = Modifier\.fillMaxSize\(\)\.padding\(24\.dp\),
            horizontalAlignment = Alignment\.CenterHorizontally,
            verticalArrangement = Arrangement\.Center
        \) \{'''
new_login_col = '''        Column(
            modifier = Modifier.fillMaxSize().imePadding().padding(24.dp).verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {'''
content = re.sub(old_login_col, new_login_col, content)

# Register Screen
old_reg_col = r'''        LazyColumn\(
            modifier = Modifier\.fillMaxSize\(\)\.padding\(24\.dp\),
            horizontalAlignment = Alignment\.CenterHorizontally,
            verticalArrangement = Arrangement\.Center
        \) \{'''
new_reg_col = '''        LazyColumn(
            modifier = Modifier.fillMaxSize().imePadding().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {'''
content = re.sub(old_reg_col, new_reg_col, content)

# MainAppScreen (adding imePadding to the NavHost or Box)
old_main_box = r'''    \) \{ padding ->
        Box\(modifier = Modifier\.padding\(padding\)\.fillMaxSize\(\)\) \{'''
new_main_box = '''    ) { padding ->
        Box(modifier = Modifier.padding(padding).fillMaxSize().imePadding()) {'''
content = re.sub(old_main_box, new_main_box, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
