import urllib.request, json

with open('c:/portfólio/Portfólio-site/bella-flora-lp/.opus_token.json', 'r') as f:
    token_data = json.load(f)

access_token = token_data['access_token']

def call_tool(tool_name, arguments={}):
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': tool_name, 'arguments': arguments}}
    req = urllib.request.Request(
        'https://mcp.opus-growth.com/mcp',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Authorization': f'Bearer {access_token}', 'User-Agent': 'Claude-Code/2.1.319'}
    )
    with urllib.request.urlopen(req) as resp:
        res = resp.read().decode('utf-8')
        for line in res.splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])
        return json.loads(res)

query = "SELECT ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.id = 200791794458 AND ad_group_criterion.type = 'KEYWORD'"
res = call_tool('google_ads_query', {'account_id': '9797555001', 'query': query})
data = res.get('result', {}).get('structuredContent', {})
rows = data.get('rows', [])
print(f'Total Keywords in Grupo de anúncios 4: {len(rows)}')
for r in rows:
    agc = r.get('adGroupCriterion', {})
    cid = agc.get('criterionId')
    kw = agc.get('keyword', {})
    text = kw.get('text')
    match = kw.get('matchType')
    status = agc.get('status')
    print(f'ID: {cid} | Text: "{text}" | Match: {match} | Status: {status}')
