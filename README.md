# Bulk Email Sender

This repository includes a Tkinter-based application for sending personalized emails in bulk. Contacts can be imported from CSV or Excel files and each message is generated from a template.

## Running Locally

Install the requirements and run the script:

```bash
pip install -r requirements.txt
python email_sender.py
```

## Packaging

A GitHub Actions workflow automatically builds a Windows executable on pushes to `main`. To build locally use:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole email_sender.py
```

The resulting executable will appear in the `dist` directory.

## Gmail App Password

The application sends email through Gmail. If you use two-step verification you must create an App Password:

1. Visit <https://myaccount.google.com/apppasswords> while logged into your Gmail account.
2. Generate a new password for "Mail" and copy the 16-character value.
3. Enter this password in the app when prompted.

This avoids storing your main account password and is required for SMTP access.

