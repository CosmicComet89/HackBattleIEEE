import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import csv

email_user = 'senthurkumaran2004@gmail.com'
email_pass = 'llzs ydsg wrtk xsip'
email_server = 'imap.gmail.com'  


mail = imaplib.IMAP4_SSL(email_server)
mail.login(email_user, email_pass)


mail.select("inbox")



END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=7)

end_date_str = END_DATE.strftime("%d-%b-%Y")
start_date_str = START_DATE.strftime("%d-%b-%Y")

search_criteria = f'(SINCE "{start_date_str}" BEFORE "{end_date_str}")'

status, email_ids = mail.search(None, search_criteria)


email_subjects = []

for email_id in email_ids[0].split():
    status, email_data = mail.fetch(email_id, "(RFC822)")
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    

    subject, charset = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(charset if charset else 'utf-8')
    
    email_subjects.append(subject)

print("Email Subjects for the Last 7 Days:")
for subject in email_subjects:
    print(subject)

csv_filename = 'email_subjects.csv' 
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Email Subject']) 
    writer.writerows([[subject] for subject in email_subjects])  

mail.logout()
