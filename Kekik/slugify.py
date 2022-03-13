# https://github.com/django/django/blob/main/django/utils/text.py#L386-#L399

import re, unicodedata

def slugify(deger:str, unicode_izin=False) -> str:
    """
    'unicode_izin' False ise ASCII'ye dönüştürür.
    Boşlukları veya tekrarlanan kısa çizgileri tek tirelere dönüştürür.
    Alfasayısal, alt çizgi veya kısa çizgi olmayan karakterleri kaldırıp Küçük harfe dönüştür.
    Ayrıca baştaki ve sondaki beyaz boşlukları, tireleri ve alt çizgileri de çıkarır.
    """
    if unicode_izin:
        deger = unicodedata.normalize('NFKC', deger)
    else:
        deger = unicodedata.normalize('NFKD', deger).encode('ascii', 'ignore').decode('ascii')
    deger = re.sub(r'[^\w\s-]', '', deger.lower())
    return re.sub(r'[-\s]+', '-', deger).strip('-_')