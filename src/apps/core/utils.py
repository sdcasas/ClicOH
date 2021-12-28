import requests
from typing import Optional

from django.core.cache import cache
from django.conf import settings


def convert_str_to_float(value: str) -> Optional[float]:
    return float(value.replace(",", ".").strip()) if value else None


def get_dolar_blue() -> Optional[float]:
    result = cache.get("dolar_blue", None)
    if result:
        return result
    try:
        #print(f"CONSULTANDO A {settings.API_DOLAR_URL} =====================================")
        response = requests.get(url=settings.API_DOLAR_URL, timeout=10)
    except requests.exceptions.RequestException as e:
        return result

    if response.status_code == 200:
        for row in response.json():
            try:
                if row["casa"]["nombre"] == "Dolar Blue":
                    result = convert_str_to_float(row["casa"]["venta"])
                    cache.set('dolar_blue', result, 60*60)
            except Exception as e:
                print(e)
    return result