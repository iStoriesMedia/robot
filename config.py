import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('PASSWORD')
