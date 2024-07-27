# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli import konsol
from httpx     import Client, HTTPError

class Domain2IP:
    def __init__(self, domain: str):
        self.oturum = Client(headers={"accept": "application/dns-json"})
        self.domain = domain

        self.CORS_PROXY_URL = "https://ts-cors-proxy.eralde.workers.dev"
        self.CF_DOH_URL     = "https://cloudflare-dns.com/dns-query"

    def _dns_sorgula(self, domain: str, sorgu_turu: str):
        if not domain:
            domain = self.domain

        try:
            url = f"{self.CORS_PROXY_URL}/{self.CF_DOH_URL}?name={domain}&type={sorgu_turu}"
            yanit = self.oturum.get(url)
            yanit.raise_for_status()

            return yanit.json().get("Answer" if sorgu_turu == "A" else "Authority", [])

        except HTTPError as http_hatasi:
            konsol.log(f"[red][!] HTTP hatası meydana geldi: {http_hatasi}")

        except Exception as diger_hata:
            konsol.log(f"[red][!] Başka bir hata meydana geldi: {diger_hata}")

        return []

    def a_kayitlari(self, domain: str = None):
        return self._dns_sorgula(domain, "A")

    def cname_kayitlari(self, domain: str = None):
        return self._dns_sorgula(domain, "CNAME")

    def tum_ip_adresleri(self):
        a_kayitlari  = self.a_kayitlari()
        ip_adresleri = [kayit["data"] for kayit in a_kayitlari]

        cname_kayitlari = self.cname_kayitlari()
        for cname_kayit in cname_kayitlari:
            cname_domain = cname_kayit["data"]
            cname_ipler  = self.a_kayitlari(cname_domain)
            ip_adresleri.extend([kayit["data"] for kayit in cname_ipler])

        return sorted(list(set(ip_adresleri)))

    def ip_to_binary(self, ip_str):
        return "".join([f"{int(octet):08b}" for octet in ip_str.split(".")])

    def binary_to_ip(self, binary_str):
        octets = [
            str(int(binary_str[i : i + 8], 2)) for i in range(0, len(binary_str), 8)
        ]

        return ".".join(octets)

    def get_mask_binary(self, ones_length):
        return "".join(["1" if i < ones_length else "0" for i in range(32)])

    def longest_common_prefix(self, a, b):
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1

        return i

    def grubu_isle(self, grup):
        if len(grup) == 1:
            return None
            # return {
            #     "subnet" : f"{self.binary_to_ip(grup[0])}/32",
            #     "ipler"  : [self.binary_to_ip(grup[0])],
            # }

        lcp       = self.longest_common_prefix(grup[0], grup[-1])
        subnet_ip = self.binary_to_ip(grup[0][:lcp] + "0" * (32 - lcp))

        return {
            "subnet" : f"{subnet_ip}/{lcp}",
            "ipler"  : sorted([self.binary_to_ip(ip) for ip in grup]),
        }

    def subnetlere_ayir(self, ip_listesi, min_ortak_bit=24):
        if not ip_listesi:
            konsol.log("[red][!] Subnetlere ayırmak için IP yok.")
            return []

        binary_listesi = sorted(map(self.ip_to_binary, ip_listesi))
        if not binary_listesi:
            konsol.log("[red][!] İşlenecek binary IP verisi yok.")
            return []

        gruplar     = []
        mevcut_grup = [binary_listesi[0]]
        for binary_ip in binary_listesi[1:]:
            if self.longest_common_prefix(mevcut_grup[-1], binary_ip) < min_ortak_bit:
                gruplar.append(mevcut_grup)
                mevcut_grup = [binary_ip]
            else:
                mevcut_grup.append(binary_ip)

        gruplar.append(mevcut_grup)

        return [self.grubu_isle(grup) for grup in gruplar if self.grubu_isle(grup)]

    @property
    def bilgi(self):
        tum_ipler = self.tum_ip_adresleri()
        subnetler = [subnet["subnet"] for subnet in self.subnetlere_ayir(tum_ipler) if subnet]

        return {
            "domain"    : self.domain,
            "ipler"     : tum_ipler or None,
            "subnetler" : subnetler or None,
        }