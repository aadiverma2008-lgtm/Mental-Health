"""
Quick test script to verify backend is working
"""
import requests
import sys

def test_backend():
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_backend():
        sys.exit(0)
    else:
        sys.exit(1)

# Made with Bob
