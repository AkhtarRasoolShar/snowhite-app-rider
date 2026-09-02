import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix MainAppScreen extra brace
bad_main_end = """        }
    }
    }
}

@Composable
fun RadarScreen"""
good_main_end = """        }
    }
}

@Composable
fun RadarScreen"""
content = content.replace(bad_main_end, good_main_end)

# Let's fix HistoryScreen
bad_history_end = """        }
    }
    }

    if (selectedOrderForUpdate != null) {"""
good_history_end = """        }
    }

    if (selectedOrderForUpdate != null) {"""
content = content.replace(bad_history_end, good_history_end)

# Let's fix ProfileScreen
bad_profile_end = """        }
    }
    }
}

@Composable
fun MainAppScreen"""
good_profile_end = """        }
    }
}

@Composable
fun MainAppScreen"""
content = content.replace(bad_profile_end, good_profile_end)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
