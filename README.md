from flask import Flask, render_template
from exchangelib import Credentials, Account, DELEGATE

app = Flask(__name__)

def get_emails():
    credentials = Credentials('your_email@example.com', 'your_password')
    account = Account('shared_mailbox@example.com', credentials=credentials, autodiscover=True, access_type=DELEGATE)
    
    emails = []
    for item in account.inbox.all().order_by('-datetime_received')[:100]:
        emails.append({
            'subject': item.subject,
            'body': item.text_body,
            'sender': item.sender.email_address
        })
    return emails

@app.route('/')
def index():
    emails = get_emails()
    return render_template('index.html', emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
