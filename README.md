from flask import Flask, render_template
from exchangelib import Credentials, Account, Configuration, DELEGATE

app = Flask(__name__)

def get_emails():
    credentials = Credentials('your_email@example.com', 'your_password')
    config = Configuration(
        server='your_ews_server',  # e.g., 'outlook.office365.com'
        credentials=credentials
    )
    account = Account(
        'shared_mailbox@example.com',
        config=config,
        autodiscover=False,  # Disable autodiscover
        access_type=DELEGATE
    )

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
