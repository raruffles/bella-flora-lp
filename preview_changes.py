import urllib.request, json

with open('c:/portfólio/Portfólio-site/bella-flora-lp/.opus_token.json', 'r') as f:
    token_data = json.load(f)

access_token = token_data['access_token']
CUSTOMER_ID = "9797555001"
AD_GROUP_ID = "200791794458" # Grupo de anúncios 4
CAMPAIGN_ID = "20372072830"  # [WL][TRAF] Manipulado

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

print("=== 1. PREVIEW: PAUSE KEYWORDS IN GRUPO DE ANÚNCIOS 4 ===")
criterion_ids = "10329410,16833711,18427900,18427920,93389695,125990115,125990455,465518669,465518729,616543111,4942271030,5724939750,296132538199,296742522845,296798071909,296798073549,299257047275,317712279536,326003720604"
kw_pause_preview = call_write_tool('manage_keywords', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'criterion_ids': criterion_ids,
    'action': 'pause',
    'confirm': False
})
print(json.dumps(kw_pause_preview, indent=2))

print("\n=== 2. PREVIEW: ADD 6 PHRASE MATCH KEYWORDS ===")
new_keywords = [
    "laboratório de manipulação em sjc",
    "fórmulas personalizadas sjc",
    "manipulados são josé dos campos",
    "orçamento de manipulação sjc",
    "suplementos manipulados sjc",
    "dermocosméticos manipulados sjc"
]
kw_add_preview = call_write_tool('add_keywords', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'keywords': new_keywords,
    'match_type': 'PHRASE',
    'confirm': False
})
print(json.dumps(kw_add_preview, indent=2))

print("\n=== 3. PREVIEW: CREATE RSA AD IN PAUSED STATUS ===")
rsa_preview = call_write_tool('create_responsive_search_ad', {
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
    'confirm': False
})
print(json.dumps(rsa_preview, indent=2))
