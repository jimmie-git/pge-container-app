import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_contacts(path: str):
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    return df


def fill_template(template: str, data: dict) -> str:
    result = template
    for key, value in data.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


class EmailSenderApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Bulk Email Sender')

        self.file_path = None
        self.contacts = None

        # File selection
        self.file_frame = tk.Frame(master)
        self.file_frame.pack(padx=10, pady=5)
        tk.Button(self.file_frame, text='Select Contact File', command=self.select_file).pack(side=tk.LEFT)
        self.file_label = tk.Label(self.file_frame, text='No file selected')
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Subject
        tk.Label(master, text='Email Subject:').pack(anchor='w', padx=10)
        self.subject_entry = tk.Entry(master, width=80)
        self.subject_entry.pack(fill='x', padx=10, pady=5)

        # Body
        tk.Label(master, text='Email Body (use {{ColumnName}} placeholders):').pack(anchor='w', padx=10)
        self.body_text = tk.Text(master, height=15, width=80)
        self.body_text.pack(padx=10, pady=5)

        # Gmail credentials
        cred_frame = tk.Frame(master)
        cred_frame.pack(padx=10, pady=5, fill='x')
        tk.Label(cred_frame, text='Gmail Address:').grid(row=0, column=0, sticky='e')
        self.email_entry = tk.Entry(cred_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5)
        tk.Label(cred_frame, text='App Password:').grid(row=1, column=0, sticky='e')
        self.password_entry = tk.Entry(cred_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1, padx=5)

        # Buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text='Preview First Email', command=self.preview_email).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Send Emails', command=self.send_emails).pack(side=tk.LEFT, padx=5)

        # Log
        tk.Label(master, text='Log:').pack(anchor='w', padx=10)
        self.log_text = tk.Text(master, height=10, width=80, state='disabled')
        self.log_text.pack(padx=10, pady=5)

    def log(self, message: str):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV/Excel', '*.csv *.xlsx *.xls')])
        if path:
            try:
                self.contacts = load_contacts(path)
                self.file_path = path
                self.file_label.config(text=path)
                self.log(f'Loaded {len(self.contacts)} contacts.')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to load file: {e}')

    def preview_email(self):
        if self.contacts is None or self.contacts.empty:
            messagebox.showwarning('No Contacts', 'Please load a contact file first.')
            return
        data = self.contacts.iloc[0].to_dict()
        subject = fill_template(self.subject_entry.get(), data)
        body = fill_template(self.body_text.get('1.0', 'end').strip(), data)
        messagebox.showinfo('Preview', f'Subject: {subject}\n\n{body}')

    def send_emails(self):
        if self.contacts is None or self.contacts.empty:
            messagebox.showwarning('No Contacts', 'Please load a contact file first.')
            return
        sender = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not sender or not password:
            messagebox.showwarning('Credentials Missing', 'Enter Gmail address and app password.')
            return

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, password)
        except Exception as e:
            messagebox.showerror('Login Failed', f'Could not log in: {e}')
            return

        for idx, row in self.contacts.iterrows():
            data = row.to_dict()
            recipient = str(data.get('Email', ''))
            if not recipient:
                self.log(f'Skipping row {idx+1}: no Email field')
                continue
            subject = fill_template(self.subject_entry.get(), data)
            body = fill_template(self.body_text.get('1.0', 'end').strip(), data)

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server.sendmail(sender, recipient, msg.as_string())
                self.log(f'Sent to {recipient}')
            except Exception as e:
                self.log(f'Failed to send to {recipient}: {e}')
        server.quit()
        messagebox.showinfo('Done', 'Email sending completed.')


def main():
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
