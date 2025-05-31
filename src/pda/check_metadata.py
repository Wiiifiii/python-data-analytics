import requests

PXWEB_URL = "https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/synt/statfin_synt_pxt_12dt.px"
query_payload_minimal = {
    "query": [
        {
            "code": "Vuosi",
            "selection": {
                "filter": "item",
                "values": ["2022"]
            }
        },
        {
            "code": "Tieto",
            "selection": {
                "filter": "item",
                "values": ["tfr"]
            }
        }
    ],
    "response": {
        "format": "json-stat2"
    }
}


resp = requests.post(PXWEB_URL, json=query_payload_minimal, timeout=15)
resp.raise_for_status()
data = resp.json()
print("Got JSON-stat2 dataset:", list(data.keys()))
