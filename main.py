import os
from dotenv import load_dotenv
from imapclient import IMAPClient
import email

load_dotenv()
#now have access to uid and pass and monitoremail

host = 'imap.gmail.com'
user = os.getenv("uid")
password = os.getenv("pass")
ssl = True

server = IMAPClient(host, use_uid=True, ssl=ssl)
server.login(user, password)
server.select_folder("INBOX")
messages = server.search(['NOT','DELETED', u'FLAGGED'])

for uid, message_data in server.fetch(messages, "RFC822").items():
        email_message = email.message_from_bytes(message_data[b"RFC822"])
        print(uid, email_message.get("From"), email_message.get("Subject"))


#for msgid, data in response.items():
#
#        parsedEmail = email.message_from_string('RFC822')
#        body = email.message_from_string('BODY[TEXT]')
#        #parsedBody = parsedEmail.get_payload(0)
#        print(parsedEmail)

server.logout()