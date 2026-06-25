import sys, os
os.chdir('backend')          # ensure .env is found
sys.path.insert(0, '.')
from config import settings

key = settings.OPENAI_API_KEY
print("Key prefix :", key[:16] + "...")
print("Key length :", len(key))
print("Starts sk- :", key.startswith("sk-"))
print("Has spaces :", key != key.strip())
print("Has newline :", "\n" in key or "\r" in key)
print("Repr head  :", repr(key[:20]))
