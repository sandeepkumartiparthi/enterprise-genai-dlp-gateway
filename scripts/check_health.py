import urllib.request

try:
    with urllib.request.urlopen('http://127.0.0.1:5180/api/audit/stats', timeout=5) as res:
        print(f"Backend Status: {res.status} OK (HTTP 200)")
except Exception as e:
    print(f"Backend Status: {e}")

try:
    with urllib.request.urlopen('http://127.0.0.1:5173/', timeout=5) as res:
        print(f"Frontend Status: {res.status} OK (HTTP 200)")
except Exception as e:
    print(f"Frontend Status: {e}")
