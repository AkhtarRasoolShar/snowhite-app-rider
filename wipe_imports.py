with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# find the last import
end_imports = content.rfind("import ")
end_line = content.find("\n", end_imports)

clean_imports = """package com.example

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Geocoder
import android.location.Location
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.foundation.shape.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.core.app.ActivityCompat
import androidx.core.view.WindowCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.compose.*
import androidx.work.*
import coil.compose.AsyncImage
import com.example.ui.theme.RiderTheme
import com.google.android.gms.location.LocationServices
import retrofit2.http.Headers
import java.util.concurrent.TimeUnit
"""

# Let's clean up any fully-qualified names in MainActivity that might cause errors
new_content = clean_imports + content[end_line:]

# Fix any `androidx.compose.ui.androidx.compose.ui` issues
new_content = new_content.replace("androidx.compose.ui.androidx.compose.ui", "androidx.compose.ui")
new_content = new_content.replace("androidx.compose.ui.Modifier", "Modifier")
new_content = new_content.replace("androidx.activity.compose.setContent", "setContent")
new_content = new_content.replace("androidx.navigation.compose.composable", "composable")
new_content = new_content.replace("androidx.compose.foundation.shape.RoundedCornerShape", "RoundedCornerShape")
new_content = new_content.replace("androidx.activity.enableEdgeToEdge", "enableEdgeToEdge")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(new_content)
