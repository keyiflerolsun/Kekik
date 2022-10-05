# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io         import open

setup(
    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    packages     = ["Kekik"],

    name         = "Kekik",
    version      = "1.0.8",
    url          = "https://github.com/keyiflerolsun/Kekik",
    description  = "İşlerimizi kolaylaştıracak fonksiyonların el altında durduğu kütüphane..",
    keywords     = ["Kekik", "KekikAkademi", "keyiflerolsun"],

    long_description_content_type = "text/markdown",
    long_description              = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data          = True,

    license     = "GPLv3+",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3"
    ],

    python_requires  = ">=3.10",
    install_requires = [
        "setuptools",
        "wheel",
        "pytz",
        "requests",
        "aiohttp",
        "thispersondoesnotexist",
        "simplejson",
        "rich",
        "tabulate",
        "tqdm",
        "qrcode",
        "pyfiglet",
        "Pillow",
        "notify-py",
        "py3-validate-email"
    ]
)