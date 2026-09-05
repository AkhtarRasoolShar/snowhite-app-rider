with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    c = f.read()

# fix acceptOrder
bad1 = """    } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to accept order", Toast.LENGTH_SHORT).show()
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Order acceptance queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.AcceptOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad1, "")

# fix rejectOrder
bad2 = """    } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to reject order", Toast.LENGTH_SHORT).show()
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Order rejection queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.RejectOrder(orderId)
                if (!pendingActions.contains(action)) pendingActions.add(action)
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad2, "")

# fix updateOrderStatus
bad3 = """    } else {
                    Toast.makeText(context, response.body()?.message ?: "Failed to update status", Toast.LENGTH_SHORT).show()
                }
                } catch (e: Exception) {
                android.util.Log.e("API_ERROR", "Fetch failed", e)
                Toast.makeText(context, "Network Error. Status update queued.", Toast.LENGTH_SHORT).show()
                val action = PendingAction.UpdateOrderStatus(orderId, newStatus)
                if (!pendingActions.contains(action)) pendingActions.add(action)
                } finally {
                _isLoading.value = false
            }
        }
    }"""
c = c.replace(bad3, "")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(c)
