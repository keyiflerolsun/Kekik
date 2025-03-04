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

### **[Domain2IP](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Domain2IP.py)**
```python
from Kekik import Domain2IP

dm2ip = Domain2IP("soundcloud.com")
konsol.print(dm2ip.bilgi)
# {'domain': 'soundcloud.com', 'ipler': ['18.238.243.19', '18.238.243.27', '18.238.243.62', '18.238.243.79'], 'subnetler': ['18.238.243.0/25']}
```

### **[StringCodec](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Sifreleme/StringCodec.py)**
```python
import re, json
from Kekik.Sifreleme import StringCodec

veri = r'''
var scx = {"fastly":{"tt":"RmFzdGx5","sx":{"p":[],"t":["nUE0pUZ6Yl92nJEgo3u5YzAioF9zoP92ZKtjMGMuAGRlBN=="]},"order":4}};
'''

scx_data = json.loads(re.findall(r'scx = (.*?);', veri)[0])

link_list = []
for key in list(scx_data.keys()):
    t = scx_data[key]["sx"]["t"]
    if isinstance(t, list):
        link_list.append({key: StringCodec.decode(elem) for elem in t})
    if isinstance(t, dict):
        link_list.append({k: StringCodec.decode(v) for k, v in t.items()})

print(link_list)
# [{'fastly': 'https://vidmoxy.com/fl/v1x0e6a5128'}]
```

### **[AESManager](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Sifreleme/AESManager.py)**
```python
import re, json
from Kekik.Sifreleme import AESManager

veri = r'''
  $(document).ready(function() {
    bePlayer('S3JScTBsNzMyYlFSMHg4NG5vQXNjUT09', '{"ct":"SjkWeIotWbL6TmnwyhkeLy6wAWvEG1pz8R0g+IsLN6P1vo9WvXuiqqDal5g6FXW3Td+Q+1DIGQAt3sNxydOAr4p3uFxxpVPUwIMwLWzw+5m0ED0tno1KU0\/rCXRwq6ATvmrIqSr+qb95hY0wjm3gfjPsxDn4vJ1fcdiRwrfC38MjfKyJFN3\/n\/xLvNT4vgQJTYTEmNOzFZgEIhsSRFiW1\/8nQCaS\/8Xkw0ySUqLvzSMsVf2SSgXyESxyksn3+kz9KqEI+mQpJFUcLSBz8VKXly+tEcYGpTQChzceyudkZcEGvppKheBAarEQ6e3eR9d04gQcFpEaV+QmHODvI1Ql\/pJ1FSAh9F5ZDtF00XDSLZbIEt00PWRkgfc3kxuNQzcC1C6BULNdoGwHbvo5W6uUsMwxG+sn+EH7B7jWtyhx5VHKpIfkyrjC10+K\/hG29bkS3YNSTaDxJnTa3jj1usbwwMX0A7wApIlce4rEVgWpO5y1ZuiJ+tEE3kH1InUzT1jfY4Y0KrZ5X+p2nrQhJrDOxfDy\/GhaidNmmpfuzF6Iniko6sCGa0QRbhVB8ZbrC9qFB\/sk47ZOP1IHPY\/jCh4BTFMDCy1Qx1\/PbVLZzNLHju\/cLYRzS0vJp5aqkwg\/QNCo1q5HrxXL32lMLNOcWPRDqyZaMpiYP+LzJPVndLsqGlfKJWETuKonEqc4r4M0Eu\/bTji\/S7zQ7bvEPuT3PyIRWXDffuNSX6+nqWFD8LM\/iNyc1cC3bMi+p0TR3YZu1MlIvxjYPK0lYtDvd+vaYgCotFm0lLsqg5cuw3pGb8jnEfM1VzEqDcBvBTkRKrxIao\/WWdvGf1MCmTsr+nVH0sT8PTrh6XcoG7hV\/+y8XCsEj2LKWtDtfK+RxSztteXYUUUI9NVtCvjlW\/b8+h6u+B\/CNLtrwoDQzKhTVZ1rZbe\/TP+HR7SkMXYqyAX3qqiyi9s+TrcqkxdbAHzkjr0q2DshtUeipcL5HVrdxL28iXqtYMT\/ytsRCQHpnswNGqW+D47VAYtDl4VafSaNGUMPfu6nq4k0\/FrxtYkts4lE9YUkueQHip8eOFO8dxTp8O7+Civt88C45wEjBHqaiN+n6wm1+3xUy2hKX0PD4gvlPuUeoHDbm\/HLUlPYmGw5cCEAskuJRXdW+gnFB6XzVIKrF7OUtd2yLqSLhnWcSFkMJoPDuIezn1D60pMi8LlJKb1HXwbPRRcqh00\/bFNdmodGpwybcaeegvRaCJbDqd6fmQUxG1ir9o5O8st2\/oJ9\/HivYvxi\/sicZYNzFtuZFGC\/ubPK5Ld9RsJb\/RQ9rkTZzhkBnmM=","iv":"2fedfd8ae68165490f274b521d5a3291","s":"74a525e8e5746772"}');
  });
'''

be_player      = re.search(r"bePlayer\('([^']+)',\s*'(\{[^\}]+\})'\);", veri).groups()
be_player_pass = be_player[0]
be_player_data = be_player[1]

print(json.loads(AESManager.decrypt(be_player_data, be_player_pass).replace("\\", "")))
# {'schedule': {'client': 'vast', 'schedule': [{'offset': 'pre', 'tag': ' https://v.adserve.tv/pg/vast.xml', 'skipoffset': '10', 'skipmessage': '{{LANG Skip_Ad}} XX'}]}, 'adsecond': 0, 'bannerad': None, 'title': 'Doraemon', 'description': '1.Sezon 13.Bu00f6lu00fcm', 'video_location': 'https://mucize.online/list/M2EyVVE0elFFTnRIWXFWOHpwenJIUkdyU29Rclg1aEwvc0Q0dE4zajRQa3I2Yi95TVpWbG41T21aTFQ4TnlKUDVCVkUvVFpBMjl3NG94OHhWaWYzZlVCdStSczRXd0FZRUpmSWQraDZjMGZNQTZqY1FOMWhYRUZqZFF2NC9sMlQ5N2JnKzdtTGpKNFdTK2hBSmM1a3JPWitpMkdlVXlRUjMzeG5TbUhxOU44PQ==', 'images': 'https://mucize.online/upload/photos/2023/12/66dfa35da16bb3dab97a866ac31cca239wLRrDBRGtCD68BRF7BsD0RHHQ3.jpg', 'watermark': 'themes/dosyaload/img/logoo.png', 'link': None, 'vast': 'off', 'dwlink': 'https://mucize.online/download/3302', 'exit': False, 'intro': '', 'outro': None, 'video_id': 3302, 'siteurl': None, 'urls': None, 'referer': 'cizgimax.online', 'sitex': ['https://hls.bepeak.net', 'http://localhost'], 'dws': False, 'download': False}
```

