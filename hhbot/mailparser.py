from settings.settings import EMAIL, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER
import imaplib
import email as emaillib
from bs4 import BeautifulSoup
import traceback
import re
import base64


def _get_latest_email():
    try:
        imap_session = imaplib.IMAP4_SSL(SMTP_SERVER)
        imap_session.login(EMAIL,EMAIL_PASSWORD)
        status, messages = imap_session.select("INBOX")
        latest_email_id = int(messages[0])
        latest_email = imap_session.fetch(str(latest_email_id), '(RFC822)')
        assert latest_email is not None

    except Exception as e:
        traceback.print_exc()
        print(str(e))

    finally:
        imap_session.close()
        imap_session.logout()
    
    return _get_body_of(latest_email)

def _check_headers_of(msg):
    email_subject = emaillib.header.decode_header(msg['subject'])
    email_subject = str(email_subject[0][0], 'utf-8') 
    email_from = msg['from']
    if email_subject != 'Код подтверждения' or email_from != '"hh.ru" <noreply@hh.ru>':
        print("Incorrect email")
        print('From : ' + email_from + '\n')
        print('Subject : ' + email_subject + '\n')
        return False
    
    return True


def _get_body_of(email):
    for response_part in email:
        arr = response_part[0]
        if isinstance(arr, tuple):
            msg = emaillib.message_from_string(str(arr[1],'utf-8'))
            if _check_headers_of(msg) and msg.get_content_type() == "text/html":
                body = msg.get_payload(decode=True).decode()
                return body

    return None


def get_email_key():
    email_body = _get_latest_email()
    if email_body is None:
        # or exception
        return None

    soup = BeautifulSoup (email_body, 'html.parser')
    return soup.find("b", string=re.compile("\d\d\d\d")).string