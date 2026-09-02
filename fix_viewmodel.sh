#!/bin/bash
sed -i 's/if (response.status == "success") {/if (response.isSuccessful) {/g' /app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt
