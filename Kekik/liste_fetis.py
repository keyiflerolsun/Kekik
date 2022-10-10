# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

def n_adete_bol(liste:list, adet:int=2) -> list[list]:
    return [liste[say::adet] for say in range(adet)]

def n_er_hale_getir(liste:list, adet:int=2) -> list[list]:
    return [liste[i : i + adet] for i in range(0, len(liste), adet)]