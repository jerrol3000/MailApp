import tkinter as tk
from tkinter import messagebox
import imaplib
import email

print("running")

class EmailDeleterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Deleter")
        self.geometry("800x600")

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()

        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.delete_from_label = tk.Label(self, text="Delete email from:")
        self.delete_from_label.pack()

        self.delete_from_entry = tk.Entry(self)
        self.delete_from_entry.pack()

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_emails)
        self.delete_button.pack()

        self.remaining_emails_label = tk.Label(self, text="Remaining Emails:")
        self.remaining_emails_label.pack()

        self.remaining_emails_listbox = tk.Listbox(self)
        self.remaining_emails_listbox.pack()

        self.deleted_emails_label = tk.Label(self, text="Deleted Emails:")
        self.deleted_emails_label
        self.deleted_emails_label.pack()

        self.deleted_emails_listbox = tk.Listbox(self)
        self.deleted_emails_listbox.pack()

    def delete_emails(self):
        email_address = self.email_entry.get()
        password = self.password_entry.get()
        delete_from = self.delete_from_entry.get()
        deleted_count = 0

        # Connect to the mail server
        mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        mail.login(email_address, password)

        # Check if connection is still open
        status, _ = mail.noop()
        if status != 'OK':
            messagebox.showerror("Error", "Connection to email server lost")
            return

        # Select the inbox
        mail.select("inbox")

        # Search for specific email
        status, messages = mail.search(None, f'FROM "{delete_from}"')

        if messages[0]:
             messages = messages[0].decode("utf-8").split(" ")
             for message in messages:
               status, data = mail.status("inbox", "(MESSAGES)")
               num_messages = data[0].decode("utf-8").split()[-1]
               if int(message) <= int(num_messages[:-1]):
                    _, data = mail.fetch(message, "(RFC822)")
                    msg = email.message_from_bytes(data[0][1])
                    print(f"Deleted email with subject: {msg['subject']}")
                    mail.store(message, '+FLAGS', '\\Deleted')
                    deleted_count += 1
                    mail.expunge()
        else:
            messagebox.showinfo("Info", "No emails to delete")

        # Close mailbox
        mail.close()

        if deleted_count:
             mail.expunge()
             messagebox.showinfo("Info", f"{deleted_count} emails were deleted")

        # Fetch remaining emails
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        if messages[0]:
          print("check 1")
          messages = messages[0].decode("utf-8").split(" ")
          for message in messages:
              status, data = mail.status("inbox", "(MESSAGES)")
              num_messages = data[0].decode("utf-8").split()[-1]
              if int(message) <= int(num_messages[:-1]):
                  _, data = mail.fetch(message, "(RFC822)")
                  print(data, 2)
                  if data:
                      msg = email.message_from_bytes(data[0][1])
                      self.remaining_emails_listbox.insert(tk.END, msg['subject'])
app = EmailDeleterApp()
app.mainloop()
