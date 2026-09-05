import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# add import
if "import kotlinx.coroutines.flow.StateFlow" not in content:
    content = content.replace("import kotlinx.coroutines.flow.MutableStateFlow", "import kotlinx.coroutines.flow.MutableStateFlow\nimport kotlinx.coroutines.flow.StateFlow")

# find RiderViewModel
start = content.find('class RiderViewModel : ViewModel() {')
end = content.find('// --- Theme ---')

vm_content = content[start:end]

save_profile = """
    fun saveProfileDetails(context: Context, address: String, bankName: String, bankIban: String, qr1: String, qr2: String) {
        val prefs = context.getSharedPreferences("RiderPrefs", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putString("rider_address", address)
            putString("bank_name", bankName)
            putString("bank_iban", bankIban)
            putString("quick_reply_1", qr1)
            putString("quick_reply_2", qr2)
        }.apply()
        _homeAddress.value = address
        _bankName.value = bankName
        _bankIban.value = bankIban
        _quickReply1.value = qr1
        _quickReply2.value = qr2
        Toast.makeText(context, "Profile Saved Locally", Toast.LENGTH_SHORT).show()
    }
    
    fun logout(context: Context) {
        SessionManager.logout(context)
        _riderId.value = -1
    }
}
"""

vm_content = vm_content.replace('}\n\n', '}\n' + save_profile)

content = content[:start] + vm_content + content[end:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

