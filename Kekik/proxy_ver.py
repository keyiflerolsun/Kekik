# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from typing  import Literal
from Kekik   import dosya2set
from aiohttp import BasicAuth
from random  import shuffle, choice

def proxy_ver(proxi_txt:str, tur=Literal["requests", "aiohttp", "selenium", "httpx"]) -> None | dict[str, str] | ((str and BasicAuth) or (str and None)) | str:

    proxiler = list(dosya2set(proxi_txt)) if dosya2set(proxi_txt) else None

    if not proxiler:
        return None

    shuffle(proxiler)
    secim = choice(proxiler)

    if tur == "selenium":
        return secim

    proxi_part = secim.split(":")

    match len(proxi_part):
        case 4:
            p_ip, p_port, p_user, p_pass = proxi_part
            proxi_auth = BasicAuth(p_user, p_pass, "utf-8")

            requests_proxi = {
                "http"   : f"http://{p_user}:{p_pass}@{p_ip}:{p_port}",
                "https"  : f"http://{p_user}:{p_pass}@{p_ip}:{p_port}",
                # "socks5" : f"socks5://{p_user}:{p_pass}@{p_ip}:{p_port}",
            }

            httpx_proxi = {
                "http://"  : f"http://{p_user}:{p_pass}@{p_ip}:{p_port}",
                "https://" : f"http://{p_user}:{p_pass}@{p_ip}:{p_port}"
            }
        case 2:
            p_ip, p_port = proxi_part
            proxi_auth   = None

            requests_proxi = {
                "http"   : f"http://{p_ip}:{p_port}",
                "https"  : f"http://{p_ip}:{p_port}",
                # "socks5" : f"socks5://{p_ip}:{p_port}",
            }

            httpx_proxi = {
                "http://"  : f"http://{p_ip}:{p_port}",
                "https://" : f"http://{p_ip}:{p_port}"
            }
        case _:
            return None

    match tur:
        case "aiohttp":
            return f"http://{p_ip}:{p_port}", proxi_auth
        case "requests":
            return requests_proxi
        case "httpx":
            return httpx_proxi