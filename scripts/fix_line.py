with open('E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines[783] = '          title: `Quota Updated: ${editingQuotaDept}`,\n'

with open('E:/enterprise-genai-dlp-gateway/frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Line 784 set with backticks!')
