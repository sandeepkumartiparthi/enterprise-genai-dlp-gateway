import os
import shutil

src_brain = r"C:\Users\sande\.gemini\antigravity\brain\a0423d85-671a-488c-8dc4-4980df1c191c"
e_root = r"E:\enterprise-genai-dlp-gateway"

# 1. Copy documentation report
doc_src = os.path.join(src_brain, "documentation_and_test_report.md")
doc_dst = os.path.join(e_root, "docs", "TESTING_AND_VERIFICATION_REPORT.md")
if os.path.exists(doc_src):
    shutil.copy2(doc_src, doc_dst)
    print(f"Copied {doc_src} -> {doc_dst}")

# 2. Copy test and verification scripts from scratch
scratch_src = os.path.join(src_brain, "scratch")
scripts_dst = os.path.join(e_root, "scripts")
os.makedirs(scripts_dst, exist_ok=True)

for fname in os.listdir(scratch_src):
    s_file = os.path.join(scratch_src, fname)
    if os.path.isfile(s_file):
        d_file = os.path.join(scripts_dst, fname)
        shutil.copy2(s_file, d_file)

print(f"Copied all scripts from {scratch_src} -> {scripts_dst}")

# 3. Synchronize scratch workspace to E: just in case
scratch_workspace = r"C:\Users\sande\.gemini\antigravity\scratch\enterprise-genai-dlp-gateway"
for root, dirs, files in os.walk(scratch_workspace):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'bin', 'obj', 'dist', '.vs']]
    rel = os.path.relpath(root, scratch_workspace)
    target_dir = os.path.join(e_root, rel)
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        s_path = os.path.join(root, f)
        t_path = os.path.join(target_dir, f)
        if not os.path.exists(t_path) or os.path.getmtime(s_path) > os.path.getmtime(t_path):
            shutil.copy2(s_path, t_path)
            print(f"Synced: {rel}/{f}")

print("Sync completed successfully!")
