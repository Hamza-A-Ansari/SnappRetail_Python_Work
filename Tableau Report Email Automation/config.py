# Statement for enabling the development environment
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()

tableau_user = os.getenv("tableau_user")
tableau_passwd = os.getenv("tableau_passwd")
tableau_server = os.getenv("tableau_server")
sender_email =os.getenv("email_address")
sender_password = os.getenv("email_password")
tableau_version=os.getenv('tableau_version')
recipient_email = os.getenv('recipient_email')
smtp_server = os.getenv('smtp_server')
smtp_port = os.getenv('smtp_port')




