# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

# * pip3 install -U PyAudio SpeechRecognition beepy gTTS playsound

from Kekik.cli          import konsol
from speech_recognition import Recognizer, Microphone
from beepy              import beep
from gtts               import gTTS
from playsound          import playsound
from os                 import system, remove

def ses2yazi(n_saniye_dinle:int | None) -> str:
    dinleyici = Recognizer()

    import os, sys, contextlib

    @contextlib.contextmanager
    def ignore_stderr():
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        sys.stderr.flush()
        os.dup2(devnull, 2)
        os.close(devnull)
        try:
            yield
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)

    with ignore_stderr() as _, Microphone() as source:
        dinleyici.adjust_for_ambient_noise(source)
        beep()
        konsol.log("[purple][~] Mikrofon Dinleniyor..")
        if n_saniye_dinle:
            veri = dinleyici.record(source, duration=n_saniye_dinle)
        else:
            veri = dinleyici.listen(source)
        konsol.log("[magenta][~] Ses Erişimi Tamamlandı..")
        yazi = dinleyici.recognize_google(veri, language="tr")

    return yazi

def yazi2ses(metin:str, mp3_adi:str) -> str:
    tts = gTTS(metin.strip(), lang="tr", slow=False)
    tts.save(f"{mp3_adi}.mp3")
    return f"{mp3_adi}.mp3"

def cevir(girdi_dosya:str, cikti_dosya:str) -> str:
    system(f'ffmpeg -hide_banner -loglevel error -y -i {girdi_dosya} -af "asetrate=44100*0.9, aresample=44100, atempo=1/1.15" {cikti_dosya}')
    remove(girdi_dosya)
    return cikti_dosya

def inceses(metin:str, cikti_adi:str) -> str:
    _gecici = yazi2ses(metin, "gecici")
    return cevir(_gecici, f"{cikti_adi}.mp3")


# ne_dedim = ses2yazi()
# print(ne_dedim)
# playsound(yazi2ses(ne_dedim, "dinlenen_ses"))
# playsound(inceses(ne_dedim, "dinlenen_ses"))