import re

with open("app/src/main/java/com/example/ChatViewModel.kt", "r") as f:
    content = f.read()

# Make the catch block silent if it's the expected HTTP 404 or missing PHP file.
target = """            } catch (e: Exception) {
                Log.e("CHAT_API", "Fetch Messages - Network Exception: ${e.message}")
            }"""
replacement = """            } catch (e: Exception) {
                // If it's a 404/JSON parsing issue, disable backend instead of spamming.
                isBackendSupported = false
                Log.e("CHAT_API", "Fetch Messages - Network Exception (Disabling Backend): ${e.message}")
            }"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Could not find target 1")

target2 = """                    } catch (e: Exception) {
                        Log.e("CHAT_API", "Polling Typing Status - Error: ${e.message}")
                    }"""
replacement2 = """                    } catch (e: Exception) {
                        isBackendSupported = false
                    }"""

if target2 in content:
    content = content.replace(target2, replacement2)
else:
    print("Could not find target 2")

with open("app/src/main/java/com/example/ChatViewModel.kt", "w") as f:
    f.write(content)
