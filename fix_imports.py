with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("import retrofit2.http.Headers"): continue
    if line.startswith("import android.util.Log"): continue
    if line.startswith("import androidx.navigation.NavController") and not "compose" in line: continue
    if line.startswith("import androidx.navigation.NavHostController") and not "compose" in line: continue
    new_lines.append(line)

final_lines = []
for line in new_lines:
    final_lines.append(line)
    if line.startswith("package com.example"):
        final_lines.append("import retrofit2.http.Headers\n")
        final_lines.append("import android.util.Log\n")
        final_lines.append("import androidx.navigation.NavController\n")
        final_lines.append("import androidx.navigation.NavHostController\n")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(final_lines)

