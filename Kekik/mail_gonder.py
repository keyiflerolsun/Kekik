# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

def mail_gonder(host:str, port:Union[int, str], mail:str, sifre:str, alici:str, konu:str, icerik:str, html:bool=False):
    mesaj = MIMEMultipart('alternative')
    mesaj['Subject'] = konu
    mesaj['From']    = mail
    mesaj['To']      = alici

    mesaj.attach(MIMEText(icerik, 'html') if html else MIMEText(icerik, 'plain'))

    smtp = SMTP(host, int(port))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(mail, sifre)
    smtp.sendmail(mail, alici, mesaj.as_string())
    smtp.quit()
