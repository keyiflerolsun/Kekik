# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from speech_recognition import Recognizer, Microphone
from gtts import gTTS
from os import system, remove

def ses2yazi() -> str:
    dinleyici = Recognizer()
    with Microphone() as source:
        dinleyici.adjust_for_ambient_noise(source)
        veri = dinleyici.record(source, duration=5)
        yazi = dinleyici.recognize_google(veri, language="tr")
    return yazi

def yazi2ses(metin:str, mp3_adi:str) -> str:
    tts = gTTS(metin.strip(), lang="tr", slow=True)
    tts.save(f"{mp3_adi}.mp3")
    return f"{mp3_adi}.mp3"

def cevir(girdi_dosya:str, cikti_dosya:str) -> str:
    system(f'ffmpeg -hide_banner -loglevel error -y -i {girdi_dosya} -af "asetrate=44100*0.9, aresample=44100, atempo=1/0.9" {cikti_dosya}')
    remove(girdi_dosya)
    return cikti_dosya

def inceses(metin:str, cikti_adi:str) -> str:
    _gecici = yazi2ses(metin, "gecici")
    return cevir(_gecici, f"{cikti_adi}.mp3")

# print(inceses("Selam Kanka Naber bakalım?", "selam"))
