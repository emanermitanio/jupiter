from flask import Flask, render_template
import win32com.client

app = Flask(__name__)

def get_emails():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    # Replace 'Shared Mailbox' with the name of your shared mailbox
    shared_mailbox = outlook.Folders("Shared Mailbox")
    inbox = shared_mailbox.Folders("Inbox")
    messages = inbox.Items

    email_data = []
    for message in messages:
        email_info = {
            "subject": message.Subject,
            "sender": message.SenderName,
            "received_time": message.ReceivedTime,
            "body": message.Body
        }
        email_data.append(email_info)
    
    return email_data

@app.route('/')
def index():
    emails = get_emails()
    return render_template('index.html', emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