### **[Packer](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Sifreleme/Packer.py)**
```python
import re
from Kekik.Sifreleme import Packer

veri = r'''
        qualityLabels: {"1661":"720p","814":"480p","524":"360p"},
            };
eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('1d(17(p,a,c,k,e,d){e=17(c){18(c<a?\'\':e(1D(c/a)))+((c=c%a)>1w?1c.1C(c+29):c.1B(1z))};1a(!\'\'.19(/^/,1c)){1b(c--){d[e(c)]=k[c]||e(c)}k=[17(e){18 d[e]}];e=17(){18\'\\\\w+\'};c=1};1b(c--){1a(k[c]){p=p.19(1y 1x(\'\\\\b\'+e(c)+\'\\\\b\',\'g\'),k[c])}}18 p}(\'G.H=[{"16":M,"D":"\\\\w\\\\2\\\\2\\\\5\\\\y\\\\N\\\\e\\\\e\\\\i\\\\l\\\\x\\\\a\\\\6\\\\P\\\\f\\\\h\\\\y\\\\5\\\\Q\\\\2\\\\x\\\\d\\\\L\\\\9\\\\9\\\\e\\\\1\\\\l\\\\e\\\\8\\\\2\\\\m\\\\4\\\\8\\\\k\\\\b\\\\s\\\\J\\\\k\\\\n\\\\p\\\\v\\\\3\\\\q\\\\A\\\\c\\\\r\\\\3\\\\d\\\\1\\\\d\\\\j\\\\4\\\\E\\\\2\\\\5\\\\7\\\\1\\\\8\\\\j\\\\1\\\\d\\\\1\\\\t\\\\q\\\\b\\\\K\\\\4\\\\s\\\\t\\\\O\\\\b\\\\6\\\\F\\\\W\\\\q\\\\n\\\\V\\\\3\\\\6\\\\6\\\\z\\\\f\\\\c\\\\I\\\\4\\\\1\\\\c\\\\C\\\\6\\\\3\\\\o\\\\w\\\\l\\\\9\\\\r\\\\m\\\\b\\\\a\\\\m\\\\u\\\\B\\\\p\\\\k\\\\5\\\\9\\\\7\\\\v\\\\z\\\\A\\\\B\\\\7\\\\C\\\\u\\\\E\\\\Y\\\\2\\\\L\\\\K\\\\J\\\\7\\\\g\\\\8\\\\3\\\\a\\\\i\\\\5\\\\g\\\\g\\\\h\\\\15\\\\h\\\\i\\\\1\\\\F\\\\j\\\\a\\\\2\\\\1\\\\I\\\\f\\\\o\\\\14\\\\c\\\\n\\\\p\\\\o\\\\3\\\\13\\\\12\\\\4","11":"0","10":"Z","X":"U"}];T S=R(G.H[0].D);\',1F,1G,\'|1H|1I|1J|1u|1L|1E|1v|1p|1t|1f|1g|1h|1i|1N|1j|1k|1e|1m|1n|1o|1l|1q|1r|1s|1M|1K|1O|1P|2e|2f|2g|2h|2i|2m|2j|2k|2l|2c|2n|2o|2p|2q|2r|2s|2t|2u|2d|2b|1Z|28|1Q|1R|1S|1T|1U|1V|1W|1X|2a|1Y|20|21|22|23|24|25|26|27\'.1A(\'|\'),0,{}))',62,155,'|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||function|return|replace|if|while|String|eval|x65|x69|x5a|x47|x62|x67|x46|x32|x64|x30|x51|x4e|x4f|x41|x38|x7a|x31|x57|35|RegExp|new|36|split|toString|fromCharCode|parseInt|x6d|62|69|x66|x74|x6c|x58|x70|x6b|x2f|x33|x6a|x61|x6f|getLocation|mu|var|none|x37|x71|x4d|x3a|hls|type|label|x72|x76|x52|x6e|default|x77||preload|true|x42|x75|x50|x63|x78|x68|x2e|x4b|x45|x4c|x73|file|x79|x48|jwSetup|sources|x59|x44|x55'.split('|'),0,{}));
var played = 0;
'''

eval_jwSetup = re.compile(r'\};\s*(eval\(function[\s\S]*?)var played = \d+;').findall(veri)[0]
print(Packer.unpack(Packer.unpack(eval_jwSetup)))
# jwSetup.sources=[{"default":true,"file":"\x68\x74\x74\x70\x73\x3a\x2f\x2f\x64\x32\x2e\x69\x6d\x61\x67\x65\x73\x70\x6f\x74\x2e\x62\x75\x7a\x7a\x2f\x66\x32\x2f\x4e\x74\x4f\x31\x4e\x51\x5a\x6a\x44\x51\x41\x6b\x78\x6c\x58\x45\x47\x33\x6c\x62\x66\x62\x30\x31\x79\x74\x70\x57\x66\x4e\x30\x66\x62\x66\x50\x58\x5a\x55\x31\x6a\x50\x77\x5a\x6d\x48\x71\x58\x41\x37\x6c\x6d\x6d\x4b\x67\x47\x59\x31\x66\x47\x42\x6d\x6c\x38\x68\x32\x7a\x33\x4f\x5a\x69\x4f\x63\x4c\x6b\x51\x70\x7a\x57\x78\x4b\x45\x4c\x57\x42\x63\x79\x4d\x74\x75\x55\x44\x57\x46\x4e\x6c\x69\x64\x70\x46\x46\x65\x6e\x65\x64\x66\x48\x30\x69\x74\x66\x59\x67\x38\x52\x47\x41\x6b\x38\x6c\x76\x72\x31","label":"0","type":"hls","preload":"none"}];var mu=getLocation(jwSetup.sources[0].file);

# ! Veya

while Packer.detect_packed(veri):
    veri = Packer.unpack(veri)
```

