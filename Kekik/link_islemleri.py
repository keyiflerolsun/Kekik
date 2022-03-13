# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import re
from typing import List

def link_ayikla(link:str) -> List[str]:
    """ Metindeki linkleri liste halinde return eder """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    url   = re.findall(regex, link)

    return [x[0] for x in url]

def youtube_link_mi(link:str) -> bool:
    return bool(re.match(r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", link))