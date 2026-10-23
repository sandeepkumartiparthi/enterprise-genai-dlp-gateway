import re

file_path = r"E:\enterprise-genai-dlp-gateway\frontend\src\App.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update <header> to have overflow-x-hidden
old_header = '<header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">'
new_header = '<header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs overflow-x-hidden">'

assert old_header in content, "old_header not found"
content = content.replace(old_header, new_header, 1)

# 2. Update Tier 1 container to overflow-hidden
old_tier1 = '<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-15 flex items-center justify-between gap-4">'
new_tier1 = '<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-15 flex items-center justify-between gap-4 overflow-hidden">'

assert old_tier1 in content, "old_tier1 not found"
content = content.replace(old_tier1, new_tier1, 1)

# 3. Update Tier 2 container and nav (remove overflow-x-auto, add overflow-hidden & shrink-0)
old_tier2 = """        {/* TIER 2: 5 PRIMARY NAVIGATION TABS & ACTIVE HORIZON TELEMETRY */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-12 flex items-center justify-between gap-4">
          {/* Left: Perfectly aligned segmented Navigation Tabs */}
          <nav className="flex items-center gap-1.5 overflow-x-auto py-1">"""

new_tier2 = """        {/* TIER 2: 5 PRIMARY NAVIGATION TABS & ACTIVE HORIZON TELEMETRY */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-12 flex items-center justify-between gap-4 overflow-hidden">
          {/* Left: Perfectly aligned segmented Navigation Tabs (No sideways scroll) */}
          <nav className="flex items-center gap-1.5 py-1 shrink-0 overflow-visible">"""

assert old_tier2 in content, "old_tier2 not found"
content = content.replace(old_tier2, new_tier2, 1)

# 4. Make sure the right side telemetry chip hides on medium screens to avoid any crowding
old_chips = '<div className="hidden md:flex items-center gap-2 text-xs">'
new_chips = '<div className="hidden lg:flex items-center gap-2 text-xs shrink-0">'
assert old_chips in content, "old_chips not found"
content = content.replace(old_chips, new_chips, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated App.tsx: removed sideway scroll and added overflow protections!")
