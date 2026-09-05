import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix repeated annotations
content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalMaterial3Api::class)")
content = content.replace("@Composable\n@Composable", "@Composable")
content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable")

# Add the proper import for items
if "import androidx.compose.foundation.lazy.grid.items" not in content:
    content = content.replace("import androidx.compose.foundation.lazy.grid.LazyVerticalGrid", "import androidx.compose.foundation.lazy.grid.LazyVerticalGrid\nimport androidx.compose.foundation.lazy.grid.items")
    # If the file doesn't have the LazyVerticalGrid import, add it at the top
    if "import androidx.compose.foundation.lazy.grid.items" not in content:
        import_stmt = "import androidx.compose.foundation.lazy.grid.*\n"
        content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\n" + import_stmt)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
