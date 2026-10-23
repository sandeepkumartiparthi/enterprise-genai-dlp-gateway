import urllib.request
import time

time.sleep(2)

print("Checking Backend...")
try:
    with urllib.request.urlopen('http://127.0.0.1:5180/api/dlp/health', timeout=5) as res:
        print(f"Backend Status: {res.status} OK")
except Exception as e:
    print(f"Backend Status: {e}")

print("Checking Frontend...")
try:
    with urllib.request.urlopen('http://127.0.0.1:5173/', timeout=5) as res:
        print(f"Frontend Status: {res.status} OK")
except Exception as e:
    print(f"Frontend Status: {e}")
