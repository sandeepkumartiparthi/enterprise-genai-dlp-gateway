app_path = r'E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for the lines around 1620
for idx, line in enumerate(lines):
    if '<span>Redact</span>' in line:
        print(f"Found Redact at line {idx+1}")
        # Print subsequent lines
        for j in range(idx, idx + 10):
            print(f"{j+1}: {repr(lines[j])}")
        break
