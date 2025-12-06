# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

"""Serileştirme ve Cache Key Yardımcıları"""

from __future__ import annotations
import json
import pickle
from hashlib import md5
from inspect import signature
from typing import Any, Callable

# -----------------------------------------------------
# Serileştirme Sabitleri
# -----------------------------------------------------
_JSON_MARKER   = b'\x01'
_PICKLE_MARKER = b'\x02'


# -----------------------------------------------------
# Serileştirme Fonksiyonları
# -----------------------------------------------------
def is_json_serializable(value: Any) -> bool:
    """Verinin JSON'a serileştirilebilir olup olmadığını kontrol eder."""
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False


def serialize(value: Any) -> bytes:
    """
    Veriyi cache için serialize eder.
    
    Format:
        - JSON:   0x01 + json_bytes
        - Pickle: 0x02 + pickle_bytes
    """
    if is_json_serializable(value):
        json_bytes = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return _JSON_MARKER + json_bytes

    return _PICKLE_MARKER + pickle.dumps(value)


def deserialize(data: bytes) -> Any:
    """Cache'ten okunan veriyi deserialize eder."""
    if not isinstance(data, bytes) or len(data) == 0:
        return pickle.loads(data)

    marker  = data[:1]
    payload = data[1:]

    if marker == _JSON_MARKER:
        return json.loads(payload.decode("utf-8"))

    if marker == _PICKLE_MARKER:
        return pickle.loads(payload)

    # Eski format uyumluluğu
    return pickle.loads(data)


# -----------------------------------------------------
# Cache Key Oluşturma
# -----------------------------------------------------
def normalize_value(value: Any) -> Any:
    """
    Cache key için değeri normalize eder.
    Kompleks objeleri basit tiplere dönüştürür.
    """
    # Primitif tipler
    if isinstance(value, (int, float, str, bool, type(None))):
        return value

    # Dict: Anahtarları sırala
    if isinstance(value, dict):
        return {k: normalize_value(v) for k, v in sorted(value.items())}

    # List/Tuple: Elemanları normalize et
    if isinstance(value, (list, tuple)):
        return [normalize_value(item) for item in value]

    # Kompleks objeler için string temsil
    try:
        str_repr = str(value)
        if len(str_repr) < 100 and not str_repr.startswith("<"):
            return str_repr
    except Exception:
        pass

    return value.__class__.__name__


def _filter_self_from_args(func: Callable, args: tuple) -> tuple:
    """
    Class method'lardaki self/cls parametresini args'tan çıkarır.
    """
    try:
        params = list(signature(func).parameters.keys())
        if params and params[0] in ("self", "cls") and args:
            return args[1:]
    except (ValueError, TypeError):
        pass
    return args


def make_cache_key(func: Callable, args: tuple, kwargs: dict) -> str:
    """
    Fonksiyon ve parametrelerden benzersiz cache key oluşturur.
    
    Format: module:class:method:[args]:[kwargs]
    """
    # Base key: module:qualname
    base_key = f"{func.__module__}.{func.__qualname__}"
    base_key = ":".join(base_key.split("."))

    # self/cls parametresini hariç tut
    filtered_args = _filter_self_from_args(func, args)

    # Args ekle
    if filtered_args:
        norm_args = [normalize_value(arg) for arg in filtered_args]
        base_key += f":{norm_args}"

    # Kwargs ekle
    if kwargs:
        norm_kwargs = {k: normalize_value(v) for k, v in kwargs.items()}
        base_key += f":{sorted(norm_kwargs.items())}"

    return base_key
