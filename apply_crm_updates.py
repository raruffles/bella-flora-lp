import urllib.request, json

with open(r'c:\portfólio\Portfólio-site\bella-flora-lp\.opus_token.json', 'r') as f:
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

print("--- 1. ADICIONANDO 8 PALAVRAS-CHAVE PARA TAUBATÉ (CONCORDÂNCIA DE FRASE) ---")
taubate_keywords = [
    "laboratório de manipulação taubaté",
    "fórmulas personalizadas taubaté",
    "manipulados taubaté",
    "orçamento de manipulação taubaté",
    "suplementos manipulados taubaté",
    "dermocosméticos manipulados taubaté",
    "manipulação em taubaté",
    "manipulação vale do paraíba"
]
kw_res = call_write_tool('add_keywords', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'keywords': taubate_keywords,
    'match_type': 'PHRASE',
    'confirm': True
})
print("Resultado Keywords:", json.dumps(kw_res, indent=2))

print("\n--- 2. CRIANDO ANÚNCIO CORRIGIDO COM COBERTURA SJC E TAUBATÉ ---")
rsa_res = call_write_tool('create_responsive_search_ad', {
    'customer_id': CUSTOMER_ID,
    'ad_group_id': AD_GROUP_ID,
    'final_url': 'https://www.farmaciabellaflora.com.br',
    'path1': 'laboratorio',
    'path2': 'formulas',
    'headlines': [
        "Bella Flora Manipulação",
        "Atendimento em SJC e Taubaté",
        "Entrega em SJC e Taubaté",
        "Laboratório de Manipulação",
        "Fórmulas Personalizadas",
        "Orçamento Rápido no WhatsApp",
        "Manipulação Vale do Paraíba",
        "Receba Seu Pedido em Casa",
        "Qualidade e Preço Justo",
        "Suplementos e Bem-Estar"
    ],
    'descriptions': [
        "Faça um único pedido de orçamento pelo WhatsApp com atendimento rápido e personalizado.",
        "Fórmulas manipuladas sob medida com os melhores preços e entrega em SJC e Taubaté.",
        "Envie seu pedido online com praticidade. Atendimento ágil para SJC, Taubaté e todo o Vale."
    ],
    'status': 'PAUSED',
    'confirm': True
})
print("Resultado RSA:", json.dumps(rsa_res, indent=2))

with open(r'c:\portfólio\Portfólio-site\bella-flora-lp\crm_execution_log.json', 'w', encoding='utf-8') as f:
    json.dump({'keywords': kw_res, 'rsa': rsa_res}, f, indent=2)

print("\nEXECUÇÃO FINALIZADA COM SUCESSO!")
