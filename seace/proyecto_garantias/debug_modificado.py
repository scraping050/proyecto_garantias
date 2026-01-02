import requests
import json

url = "http://localhost:5000/api/reportes/generar"

payload = {
    "tipo": "personalizado",
    "filtros": {
        "origen_tipo": "MODIFICADO"
    }
}

headers = {
    'Content-Type': 'application/json'
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
