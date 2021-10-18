import os
from dotenv import load_dotenv
from imapclient import IMAPClient
import email

load_dotenv()
#now have access to uid and pass and monitoremail
#login to email server and setup
host = 'imap.gmail.com'
user = os.getenv("uid")
password = os.getenv("pass")
ssl = True

#create server, login, and search inbox for messages
server = IMAPClient(host, use_uid=True, ssl=ssl)
server.login(user, password)
server.select_folder("INBOX")
messages = server.search([['NOT','DELETED'], [u'FLAGGED']])

#get most recent messages [-1] (last item in list) and print info
for uid, message_data in server.fetch(messages[-1], "RFC822").items():
        email_message = email.message_from_bytes(message_data[b"RFC822"])

        #write subject line to file
        #Debugging email content v
        #print(uid, email_message.get("From"))
        #print("Subject: ",email_message.get("Subject"))
        #print("Body: \n",email_message.get_payload()[0])

        subject = email_message.get("Subject")
        print(subject)

server.logout()
