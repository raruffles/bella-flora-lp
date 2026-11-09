path = r'c:\portfólio\Portfólio-site\bella-flora-lp\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Medicamentos magistrais, suplementa' in line:
        lines[i] = '  <meta name="twitter:description" content="Fórmulas magistrais, suplementação e dermocosméticos manipulados sob medida. Orçamento rápido pelo WhatsApp." />\n'
    if 'prescri' in line and 'ICP-Brasil' in line:
        lines[i] = line.replace('prescrições com certificado', 'documentos com certificado')
    if 'isentos de prescri' in line:
        lines[i] = line.replace('isentos de prescrição médica conforme lista oficial da Anvisa', 'de venda livre conforme normas da Anvisa')
    if 'Sob Prescri' in line:
        lines[i] = '              Sob Medida\n'
    if 'conforme a prescri' in line:
        lines[i] = '                Cápsulas gastrorresistentes, sachês solúveis, gotas orais e filmes sublinguais dosados rigorosamente sob medida para você.\n'
    if 'endocrinologistas' in line and 'prescritas' in line:
        lines[i] = '                <li class="flex items-center gap-1.5"><i class="bi bi-check2 text-emerald-700 font-bold"></i> Fórmulas indicadas por endocrinologistas</li>\n'
    if 'drogarias convencionais' in line or 'drogarias' in line:
        lines[i] = line.replace('drogarias convencionais', 'opções industriais').replace('drogarias', 'opções industriais')
    if 'Prescritora Parceira' in line:
        lines[i] = '              <i class="bi bi-patch-check-fill text-emerald-700"></i> Médica Parceira\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Updated successfully!')
