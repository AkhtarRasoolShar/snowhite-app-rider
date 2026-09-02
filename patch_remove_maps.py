with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_imports = """import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.rememberCameraPositionState
import com.google.maps.android.compose.CameraPositionState
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng"""
content = content.replace(target_imports, "")

target_map = """        // Google Map Box
        val karachi = LatLng(24.8607, 67.0011)
        val cameraPositionState = rememberCameraPositionState {
            position = CameraPosition.fromLatLngZoom(karachi, 12f)
        }
        
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
                .background(Color(0xFFE2E8F0))
        ) {
            GoogleMap(
                modifier = Modifier.fillMaxSize(),
                cameraPositionState = cameraPositionState
            )
        }"""

replace_map = """        // Static Placeholder Box (Map Removed)
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(180.dp)
                .background(DarkBlue),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Icon(Icons.Default.Radar, contentDescription = "Radar", tint = TealAccent, modifier = Modifier.size(64.dp))
                Spacer(Modifier.height(8.dp))
                Text("SCANNING ACTIVE ZONE", color = Color.White, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
                Text(zone.uppercase(), color = TealAccent, fontSize = 12.sp)
            }
        }"""
content = content.replace(target_map, replace_map)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
