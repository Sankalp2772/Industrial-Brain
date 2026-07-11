import os

frontend_src = r"d:\Industrial Brain\frontend\src"

for root, _, files in os.walk(frontend_src):
    for f in files:
        if f.endswith('.tsx') or f.endswith('.ts'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'mock' in content.lower() or 'fetch' in content.lower() or 'axios' in content.lower():
                    print(f"--- {f} ---")
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'mock' in line.lower() or 'fetch' in line.lower() or 'axios' in line.lower():
                            print(f"{i+1}: {line.strip()}")