### **[CryptoJS](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Sifreleme/CryptoJS.py)**
```python
import re
from Kekik.Sifreleme import CryptoJS

veri = r'''
<script type="text/javascript">var bytes = CryptoJS.AES.decrypt("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");document.write(bytes.toString(CryptoJS.enc.Utf8));</script>
'''

cryptData = re.search(r"CryptoJS\.AES\.decrypt\(\"(.*)\",\"", veri).group(1)
cryptPass = re.search(r"\",\"(.*)\"\);", veri).group(1)

print(CryptoJS.decrypt(cryptPass, cryptData))
# <!doctypehtml><meta charset=utf-8><meta content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover"name=viewport><meta content=noindex name=robots><title>MolySTREAM</title><style>body,html{background:#000;width:100%;height:100%}*{margin:0;padding:0}#sheplayer{width:100%!important;height:100%!important;z-index:9}</style><style>#playSheila{display:none;position:fixed;width:100%;height:100%;z-index:8;background:#000;background-image:url(https://www.molystream.net/obilet.png);background-size:100% 100%}.playSheilaBtn{position:absolute;background:#000;color:#fff;padding:1em;left:50%;top:50%;transform:translate(-50%,-50%);font-family:Arial;border-radius:10px;font-size:13px;font-weight:700;cursor:pointer}@media only screen and (max-width:600px){.playSheilaBtn{top:60%}}#sheila{background:#000;color:#fff;position:fixed;width:100%;height:100%;z-index:7}.sheilaBtns{height:100%;width:100%;display:flex;align-items:center;justify-content:center;text-align:center}.playBtnSheila{display:flex;flex-direction:column;align-items:center;padding:0 2em;text-align:center;font-family:Arial;cursor:pointer}.playBackBtnSheila{display:flex;flex-direction:column;align-items:center;padding:0 2em;text-align:center;font-family:Arial;cursor:pointer}.sheilaBtns span{padding:1em 0}.sheilaBtns img{width:50px;height:50px}</style><div id=playSheila><div class=playSheilaBtn onclick=load()>Videoyu Başlat</div></div><div id=sheila></div><div id=sheplayer></div><div style=display:none><div class="jw-reset jw-button-color jw-icon jw-icon-rewind jw-icon-inline"aria-label="10 Saniye İleri Sar"role=button tabindex=0 id=icon-forward-desktop><svg class="jw-svg-icon jw-svg-icon-rewind"focusable=false viewBox="0 0 240 240"xmlns=http://www.w3.org/2000/svg><path d=M193.14,131.08a21.57,21.57,0,0,0-17.7-10.6,21.58,21.58,0,0,0-17.7,10.6,44.77,44.77,0,0,0,0,46.3,21.63,21.63,0,0,0,17.7,10.6,21.61,21.61,0,0,0,17.7-10.6A44.77,44.77,0,0,0,193.14,131.08Zm-17.7,47.2c-7.8,0-14.4-11-14.4-24.1s6.6-24.1,14.4-24.1,14.4,11,14.4,24.1S183.34,178.28,175.44,178.28ZM132,188V137l-4.8,4.8-6.8-6.8,13-13a4.8,4.8,0,0,1,8.2,3.4v62.7ZM30.89,52.88H161V33.58c0-5.3,3.6-7.2,8-4.3l41.8,27.9a5.8,5.8,0,0,1,2.7,2.7,6,6,0,0,1-2.7,8L169,95.78c-4.4,2.9-8,1-8-4.3V72.18H45.29v96.4h48.2v19.3H30.79a4.88,4.88,0,0,1-4.8-4.8V57.78A5,5,0,0,1,30.89,52.88Z></path></svg><div class="jw-reset-text jw-tooltip jw-tooltip-forward"dir=auto><div class=jw-text>10 Saniye İleri Sar</div></div></div><div class="jw-reset jw-display-icon-container jw-display-icon-rewind"id=icon-forward-mobile><div class="jw-reset jw-button-color jw-icon jw-icon-rewind"aria-label="10 Saniye İleri Sar"role=button tabindex=0><svg class="jw-svg-icon jw-svg-icon-rewind"focusable=false viewBox="0 0 240 240"xmlns=http://www.w3.org/2000/svg><path d=M193.14,131.08a21.57,21.57,0,0,0-17.7-10.6,21.58,21.58,0,0,0-17.7,10.6,44.77,44.77,0,0,0,0,46.3,21.63,21.63,0,0,0,17.7,10.6,21.61,21.61,0,0,0,17.7-10.6A44.77,44.77,0,0,0,193.14,131.08Zm-17.7,47.2c-7.8,0-14.4-11-14.4-24.1s6.6-24.1,14.4-24.1,14.4,11,14.4,24.1S183.34,178.28,175.44,178.28ZM132,188V137l-4.8,4.8-6.8-6.8,13-13a4.8,4.8,0,0,1,8.2,3.4v62.7ZM30.89,52.88H161V33.58c0-5.3,3.6-7.2,8-4.3l41.8,27.9a5.8,5.8,0,0,1,2.7,2.7,6,6,0,0,1-2.7,8L169,95.78c-4.4,2.9-8,1-8-4.3V72.18H45.29v96.4h48.2v19.3H30.79a4.88,4.88,0,0,1-4.8-4.8V57.78A5,5,0,0,1,30.89,52.88Z></path></svg></div></div></div><script src=https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js></script><script src=https://www.molystream.net/player/jwplayer.js></script><script>jwplayer.key="ITWMv7t88JGzI0xPwW8I0+LveiXX9SWbfdmt0ArUSyc="</script><script src=https://cdn.molystream.org/assets/s.js></script><script>console.clear();var referrer=document.referrer;function UpdateQualityText(){var e=jwplayer().getQualityLevels()[jwplayer().getCurrentQuality()].label;1<e.length&&$("#QualityText").show().html("Aktif Kalite: <b>"+e+"</b>")}function deb(){devtoolsDetector.addListener(function(e,t){e?(t.checkerName&&(window.stop(),location.reload()),console.clear(),window.stop(),location.reload(),document.getElementById("sheplayer").innerHTML="MolySTREAM",window.location.href="/embed/sheila"):(console.clear(),load())}),devtoolsDetector.lanuch()}function load(){var e=document.getElementById("playSheila");e.parentNode.removeChild(e);try{if(localStorage.getItem("11666-5fdde056fb0e9042e29c0a20")){var t=document.createElement("div");t.className="sheilaBtns",t.innerHTML='<div class="playBtnSheila" onclick="loadi(1)"><img src="https://dbx.molystream.org/assets/play.svg"/><span>Başlat</span></div><div class="playBackBtnSheila"  onclick="loadi(2)"><img src="https://dbx.molystream.org/assets/playback.svg"/><span>Devam Et</span></div>',document.getElementById("sheila").appendChild(t)}else loadi("1")}catch(e){loadi("1")}}function loadi(e){document.getElementById("sheila").innerHTML="",console.clear();var t=!1;e&&(t=!0);var a=jwplayer("sheplayer").setup({file:"https://dbx.molystream.org/embed/sheila/11666-5fdde056fb0e9042e29c0a20",tracks:[null,null],type:"application/vnd.apple.mpegurl",playbackRateControls:!0,image:"",autostart:t});a.once("play",function(){try{"2"==e&&a.seek(localStorage.getItem("11666-5fdde056fb0e9042e29c0a20"))}catch(e){}UpdateQualityText()}),a.on("ready",function(){($("#icon-forward-desktop").insertAfter(".jw-icon-rewind:eq(1)"),$("#icon-forward-mobile").insertAfter(".jw-display-icon-display"),$(".jw-display-icon-next").hide(),$("#icon-forward-desktop, #icon-forward-mobile").click(function(){jwplayer().seek(jwplayer().getPosition()+10)}),$(".jw-button-container #icon-forward-desktop").mouseenter(function(){$(".jw-button-container .jw-tooltip-forward").addClass("jw-open")}).mouseleave(function(){$(".jw-button-container .jw-tooltip-forward").removeClass("jw-open")}),0==$("#QualityText").length)&&(new MutationObserver(function(e){$(".jw-flag-user-inactive").length?$("#QualityText").hide():$("#QualityText").show()}).observe(document.querySelector(".jwplayer"),{attributes:!0}),$(".jw-media").prepend('<div id="QualityText" style="display:none; width:170px; height:30px; font: normal 14px arial; line-height:30px; text-align:right; color:#fff; background:#0000; position:absolute; top:30px; right:20px; z-index:5;"></div>'))}),a.on("levelsChanged",function(e,t){UpdateQualityText()}),a.on("levels",function(){1===a.getCurrentQuality()&&a.setCurrentQuality(0),updateQualityText()}),a.on("levelsChanged",function(e,t){updateQualityText()});var o=0;a.on("error",function(e){if(2<o)return!1;o++,setTimeout(function(){a.load(a.getPlaylist())},300)}),a.on("time",function(e){try{localStorage.getItem("11666-5fdde056fb0e9042e29c0a20-all")||localStorage.setItem("11666-5fdde056fb0e9042e29c0a20-all",a.getDuration()),localStorage.setItem("11666-5fdde056fb0e9042e29c0a20",Math.floor(e.position))}catch(e){}}),$(function(){$("body").on("click",".jw-icon-hd .jw-option",function(){0})}),console.clear()}$(".playSheilaBtn").css("border-radius","3px"),$(".playSheilaBtn").css("background","#fff"),$(".playSheilaBtn").css("color","#000"),$("#playSheila").css("background","#000"),$("#playSheila").css("background-image","none"),$("#playSheila").css("background-size","100% 100%"),$("#playSheila").css("display","block"),deb(),setInterval(function(){console.clear()},100)</script>
```

