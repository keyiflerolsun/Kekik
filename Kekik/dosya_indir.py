# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from typing import Optional
from tqdm import tqdm
import requests
from urllib.parse import unquote

def indirilebilir_mi(url:str) -> bool:
    istek  = requests.head(url, allow_redirects=True)
    header = istek.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def dosya_indir(url:str, dosya_adi:str=None) -> Optional[str]:
    kontrol = indirilebilir_mi(url)
    if not kontrol:
        print(f"HATA!, İndirilebilir Değil! » {url}")
        return None

    if not dosya_adi:
        dosya_adi = unquote(url.split("/")[-1])
    else:
        if "." not in dosya_adi:
            uzanti = unquote(url.split("/")[-1]).split(".")[-1]
            dosya_adi = f"{dosya_adi}.{uzanti}"

    istek = requests.get(url, stream=True)
    dosya_boyutu = int(istek.headers.get('content-length', 0))

    bar_format   = '{l_bar} [{rate_fmt}] | {bar}| [{n_fmt}B / {total_fmt}B] » [{elapsed} / {remaining}]'
    progress_bar = tqdm(desc=dosya_adi, total=dosya_boyutu, unit='B', unit_scale=True, bar_format=bar_format)
    with open(dosya_adi, 'wb') as dosya:
        for veri in istek.iter_content(1024): # 1KB
            progress_bar.update(len(veri))
            dosya.write(veri)
    progress_bar.close()

    if dosya_boyutu != 0 and progress_bar.n != dosya_boyutu:
        print(f"HATA!, Bişeyler Yanlış Gitti! » {dosya_adi}")
        return None

    return dosya_adi