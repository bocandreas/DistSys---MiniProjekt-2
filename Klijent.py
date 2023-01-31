"""
Klijent
Generira se lista od 10 000 klijenata. (client ids) Ucitava dataset i uzima
stupac koji sadrzi python kod. Dataset se podijeli ravnomjerno klijentima. (dict
klijenata i njihov python kod) Klijenti salju zahtjeve za obradu koda. Ispisuje u
konzolu za svakog klijenta prosjecan broj slova koji sadrzi sav njihov python kod.
"""

from aiohttp import web
import json
import requests

routes = web.RouteTableDef()
@routes.get("")

async def client_ids(request):
        #Kreiranje 10k klijenata
        clients_ids = list(range(10000))

        #Učitavanje FakeDataset-a
        lista = []
        with open ("file-000000000040.json", "r") as f:
                for jsonObj in f:
                        fileDict = json.loads(jsonObj)
                        lista.append(fileDict)
                half_dataset = lista[:50000] #Pola dataseta
                #print(prvih10k)
                pythonkod = {item["content"] for item in half_dataset}
                #print(pythonkod) 

                # Ravnomjerna podjela koda/Kreiranje liste dictionarija
                client_codes = []
                for client_id in clients_ids:
                        client_code = {"client_id": client_id, "code": []}
                        client_codes.append(client_code)
                for i, code in enumerate(pythonkod):
                        client_idx = i % len(clients_ids)
                        client_codes[client_idx]["code"].append(code)
                
 
                # Slanje zahtjeva za obradu koda
                headers = {"Content-Type": "application/json"}

                response = requests.post("http://127.0.0.1:8081/client_content", headers=headers, json=client_codes)
                #print(response.status_code)

                # Ispis svakog klijenta i prosječan broj slova
                for client_code in client_codes:
                        code = client_code["code"]
                        code_length = len("".join(code))
                        avg_length = code_length / len("".join(code).split())
                        print("Klijent: ", client_code["client_id"], " prosječan broj slova: ", avg_length)

                 
        return web.json_response({"status":"OK"}, status=200)
                
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, host="127.0.0.1", port=8080)
