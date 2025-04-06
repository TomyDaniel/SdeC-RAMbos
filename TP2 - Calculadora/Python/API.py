import requests

def obtener_gini(pais='ARG'):
    url = f"https://api.worldbank.org/v2/country/{pais}/indicator/SI.POV.GINI?format=json&per_page=100"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error al obtener los datos.")
        return None

    data = response.json()

    # Buscamos el dato más reciente que tenga valor
    for entry in data[1]:
        if entry['value'] is not None:
            year = entry['date']
            gini = entry['value']
            print(f"Gini de {pais} en {year}: {gini}")
            return gini

    print("No se encontraron datos válidos.")
    return None
