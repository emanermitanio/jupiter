import os
from exchangelib import DELEGATE, Account, Credentials, Configuration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    exchange_server = os.getenv('EXCHANGE_SERVER')

    try:
        # Set up credentials and configuration
        credentials = Credentials(email, password)
        config = Configuration(server=exchange_server, credentials=credentials)
        account = Account(email, config=config, autodiscover=False, access_type=DELEGATE)

        # Access the inbox
        inbox = account.inbox
        # Fetch the first 5 emails
        items = inbox.all().order_by('-datetime_received')[:5]

        # Print details of fetched emails
        for item in items:
            print(f"Subject: {item.subject}")
            print(f"Sender: {item.sender.email_address}")
            print(f"Received: {item.datetime_received}")
            print("-" * 30)

        print("Connection to the Exchange server was successful!")

    except Exception as e:
        print(f"Failed to connect to the Exchange server: {e}")

if __name__ == '__main__':
    test_connection()
