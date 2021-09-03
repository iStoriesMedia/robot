from config import SENDER_EMAIL, EMAIL_PASSWORD
from datetime import datetime, timedelta
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from error_handller import missing_dict_key_handler

def create_message(top_contracts, region):

    for el in top_contracts:
        el['region'] = region
        inn = el.get('suppliers_inn')
        
        if el.get('signDate') is not None:
            el['signDate'] = el['signDate'].split('T')[0] 
        if el['signDate'] is not None and el['company_date'] is not None:
            contract_date = datetime.strptime(el['signDate'], '%Y-%m-%d')
            company_date = datetime.strptime(el['company_date'], '%Y-%m-%d')
            el['date_difference'] = (contract_date - company_date).days 
        else:
            el['date_difference'] = None
        
        
    env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('index.html')

    message = template.render(items=top_contracts)

    return message


def send_empty_email(date, email_list, region):

    msg = EmailMessage()
    msg['Subject'] = f"Контракты за {date} в регионе {region} не обнаружены"
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(email_list)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)


def send_email_with_contracts(message, email_list):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Топ-10 госконтрактов"
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(email_list)

    part1 = MIMEText(message, 'html')
    msg.attach(part1)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)

def error_message(error):

    msg = EmailMessage()
    msg.set_content(error)
    msg['Subject'] = "Ошибка"
    msg['From'] = SENDER_EMAIL
    msg['To'] = 'YOUR MAIL'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == "__main__":
    send_email_with_contracts(message)
    send_empty_email(date, email, region)
    error_message(error)