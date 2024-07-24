# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io         import open

setup(
    # ? Genel Bilgiler
    name         = "Kekik",
    version      = "1.3.7",
    url          = "https://github.com/keyiflerolsun/Kekik",
    description  = "İşlerimizi kolaylaştıracak fonksiyonların el altında durduğu kütüphane..",
    keywords     = ["Kekik", "KekikAkademi", "keyiflerolsun"],

    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    license      = "GPLv3+",
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3"
    ],

    # ? Paket Bilgileri
    packages         = ["Kekik"],
    python_requires  = ">=3.10",
    install_requires = [
        "pip",
        "setuptools",
        "wheel",
        "pytz",
        "requests",
        "aiohttp",
        "httpx",
        "parsel",
        "cssselect",
        # "thispersondoesnotexist",
        "simplejson",
        "rich",
        "tabulate",
        # "tqdm",
        # "qrcode",
        # "pyfiglet",
        # "Pillow",
        # "notify-py",
        # "py3-validate-email"
    ],

    # ? PyPI Bilgileri
    long_description_content_type = "text/markdown",
    long_description              = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data          = True
)