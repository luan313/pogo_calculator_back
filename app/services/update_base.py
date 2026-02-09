import requests
import json
from ..config import(
    URL_GREAT,
    URL_ULTRA,
    URL_MASTER
)

response_great = requests.get(URL_GREAT).json()
with open('C:\\Users\\luanf\\GitHub\\pogocalculator\\backend\\data\\base_great.json', 'w', encoding='utf-8') as f:
    json.dump(response_great, f, ensure_ascii=False, indent=4)

response_ultra = requests.get(URL_ULTRA).json()
with open('C:\\Users\\luanf\\GitHub\\pogocalculator\\backend\\data\\base_ultra.json', 'w', encoding='utf-8') as f:
    json.dump(response_ultra, f, ensure_ascii=False, indent=4)

response_master = requests.get(URL_MASTER).json()
with open('C:\\Users\\luanf\\GitHub\\pogocalculator\\backend\\data\\base_master.json', 'w', encoding='utf-8') as f:
    json.dump(response_master, f, ensure_ascii=False, indent=4)