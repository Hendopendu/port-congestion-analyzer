# scripts/simple_test.py
print("=" * 50)
print("🎉 DOCKER IS WORKING!")
print("✅ Python is running inside Docker container")
print("=" * 50)

# Test basic imports
try:
    import requests
    print("✅ requests module imported successfully")
except ImportError as e:
    print(f"❌ requests error: {e}")

try:
    import pandas as pd
    print("✅ pandas module imported successfully")
    
    # Simple test
    data = {'test': [1, 2, 3]}
    df = pd.DataFrame(data)
    print("✅ pandas basic functionality works")
    
except ImportError as e:
    print(f"❌ pandas error: {e}")

try:
    import numpy as np
    print("✅ numpy module imported successfully")
except ImportError as e:
    print(f"❌ numpy error: {e}")

print("\n" + "=" * 50)
print("🚀 Ready to start web scraping!")
print("=" * 50)