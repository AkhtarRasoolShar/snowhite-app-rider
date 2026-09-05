with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    c = f.read()

bad_login = """    } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update profile", Toast.LENGTH_SHORT).show()
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad_login, "")

bad_fetch = """    } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch orders", Toast.LENGTH_SHORT).show()
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad_fetch, "")

bad_register = """    } else {
                    _authError.value = "Server error. Try again."
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                _authError.value = "Network Error. Please check connection."
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad_register, "")

bad_login_2 = """    } else {
                    _authError.value = "Server error. Try again."
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                _authError.value = "Network Error. Please check connection."
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad_login_2, "")

bad_fetch_my = """    } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to fetch history", Toast.LENGTH_SHORT).show()
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error", Toast.LENGTH_SHORT).show()
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad_fetch_my, "")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(c)
