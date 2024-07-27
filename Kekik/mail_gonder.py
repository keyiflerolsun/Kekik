# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

# from validate_email       import validate_email
# from logging              import getLogger
# getLogger("validate_email").setLevel("ERROR")

from typing                 import Union
from smtplib                import SMTP
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from email.mime.application import MIMEApplication
from email.utils            import formataddr, formatdate, make_msgid
from pytz                   import timezone
from datetime               import datetime

async def mail_gonder(
    host:str,
    port:Union[int, str],
    kullanici:str,
    sifre:str,
    gonderen_adi:str,
    gonderen_mail:str,
    alici_adi:str,
    alici_mail:str,
    konu:str,
    icerik:str="",
    html:bool=False,
    dosya_yolu:str=None
) -> bool:
    # if not validate_email(alici_mail):
    #     return False

    mesaj = MIMEMultipart("alternative")
    mesaj["Subject"]    = konu
    mesaj["From"]       = formataddr((gonderen_adi, gonderen_mail))
    mesaj["To"]         = formataddr((alici_adi, alici_mail))
    mesaj["Message-ID"] = make_msgid(domain=gonderen_mail.split("@")[-1])  # Message-ID başlığını ekle
    # mesaj["Date"]       = formatdate(localtime=True)
    mesaj["Date"]       = datetime.now(timezone("Europe/Istanbul")).strftime("%a, %d %b %Y %H:%M:%S %z")

    mesaj.attach(MIMEText(icerik, "html") if html else MIMEText(icerik, "plain"))

    if dosya_yolu:
        with open(dosya_yolu, "rb") as dosya:
            part = MIMEApplication(dosya.read(), Name=dosya_yolu)
            part["Content-Disposition"] = f'attachment; filename="{dosya_yolu}"'
            mesaj.attach(part)

    smtp = SMTP(host, int(port))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(kullanici, sifre)
    smtp.sendmail(gonderen_mail, alici_mail, mesaj.as_string())
    smtp.quit()

    return True