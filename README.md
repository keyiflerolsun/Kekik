# <img src="https://www.akashtrehan.com/assets/images/emoji/terminal.png" height="42" align="center"> Kekik

[![Boyut](https://img.shields.io/github/repo-size/keyiflerolsun/Kekik?logo=git&logoColor=white&label=Boyut)](#)
[![Görüntülenme](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/keyiflerolsun/Kekik&title=Görüntülenme)](#)
<a href="https://KekikAkademi.org/Kahve" target="_blank"><img src="https://img.shields.io/badge/☕️-Kahve Ismarla-ffdd00" title="☕️ Kahve Ismarla" style="padding-left:5px;"></a>

[![PyPI](https://img.shields.io/pypi/v/Kekik?logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/Kekik)
[![PyPI - Yüklenme](https://img.shields.io/pypi/dm/Kekik?logo=pypi&logoColor=white&label=Yüklenme)](https://pypi.org/project/Kekik)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/Kekik?logo=pypi&logoColor=white&label=Wheel)](https://pypi.org/project/Kekik)

[![Python Version](https://img.shields.io/pypi/pyversions/Kekik?logo=python&logoColor=white&label=Python)](#)
[![Lisans](https://img.shields.io/pypi/l/Kekik?logo=gnu&logoColor=white&label=Lisans)](#)
[![Durum](https://img.shields.io/pypi/status/Kekik?logo=windowsterminal&logoColor=white&label=Durum)](#)

[![PyPI Yükle](https://github.com/keyiflerolsun/Kekik/actions/workflows/pypiYukle.yml/badge.svg)](https://github.com/keyiflerolsun/Kekik/actions/workflows/pypiYukle.yml)

*İşlerimizi kolaylaştıracak fonksiyonların el altında durduğu kütüphane..*

[![ForTheBadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](https://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/keyiflerolsun/)

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

### **[unicode_tr](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/unicode_tr.py)**
```python
from Kekik import unicode_tr

print(unicode_tr(u"izmir istanbul").title())

# » İzmir İstanbul
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
from Kekik import sure2saniye, zaman_donustur

kac_saniye = sure2saniye("15:23")
print(kac_saniye)
# 923

zaman_donustur(kac_saniye)
# 15 dakika, 23 saniye
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

### **[dict2csv](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/dict2csv.py)**
```python
from Kekik import dict2csv

print(dict2csv('Config/ALICILAR.csv', [{'isim': 'Ömer Faruk', 'soyisim': 'Sancak'}, {'isim': 'Kekik', 'soyisim': 'Akademi'}]))

# True
```

### **[dosya2set](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/dosya2set.py)**
```python
from Kekik import dosya2set

print(dosya2set("_config.yml"))

# {'theme: jekyll-theme-cayman', 'show_downloads: false'}
```

### **[proxy_ver](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/proxy_ver.py)**
```python
from Kekik import proxy_ver

print(proxy_ver("Proxiler.txt", "requests"))

# {'http': 'http://keyiflerolsun:KekikAkademi@127.0.0.1:3310', 'https': 'http://keyiflerolsun:KekikAkademi@127.0.0.1:3310'}

print(proxy_ver("Proxiler.txt", "aiohttp"))

# ('http://127.0.0.1:3310', BasicAuth(login='keyiflerolsun', password='KekikAkademi', encoding='utf-8'))

print(proxy_ver("proxiler.txt", "selenium"))

# 127.0.0.1:3310:keyiflerolsun:KekikAkademi
```

### **[kisi_ver](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/kisi_ver.py)**
```python
from Kekik import kisi_ver

print(kisi_ver("tr"))

# {'isim': 'Selami', 'soyisim': 'Tokatlioğlu', 'kullanici_adi': 'Sela27Toka', 'biyografi': 'En bilge adamlar kendi yönlerini takip ederler.', 'profil_resmi': 'tmp/Sela27Toka.jpg'}

print(kisi_ver("en"))

# {'isim': 'Laurel', 'soyisim': 'Blake', 'kullanici_adi': 'Laur42Blak', 'biyografi': 'From little acorns mighty oaks do grow.', 'profil_resmi': 'tmp/Laur42Blak.jpg'}
```

### **[Nesne](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Nesne.py)**
```python
from Kekik import Nesne

nesne = Nesne({"Merhaba": "Dünya"})

print(nesne)
# Nesne(Merhaba=Dünya)

nesne.gorsel(girinti=0, kademe=1)
'''
Nesne(
        Merhaba=...
)
'''

print(nesne.Merhaba)
# Dünya
```

### **[liste_fetis](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/liste_fetis.py)**
```python
from Kekik import liste_fetis

liste = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

liste_fetis.n_adete_bol(liste, adet=3)
# [[1, 4, 7, 10], [2, 5, 8], [3, 6, 9]]

liste_fetis.n_er_hale_getir(liste, adet=3)
# [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
```

### **[BIST](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/BIST.py)**
```python
from Kekik import BIST

print(BIST.marketler)
# {'XU100': ['AEFES', 'AGHOL', 'AKBNK', 'AKFGY', 'AKSA', 'AKSEN', 'ALARK', 'ALBRK', 'ALFAS', 'ALKIM', 'ARCLK', 'ASELS', 'ASUZU', 'AYDEM', 'BAGFS', 'BASGZ', 'BERA', 'BIMAS', 'BIOEN', 'BRYAT', 'BUCIM', 'CCOLA', 'CEMTS', 'CIMSA', 'DOAS', 'DOHOL', 'ECILC', 'EGEEN', 'EKGYO', 'ENJSA', 'ENKAI', 'ERBOS', 'EREGL', 'EUREN', 'FENER', 'FROTO', 'GARAN', 'GENIL', 'GESAN', 'GLYHO', 'GSDHO', 'GUBRF', 'GWIND', 'HALKB', 'HEKTS', 'IPEKE', 'ISCTR', 'ISDMR', 'ISGYO', 'IZMDC', 'KARSN', 'KCAER', 'KCHOL', 'KERVT', 'KLRHO', 'KMPUR', 'KONTR', 'KONYA', 'KORDS', 'KOZAA', 'KOZAL', 'KRDMD', 'KZBGY', 'MAVI', 'MGROS', 'ODAS', 'OTKAR', 'OYAKC', 'PETKM', 'PGSUS', 'PSGYO', 'SAHOL', 'SASA', 'SELEC', 'SISE', 'SKBNK', 'SMRTG', 'SNGYO', 'SOKM', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TKNSA', 'TMSN', 'TOASO', 'TSKB', 'TTKOM', 'TTRAK', 'TUKAS', 'TUPRS', 'TURSG', 'ULKER', 'ULUUN', 'VAKBN', 'VESBE', 'VESTL', 'YKBNK', 'YYLGD', 'ZOREN'], 'XU050': ['AEFES', 'AKBNK', 'AKSA', 'AKSEN', 'ALARK', 'ARCLK', 'ASELS', 'BERA', 'BIMAS', 'DOHOL', 'EGEEN', 'EKGYO', 'ENJSA', 'ENKAI', 'EREGL', 'FROTO', 'GARAN', 'GESAN', 'GUBRF', 'HALKB', 'HEKTS', 'ISCTR', 'ISGYO', 'KCHOL', 'KONTR', 'KORDS', 'KOZAA', 'KOZAL', 'KRDMD', 'MGROS', 'ODAS', 'OYAKC', 'PETKM', 'PGSUS', 'SAHOL', 'SASA', 'SISE', 'SMRTG', 'SOKM', 'TAVHL', 'TCELL', 'THYAO', 'TKFEN', 'TOASO', 'TSKB', 'TTKOM', 'TUPRS', 'VAKBN', 'VESTL', 'YKBNK'], 'XU030': ['AKBNK', 'AKSEN', 'ALARK', 'ARCLK', 'ASELS', 'BIMAS', 'EKGYO', 'ENKAI', 'EREGL', 'FROTO', 'GARAN', 'GUBRF', 'HEKTS', 'ISCTR', 'KCHOL', 'KOZAA', 'KOZAL', 'KRDMD', 'ODAS', 'PETKM', 'PGSUS', 'SAHOL', 'SASA', 'SISE', 'TAVHL', 'TCELL', 'THYAO', 'TOASO', 'TUPRS', 'YKBNK']}

print(BIST.sembol_sorgu("VESBE"))
# {'VESBE': ['XU100']}
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
### **[terminal_baslik](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/terminal_baslik.py)**

## 💸 Bağış Yap

**[☕️ Kahve Ismarla](https://KekikAkademi.org/Kahve)**

## 🌐 Telif Hakkı ve Lisans

* *Copyright (C) 2023 by* [keyiflerolsun](https://github.com/keyiflerolsun) ❤️️
* [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](https://github.com/keyiflerolsun/Kekik/blob/master/LICENSE) *Koşullarına göre lisanslanmıştır..*

## ♻️ İletişim

*Benimle iletişime geçmek isterseniz, **Telegram**'dan mesaj göndermekten çekinmeyin;* [@keyiflerolsun](https://t.me/KekikKahve)

##

> **[@KekikAkademi](https://t.me/KekikAkademi)** *için yazılmıştır..*