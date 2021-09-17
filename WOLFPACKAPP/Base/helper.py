from django.conf import settings
import jwt
import hashlib
import pickle


class ResponseObject:

    def __init__(self, response_message, response_object, http_status=200):
        self.http_status = http_status
        self.response_message = response_message
        self.response_object = response_object

class RequestConfig:

    def __init__(self, from_session=False, default=None, nullable=True, datatype=str, session_key=None):
        self.from_session = from_session
        self.default = default
        self.nullable = nullable
        self.datatype = datatype
        self.session_key = session_key


class JWTManager:

    @staticmethod
    def generate_token(payload: dict):
        # return jwt.encode(payload, 'KARTHIK@12345', algorithm='HS256').decode("utf-8")
        return jwt.encode(payload, 'KARTHIK@12345', algorithm='HS256')

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, 'KARTHIK@12345', algorithms=['HS256'])
        return payload

    @staticmethod
    def get_payload_value_by_key(payload, key):
        return payload.get(key, None)

    @staticmethod
    def get_token_value_by_key(token, key):
        payload = JWTManager.decode_token(token)
        return payload.get(key, None)

    @staticmethod
    def get_checksum(data):
        return hashlib.md5(pickle.dumps(data)).hexdigest()


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


class EmailHelper:

    def __init__(self):
        self.host = "smtp.gmail.com"
        self.from_email = "karthikravinatha@gmail.com"
        self.password = "9448255692love"
        self.port = 587

def send_html_email(self, email_subject, email_body, email_recipients):
    host = "smtp.gmail.com"
    from_email = "karthikravinatha@gmail.com"
    password = "9448255692love"
    port = 587
    smtp = smtplib.SMTP(host= host, port= port)
    smtp.starttls()
    smtp.login(from_email, password)

    msg = MIMEMultipart()

    msg['From'] = self.from_email
    msg['To'] = ["karthikravinatha@gmail.com"]#email_recipients
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_body, 'html'))    

    smtp.send_message(msg)