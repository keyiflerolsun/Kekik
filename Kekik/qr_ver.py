# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from qrcode import QRCode
from io import StringIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import VerticalBarsDrawer

def qr_ver(veri, png:bool=False, favicon:str=None, txt:bool=False) -> str:
    qr = QRCode(border=2)
    qr.add_data(veri)
    qr.make(fit=True)

    f = StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    str_qr = f.read()[:-1]

    if png:
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=VerticalBarsDrawer(), embeded_image_path=favicon)
        img.save('qr.png')

    if txt:
        with open("qr.txt", "w+", encoding="utf-8") as dosya:
            dosya.write(str_qr)

    return str_qr