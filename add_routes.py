import os, shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(base_dir, 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add <base href="/" /> if not present
if '<base href="/" />' not in html:
    pos = html.find('<meta name="viewport"')
    if pos != -1:
        end_pos = html.find('>', pos) + 1
        html = html[:end_pos] + '\n  <base href="/" />' + html[end_pos:]
        print('Added <base href="/" />')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

# Create physical directories:
# 1. /laboratorio
# 2. /laboratorio/formulas
# 3. /formulas
# 4. /orcamento/rapido
routes = [
    os.path.join(base_dir, 'laboratorio'),
    os.path.join(base_dir, 'laboratorio', 'formulas'),
    os.path.join(base_dir, 'formulas'),
    os.path.join(base_dir, 'orcamento'),
    os.path.join(base_dir, 'orcamento', 'rapido')
]

for r in routes:
    os.makedirs(r, exist_ok=True)
    target_file = os.path.join(r, 'index.html')
    shutil.copy2(html_path, target_file)
    print(f'Created route: {target_file}')

vitrine_path = os.path.join(base_dir, 'vitrine', 'index.html')
produtos_dir = os.path.join(base_dir, 'produtos')
os.makedirs(produtos_dir, exist_ok=True)
shutil.copy2(vitrine_path, os.path.join(produtos_dir, 'index.html'))
print('Synced /produtos/index.html from dedicated /vitrine/index.html')

print('All routes created successfully!')
