import urllib.request
import json

req_data = json.dumps({
    'promptText': 'Customer Rajesh Sharma with Aadhaar 7704 2210 8821 transferred money.',
    'privacyMode': 'synthetic'
}).encode('utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:5180/api/sandbox/analyze',
    data=req_data,
    headers={'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode('utf-8'))
    print(f"Entities count: {len(data.get('entities', []))}")
    for e in data.get('entities', []):
        print("Entity:", e)
    print(f"Sanitized: {data.get('sanitizedText')}")
