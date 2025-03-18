import requests


def get_informations_via_inn(inn: str):
    url = f"https://gnk-api.didox.uz/api/v1/utils/info/{inn}"
    response = requests.get(url)
    if not response.status_code == 200:
        return None
    if not response.json()["tin"]:
        return None
    return response.json()