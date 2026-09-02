#!/bin/bash
FILE="/app/applet/app/src/main/java/com/example/MainActivity.kt"

# 1. Update Drawer onClick listeners
sed -i 's/onClick = { scope.launch { drawerState.close() } }/onClick = { scope.launch { drawerState.close() }; navController.navigate("wallet") }/' "$FILE" # First match is wallet, wait I should be precise

sed -i 's/label = { Text("My Wallet & Top-up") },\n                                    icon = { Icon(Icons.Default.AccountBalanceWallet, null) },\n                                    selected = false,\n                                    onClick = { scope.launch { drawerState.close() } }/label = { Text("My Wallet \& Top-up") },\n                                    icon = { Icon(Icons.Default.AccountBalanceWallet, null) },\n                                    selected = false,\n                                    onClick = { scope.launch { drawerState.close() }; navController.navigate("wallet") }/g' "$FILE"

