import urllib.request
import json

url = 'http://localhost:5180/api/sandbox/analyze'
payload_prompt = "Customer Rajesh Sharma (email: rajesh.sharma@finserve.in, phone +91 98201 44829) Aadhaar 4829 6103 9482 verified."

# 1. Test Synthetic mode
req_synth = urllib.request.Request(
    url,
    data=json.dumps({"promptText": payload_prompt, "privacyMode": "synthetic"}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req_synth) as res:
    data_synth = json.loads(res.read().decode('utf-8'))
    print("=== SYNTHETIC MODE ===")
    print("Sanitized text:", data_synth.get("sanitizedText") or data_synth.get("sanitizedPrompt"))
    print("Tokens/Entities:", [e.get("replacementToken") for e in data_synth.get("entities", [])])

# 2. Test Token Vault mode
req_token = urllib.request.Request(
    url,
    data=json.dumps({"promptText": payload_prompt, "privacyMode": "token"}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req_token) as res:
    data_token = json.loads(res.read().decode('utf-8'))
    print("\n=== TOKEN VAULT MODE ===")
    print("Sanitized text:", data_token.get("sanitizedText") or data_token.get("sanitizedPrompt"))
    print("Tokens/Entities:", [e.get("replacementToken") for e in data_token.get("entities", [])])
