import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import pandas as pd

# 1. Email account credentials
## Email credentials should be in a password.env file in the "code folder"
load_dotenv("password.env")  # Load environment variables from .env file\
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")




# 2. Load the CSV data
csv_file = "csv/practice_email.csv"  # Replace with your CSV file
draft_file = "txt/example.txt"

data = pd.read_csv(csv_file)

# 3. Load the draft email template
with open(draft_file, "r") as file:
    draft_body = file.read()

# 4. Send emails
def send_emails(data):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("Logged in successfully!")

        for _, row in data.iterrows():
            # variables = row['column_name]
            name = row['name']
            email = row['email']

            # Format the email body
            email_body = draft_body.format(
                name=name
            )

            # Create the MIME email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = f"Hey {name}, how are you?"
            msg.attach(MIMEText(email_body, 'plain'))

            # Send the email
            server.send_message(msg)
            print(f"Email sent to {email}")

        server.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

# 5. Run the script
if __name__ == "__main__":
    send_emails(data)
