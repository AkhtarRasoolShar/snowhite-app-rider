with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main = f.read()

main = main.replace('putInt("rider_id", data.id)', 'putString("rider_id", data.id ?: "")')
# fix where riderId is read from prefs
main = main.replace('_riderId.value = prefs.getInt("rider_id", -1)', 'val rId = prefs.getString("rider_id", "-1") ?: "-1"\n        _riderId.value = rId.toIntOrNull() ?: -1')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main)
