app_path = r'E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx'

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '<span>Redact</span>' in line:
        # Check lines idx+1 to idx+5
        if '</div>\n' in lines[idx+4] and ');\n' in lines[idx+5]:
            # Insert the 4th </div>
            lines.insert(idx+5, '                      </div>\n')
            print(f"Inserted missing </div> at line {idx+6}")
            break

with open(app_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Saved successfully!")
