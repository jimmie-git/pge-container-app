# Bulk Email Sender

This repository includes a Tkinter-based application for sending personalized emails in bulk. Contacts can be imported from CSV or Excel files and each message is generated from a template.

## Running Locally

Install the requirements and run the script:

```bash
pip install -r requirements.txt
python email_sender.py
```

## Creating a Gmail App Password

The app uses Gmail's SMTP service, which requires an App Password if you have
2-Step Verification enabled. Follow these steps:

1. Enable 2-Step Verification on your Google Account.
2. Go to your account's [App passwords](https://myaccount.google.com/apppasswords) page.
3. Generate a new password for "Mail" and copy the value.

See Google's [official guide](https://support.google.com/accounts/answer/185833)
for more details.

## Packaging

A PyInstaller spec file (`email_sender.spec`) and a GitHub Actions workflow have been added so the repository automatically builds a Windows executable on pushes to `main`. If you wish to build locally, run:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole email_sender.spec
```

The resulting executable will appear in the `dist` directory.

---

## PG&E Green Button Integration

The repository also contains sample modules for integrating with PG&E's
Share My Data API using OAuth2 and mutual TLS. Key files include:

- `OAuth2.py` – exchanges authorization codes for access tokens and refreshes
  tokens.
- `ClientCredentials.py` – obtains a client access token for connectivity tests.
- `Api.py` – makes authenticated data requests.
- `pge_example.py` – minimal Flask app demonstrating the OAuth callback flow.

These modules require the `requests` and `Flask` packages in addition to the
original requirements. Update `requirements.txt` accordingly and replace the
placeholders in `pge_example.py` with the credentials and certificate paths
provided by PG&E.

### Running the example

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set your PG&E credentials and certificate paths as environment variables**

   ```bash
   export PGE_CLIENT_ID="<your_client_id>"
   export PGE_CLIENT_SECRET="<your_client_secret>"
   export PGE_REDIRECT_URI="http://localhost:5000/oauth/callback"
   export PGE_AUTH_URL="https://api.pge.com/datacustodian/oauth/v2/authorize"
   export PGE_TOKEN_URL="https://api.pge.com/datacustodian/oauth/v2/token"
   export PGE_CERT_CRT="/path/to/client.crt"
   export PGE_CERT_KEY="/path/to/client.key"
   ```

3. **Start the Flask app**

   ```bash
   python pge_example.py
   ```

   Visit `http://localhost:5000` in your browser and click **Connect to PG&E**.
   After logging in and authorizing access, the callback route will display the
   token response from PG&E.
