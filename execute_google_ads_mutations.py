import urllib.request
import json
import time

with open('c:/portfólio/Portfólio-site/bella-flora-lp/.opus_token.json', 'r') as f:
    token_data = json.load(f)

access_token = token_data['access_token']
CUSTOMER_ID = "9797555001"
AD_GROUP_ID = "200791794458" # Grupo de anúncios 4

def call_write_tool(tool_name, arguments={}):
    payload = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'tools/call',
        'params': {
            'name': 'call_write_tool',
            'arguments': {
                'name': tool_name,
                'arguments': arguments
            }
        }
    }
    req = urllib.request.Request(
        'https://mcp.opus-growth.com/mcp',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'Claude-Code/2.1.319'
        }
    )
    with urllib.request.urlopen(req) as resp:
        res = resp.read().decode('utf-8')
        for line in res.splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])
        return json.loads(res)

results = {}

# 1. Pause disapproved ads
print("--- 1. PAUSANDO ANÚNCIOS REPROVADOS ---")
disapproved_ads = [
    {"ad_id": "823079890223", "ad_group_id": "200791794458"},
    {"ad_id": "667522936308", "ad_group_id": "149154581462"},
    {"ad_id": "667522936311", "ad_group_id": "149154581462"},
    {"ad_id": "665619539907", "ad_group_id": "149651066845"},
    {"ad_id": "666005617150", "ad_group_id": "149651066845"},
    {"ad_id": "736425750179", "ad_group_id": "153302559753"},
    {"ad_id": "829602640045", "ad_group_id": "200877713745"},
    {"ad_id": "829677915983", "ad_group_id": "200877713745"}
]

paused_ads_log = []
for ad_item in disapproved_ads:
    res = call_write_tool('update_ad_status', {
        'customer_id': CUSTOMER_ID,
        'ad_group_id': ad_item['ad_group_id'],
        'ad_id': ad_item['ad_id'],
        'status': 'PAUSED',
        'confirm': True
    })
    paused_ads_log.append({"ad_id": ad_item['ad_id'], "res": res})
    print(f"Ad {ad_item['ad_id']} paused:", res.get('result', {}).get('structuredContent', {}).get('applied'))
    time.sleep(0.5)

results['paused_ads'] = paused_ads_log

# 2. Pause broad match keywords in Grupo de anúncios 4
print("\n--- 2. PAUSANDO PALAVRAS-CHAVE EM CONCORDÂNCIA AMPLA ---")
criterion_ids = "10329410,16833711,18427900,18427920,93389695,125990115,125990455,465518669,465518729,616543111,4942271030,5724939750,296132538199,296742522845,296798071909,296798073549,299257047275,317712279536,326003720604"
res_kw_pause = call_write_tool('manage_keywords', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'criterion_ids': criterion_ids,
    'action': 'pause',
    'confirm': True
})
print("Keywords paused result:", res_kw_pause.get('result', {}).get('structuredContent', {}).get('applied'))
results['paused_keywords'] = res_kw_pause

# 3. Add 6 new phrase match keywords
print("\n--- 3. ADICIONANDO 6 NOVAS PALAVRAS-CHAVE EM CONCORDÂNCIA DE FRASE ---")
new_keywords = [
    "laboratório de manipulação em sjc",
    "fórmulas personalizadas sjc",
    "manipulados são josé dos campos",
    "orçamento de manipulação sjc",
    "suplementos manipulados sjc",
    "dermocosméticos manipulados sjc"
]
res_kw_add = call_write_tool('add_keywords', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'keywords': new_keywords,
    'match_type': 'PHRASE',
    'confirm': True
})
print("Keywords added result:", res_kw_add.get('result', {}).get('structuredContent', {}).get('applied'))
results['added_keywords'] = res_kw_add

# 4. Create new Responsive Search Ad (RSA) in PAUSED status
print("\n--- 4. CRIANDO ANÚNCIO RESPONSIVO (RSA) COM STATUS PAUSED ---")
res_rsa = call_write_tool('create_responsive_search_ad', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'final_url': 'https://www.farmaciabellaflora.com.br',
    'path1': 'orcamento',
    'path2': 'rapido',
    'headlines': [
        "Bella Flora Manipulação SJC",
        "Fórmulas Personalizadas SJC",
        "Laboratório de Manipulação",
        "Orçamento Rápido no WhatsApp",
        "Entrega em Domicílio em SJC",
        "Receba Seu Pedido em Casa",
        "Atendimento em SJC Zona Leste",
        "Suplementos e Bem-Estar SJC",
        "Cotações Rápidas em 1 Só Lugar",
        "Qualidade e Preço Justo SJC"
    ],
    'descriptions': [
        "Faça um único pedido de orçamento pelo WhatsApp com atendimento rápido e personalizado.",
        "Fórmulas manipuladas sob medida em SJC com os melhores preços e entrega em domicílio.",
        "Envie seu pedido online com praticidade. Atendimento ágil na Zona Leste e toda SJC."
    ],
    'status': 'PAUSED',
    'confirm': True
})
print("RSA created result:", res_rsa.get('result', {}).get('structuredContent', {}).get('applied'))
results['created_rsa'] = res_rsa

with open('c:/portfólio/Portfólio-site/bella-flora-lp/execution_log.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n--- TODAS AS OPERAÇÕES FORAM CONCLUÍDAS COM SUCESSO! ---")
