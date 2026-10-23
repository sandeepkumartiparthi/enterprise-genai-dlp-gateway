import os

file_path = 'E:/enterprise-genai-dlp-gateway/frontend/src/components/ThreeDimensionalSecurityVault.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Make station 3 dynamic in canvas render
old_station_3 = """        {
          id: 'station-3',
          step: 3,
          x: width * 0.63,
          y: cy,
          name: 'Cryptographic Vault',
          sub: privacyMode === 'synthetic' ? '✨ Synthetic Shadows' : '🔒 Token Chamber',
          tag: 'SURROGATES',
          color: '#7c3aed',
          glow: 'rgba(124, 58, 237, 0.25)',
          details: 'Zero-Trust Storage: Deterministic Ephemeral TTL Vault & Surrogates',
        },"""

new_station_3 = """        {
          id: 'station-3',
          step: 3,
          x: width * 0.63,
          y: cy,
          name: privacyMode === 'synthetic' ? 'Indian Synthetic Shadows Pod' : 'Cryptographic Token Chamber',
          sub: privacyMode === 'synthetic' ? '✨ Indian Personas (Natural Grammar)' : '🔒 Ephemeral UUID Vault',
          tag: privacyMode === 'synthetic' ? 'SYNTHETIC SHADOWS' : 'TOKEN VAULT',
          color: privacyMode === 'synthetic' ? '#9333ea' : '#2563eb',
          glow: privacyMode === 'synthetic' ? 'rgba(147, 51, 234, 0.35)' : 'rgba(37, 99, 235, 0.35)',
          details: privacyMode === 'synthetic'
            ? 'AI-Native Indian Synthetic Personas (natural grammar without bracketed placeholders)'
            : 'Deterministic Ephemeral Token Chamber ([ENTITY_UUID] format-preserving tokens)',
        },"""

if old_station_3 in text:
    text = text.replace(old_station_3, new_station_3)
    print("Updated station 3 in canvas render (LF)")
else:
    old_station_3_crlf = old_station_3.replace('\n', '\r\n')
    if old_station_3_crlf in text:
        text = text.replace(old_station_3_crlf, new_station_3.replace('\n', '\r\n'))
        print("Updated station 3 in canvas render (CRLF)")

# Update STATION_PODS_INFO hover details for station 3
old_hover_3 = """  {
    step: 3,
    pct: 0.63,
    name: 'Cryptographic Vault Pod',
    role: 'Surrogate Generation & Token Chamber',
    badge: 'ZERO-TRUST ISOLATION',
    color: '#7c3aed',
    desc: 'Encapsulates true identifiers in an ephemeral in-memory vault with cryptographic hash receipts.',
  },"""

new_hover_3 = """  {
    step: 3,
    pct: 0.63,
    name: 'Surrogate Isolation Pod',
    role: 'Dynamic Privacy Engine (Synthetic / Token Chamber)',
    badge: 'ZERO-TRUST ISOLATION',
    color: '#9333ea',
    desc: 'Switches dynamically between Indian Synthetic Personas (natural grammar) and Ephemeral Token Chamber ([ENTITY_UUID]).',
  },"""

if old_hover_3 in text:
    text = text.replace(old_hover_3, new_hover_3)
    print("Updated STATION_PODS_INFO hover details (LF)")
else:
    old_hover_3_crlf = old_hover_3.replace('\n', '\r\n')
    if old_hover_3_crlf in text:
        text = text.replace(old_hover_3_crlf, new_hover_3.replace('\n', '\r\n'))
        print("Updated STATION_PODS_INFO hover details (CRLF)")

# Update bottom status ticker to Indian cluster
text = text.replace(
    'Comet-Tail Particle Bus',
    'ap-south-1 (Mumbai Core) • Comet-Tail Bus'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated ThreeDimensionalSecurityVault.tsx successfully!")
