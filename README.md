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
original requirements. Before running `pge_example.py`, set the following
environment variables with the credentials and certificate paths provided by PG&E:

- `PGE_CLIENT_ID` – your client ID
- `PGE_CLIENT_SECRET` – your client secret
- `PGE_CERT_CRT` – path to the `.crt` certificate file
- `PGE_CERT_KEY` – path to the corresponding private key
