# Bulk Email Sender

This repository includes a Tkinter-based application for sending personalized emails in bulk. Contacts can be imported from CSV or Excel files and each message is generated from a template.

## Running Locally

Install the requirements and run the script:

```bash
pip install -r requirements.txt
python email_sender.py
```

## Packaging

A PyInstaller spec file (`email_sender.spec`) and a GitHub Actions workflow have been added so the repository automatically builds a Windows executable on pushes to `main`. If you wish to build locally, run:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole email_sender.spec
```

The resulting executable will appear in the `dist` directory.
