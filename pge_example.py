"""Simple Flask example demonstrating PG&E OAuth flow."""

from flask import Flask, redirect, request
from OAuth2 import OAuth2

app = Flask(__name__)

# Configuration placeholders - replace with real values
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "https://yourapp.com/oauth/callback"
AUTH_URL = "https://api.pge.com/datacustodian/oauth/v2/authorize"
TOKEN_URL = "https://api.pge.com/datacustodian/oauth/v2/token"
CERT_CRT = "path/to/client.crt"
CERT_KEY = "path/to/client.key"

oauth_client = OAuth2(CLIENT_ID, CLIENT_SECRET, CERT_CRT, CERT_KEY)

@app.route("/")
def index():
    return '<a href="/login">Connect to PG&E</a>'

@app.route("/login")
def login():
    from urllib.parse import urlencode
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "DEFAULT",
    }
    return redirect(AUTH_URL + "?" + urlencode(params))

@app.route("/oauth/callback")
def callback():
    code = request.args.get("code") or request.args.get("authorization_code")
    if not code:
        return "Missing authorization code", 400
    result = oauth_client.get_access_token(TOKEN_URL, code, REDIRECT_URI)
    if result.get("status") != 200:
        return "Token exchange failed: " + result.get("error", ""), 500
    return result

if __name__ == "__main__":
    app.run(debug=True)
