# <img src="https://www.akashtrehan.com/assets/images/emoji/terminal.png" height="48" align="center"> Kekik

![Repo Boyutu](https://img.shields.io/github/repo-size/keyiflerolsun/Kekik) ![Views](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/keyiflerolsun/Kekik&title=Profile%20Views) [![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/keyiflerolsun/Kekik)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Kekik)
![PyPI - Status](https://img.shields.io/pypi/status/Kekik)
![PyPI](https://img.shields.io/pypi/v/Kekik)
![PyPI - Downloads](https://img.shields.io/pypi/dm/Kekik)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/Kekik)
![PyPI - License](https://img.shields.io/pypi/l/Kekik)

*İşlerimizi kolaylaştıracak fonksiyonların el altında durduğu kütüphane..*

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/keyiflerolsun/)

## 🚀 Kurulum

```bash
# Yüklemek
pip install Kekik

# Güncellemek
pip install -U Kekik
```

## <img src="https://i.imgur.com/ETZ1ABF.png" height="24" align="center"> Kullanım

### **[slugify](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/slugify.py)**
```python
from Kekik import slugify

print(slugify("Ömer Faruk Sancak"))

# » omer-faruk-sancak
```

### **[link_ayikla](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/link_islemleri.py)**
```python
from Kekik import link_ayikla

print(link_ayikla("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ornare nec turpis at mollis. Aenean iaculis metus libero, a rhoncus justo suscipit quis. Suspendisse sodales ante eros. Curabitur sagittis massa lacus, vel placerat turpis aliquet ac. Nulla porta cursus consequat. Etiam tristique vestibulum maximus. Vestibulum scelerisque vehicula ex, non feugiat eros placerat a. Cras eleifend cursus felis. Nullam pulvinar dictum purus, eu lobortis sapien posuere accumsan. Integer suscipit nisi diam, nec gravida eros malesuada a. Sed vestibulum sollicitudin ex ut volutpat. Phasellus non magna sed neque blandit vestibulum vitae nec ante. https://google.com Proin fringilla ligula nec metus sagittis venenatis."))

# ['https://google.com']
```

### **[youtube_link_mi](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/link_islemleri.py)**
```python
from Kekik import youtube_link_mi

print(youtube_link_mi("https://google.com"))

# False
```

### **[okunabilir_byte](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/okunabilir_byte.py)**
```python
from Kekik import okunabilir_byte

print(okunabilir_byte(132456498564))

# 123.36 GB
```

### **[zaman_donustur](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/zaman_donustur.py)**
```python
from Kekik import zaman_donustur

print(zaman_donustur(123456))

# 1 gün, 10 saat, 17 dakika, 36 saniye
```

### **[qr_ver](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/qr_ver.py)**
```python
from Kekik import qr_ver

print(qr_ver("keyiflerolsun"))

                         
#   █▀▀▀▀▀█ ▀▀▀▄▀ █▀▀▀▀▀█  
#   █ ███ █ ▀█ ██ █ ███ █  
#   █ ▀▀▀ █ ▄▄▄██ █ ▀▀▀ █  
#   ▀▀▀▀▀▀▀ ▀▄▀ █ ▀▀▀▀▀▀▀  
#   ▀▄█ ▄ ▀█▄▀▄    █▄▄▀ █  
#   ▀▀▄▄██▀█ ▄▄▀██ ▄▀▄▀▄█  
#     ▀  ▀▀▀███ ▄█▄ █ ▄▀▄  
#   █▀▀▀▀▀█ ▀ ▀▄▀▄  ▀▄▀▄▀  
#   █ ███ █  ▄█▄██▄ ▄▀▄    
#   █ ▀▀▀ █ ▀█▀▄██▀ █▄▀▀▀  
#   ▀▀▀▀▀▀▀ ▀ ▀▀▀   ▀▀  ▀  
```

### **[csv2dict](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/csv2dict.py)**
```python
from Kekik import csv2dict

print(csv2dict('Config/ALICILAR.csv'))

# [{'mail': 'keyiflerolsun@gmail.com', 'isim': 'Ömer Faruk'}, {'mail': 'bakalim@gmail.com', 'isim': ''}]
```

### **[dict2json](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/dict2json.py)**
### **[dosya_indir](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/dosya_indir.py)**
### **[benim_hwid](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/hwid_kontrol.py)**
### **[hwid_kontrol](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/hwid_kontrol.py)**
### **[satir_ekle](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/txt_fetis.py)**
### **[satirlar_ekle](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/txt_fetis.py)**
### **[satir_sil](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/txt_fetis.py)**
### **[list2html](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/list2html.py)**
### **[mail_gonder](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/mail_gonder.py)**

## 💸 Bağış Yap

**[☕️ Kahve Ismarla](https://KekikAkademi.org/Kahve)**

## 🌐 Telif Hakkı ve Lisans

* *Copyright (C) 2022 by* [keyiflerolsun](https://github.com/keyiflerolsun) ❤️️
* [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](https://github.com/keyiflerolsun/Kekik/blob/master/LICENSE) *Koşullarına göre lisanslanmıştır..*

## ♻️ İletişim

*Benimle iletişime geçmek isterseniz, **Telegram**'dan mesaj göndermekten çekinmeyin;* [@keyiflerolsun](https://t.me/keyiflerolsun)

##

> **[@KekikAkademi](https://t.me/KekikAkademi)** *için yazılmıştır..*