### **[HexCodec](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Sifreleme/HexCodec.py)**
```python
import re
from Kekik.Sifreleme import HexCodec

veri = r'''
jwSetup.sources=[{"default":true,"file":"\x68\x74\x74\x70\x73\x3a\x2f\x2f\x64\x32\x2e\x69\x6d\x61\x67\x65\x73\x70\x6f\x74\x2e\x62\x75\x7a\x7a\x2f\x66\x32\x2f\x4e\x74\x4f\x31\x4e\x51\x5a\x6a\x44\x51\x41\x6b\x78\x6c\x58\x45\x47\x33\x6c\x62\x66\x62\x30\x31\x79\x74\x70\x57\x66\x4e\x30\x66\x62\x66\x50\x58\x5a\x55\x31\x6a\x50\x77\x5a\x6d\x48\x71\x58\x41\x37\x6c\x6d\x6d\x4b\x67\x47\x59\x31\x66\x47\x42\x6d\x6c\x38\x68\x32\x7a\x33\x4f\x5a\x69\x4f\x63\x4c\x6b\x51\x70\x7a\x57\x78\x4b\x45\x4c\x57\x42\x63\x79\x4d\x74\x75\x55\x44\x57\x46\x4e\x6c\x69\x64\x70\x46\x46\x65\x6e\x65\x64\x66\x48\x30\x69\x74\x66\x59\x67\x38\x52\x47\x41\x6b\x38\x6c\x76\x72\x31","label":"0","type":"hls","preload":"none"}];var mu=getLocation(jwSetup.sources[0].file);
'''

escaped_hex  = re.findall(r'file":"(.*)","label', veri)[0]
print(HexCodec.decode(escaped_hex))
# https://d2.imagespot.buzz/f2/NtO1NQZjDQAkxlXEG3lbfb01ytpWfN0fbfPXZU1jPwZmHqXA7lmmKgGY1fGBml8h2z3OZiOcLkQpzWxKELWBcyMtuUDWFNlidpFFenedfH0itfYg8RGAk8lvr1
```

### **[NaysHash](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/Sifreleme/NaysHash.py)**
```python
from Kekik.Sifreleme import NaysHash

print(NaysHash().generate_xtoken(
    timestamp = 1695076755128,
    endpoint  = "/customer-citizen-info-v3",
    payload   = {
        "birthDay"              : 31,
        "birthMonth"            : 1,
        "birthYear"             : 1990,
        "citizenId"             : "11111111111",
        "customerName"          : "merhaba",
        "customerSurname"       : "dünya",
        "explicitConsentSigned" : True
    },
))
# EygcmEIe3aU0TWIubaQTuBwbrqpY7HFcNDajlSKCT5c=
```

### **[kekik_cache](https://github.com/keyiflerolsun/Kekik/blob/main/Kekik/cache.py)**
```python
import Kekik.cache as cache
cache.REDIS_HOST = "127.0.0.1"
cache.REDIS_PORT = 6379
cache.REDIS_DB   = 0
cache.REDIS_PASS = None
kekik_cache      = cache.kekik_cache

@kekik_cache(ttl=5)
def sync_func(x, y):
    time.sleep(1)
    return x + y

@kekik_cache(ttl=5)
async def async_func(x, y):
    await asyncio.sleep(1)
    return x * y
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