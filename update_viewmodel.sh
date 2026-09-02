#!/bin/bash
sed -i 's/if (response.isSuccessful) {/if (response.status == "success") {/g' /app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt
sed -i 's/_orders.value = response.body() ?: emptyList()/_orders.value = response.data/g' /app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt
sed -i 's/"Failed to fetch orders: ${response.code()}"/"Failed to fetch orders: ${response.status}"/g' /app/applet/app/src/main/java/com/example/viewmodel/SnowWhiteViewModel.kt
