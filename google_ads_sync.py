import http.server
import socketserver
import urllib.parse
import urllib.request
import json
import hashlib
import base64
import secrets
import webbrowser
import os
import sys

PORT = 8085
REDIRECT_URI = f"http://localhost:{PORT}/callback"

# Register dynamic client if not cached
CLIENT_CACHE_FILE = os.path.join(os.path.dirname(__file__), ".opus_client.json")

def get_or_create_client():
    if os.path.exists(CLIENT_CACHE_FILE):
        try:
            with open(CLIENT_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    req = urllib.request.Request(
        "https://googleads.opus-growth.com/register",
        data=json.dumps({
            "client_name": "Antigravity Google Ads Client",
            "redirect_uris": [REDIRECT_URI],
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"]
        }).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Claude-Code/2.1.319"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
        with open(CLIENT_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return data

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    code = None
    error = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/callback":
            qs = urllib.parse.parse_qs(parsed.query)
            if "code" in qs:
                OAuthCallbackHandler.code = qs["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"""
                <html>
                <body style="font-family:sans-serif;text-align:center;padding:50px;background:#f0fdf4;">
                    <h1 style="color:#166534;">&#10004; Autentica&ccedil;&atilde;o Conclu&iacute;da com Sucesso!</h1>
                    <p style="color:#15803d;font-size:18px;">A conex&atilde;o com a conta Google Ads foi autorizada. Voc&ecirc; pode fechar esta aba e voltar para o chat do Antigravity.</p>
                </body>
                </html>
                """)
            else:
                OAuthCallbackHandler.error = qs.get("error_description", ["Erro desconhecido"])[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<html><body><h1>Erro: {OAuthCallbackHandler.error}</h1></body></html>".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence standard HTTP request logs
        return

def exchange_code_for_token(client, code, verifier):
    token_url = "https://googleads.opus-growth.com/token"
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": verifier
    }).encode("utf-8")

    req = urllib.request.Request(
        token_url,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Claude-Code/2.1.319"
        }
    )

    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

def call_mcp(access_token, method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": secrets.randbelow(100000),
        "method": method
    }
    if params is not None:
        payload["params"] = params

    req = urllib.request.Request(
        "https://mcp.opus-growth.com/mcp",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Claude-Code/2.1.319"
        }
    )

    with urllib.request.urlopen(req) as resp:
        res = resp.read().decode("utf-8")
        # May be SSE or JSON
        if res.startswith("data: "):
            res = res[6:].strip()
        try:
            return json.loads(res)
        except Exception:
            return res

def main():
    client = get_or_create_client()
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

    auth_params = {
        "response_type": "code",
        "client_id": client["client_id"],
        "redirect_uri": REDIRECT_URI,
        "scope": "openid https://www.googleapis.com/auth/userinfo.email",
        "state": "bellaflora_auth",
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }

    auth_url = "https://googleads.opus-growth.com/authorize?" + urllib.parse.urlencode(auth_params)

    print("AUTH_URL:" + auth_url)
    sys.stdout.flush()

    # Start local server to wait for code
    server = socketserver.TCPServer(("localhost", PORT), OAuthCallbackHandler)
    server.timeout = 180 # 3 minutes timeout

    # Open user browser
    webbrowser.open(auth_url)

    while OAuthCallbackHandler.code is None and OAuthCallbackHandler.error is None:
        server.handle_request()

    server.server_close()

    if OAuthCallbackHandler.error:
        print(f"ERROR: {OAuthCallbackHandler.error}")
        return

    code = OAuthCallbackHandler.code
    print("CODE_RECEIVED")
    sys.stdout.flush()

    token_data = exchange_code_for_token(client, code, verifier)
    access_token = token_data.get("access_token")
    if not access_token:
        print("ERROR: Could not get access token:", token_data)
        return

    print("TOKEN_ACQUIRED")
    sys.stdout.flush()

    # Save token for future calls
    with open(os.path.join(os.path.dirname(__file__), ".opus_token.json"), "w", encoding="utf-8") as f:
        json.dump(token_data, f)

    # 1. Initialize MCP
    init_res = call_mcp(access_token, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "Antigravity Google Ads Client", "version": "1.0"}
    })
    print("INIT_RES:", json.dumps(init_res, indent=2))

    # 2. List tools
    tools_res = call_mcp(access_token, "tools/list")
    print("TOOLS_LIST:", json.dumps(tools_res, indent=2))

if __name__ == "__main__":
    main()
