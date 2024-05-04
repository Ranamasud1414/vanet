# from TA import ta_instance
import TABLE
import json
import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from VEHICLE import Vehicle
import pickle
from fastapi import FastAPI,HTTPException
app = FastAPI()
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse,RedirectResponse
from pydantic import BaseModel
from starlette.responses import HTMLResponse

from fastapi import Request


host='127.0.0.1'
vehicle=Vehicle(host,5540,0,0,'') 

@app.get("/vehicle/")
async def Register_vehicle():
    vehicle_data={"id":str(vehicle.id),"host":vehicle.host,"port":vehicle.port}
    vehicle_data_json=json.dumps(vehicle_data)
    # data=await request.json()
    # requests.post(host,)
    response=requests.post('http://localhost:5549/register_vehicle/',json=vehicle_data_json)
    
    m=pickle.loads(response.content)
    signature,message=m.split(vehicle.id)
    message=vehicle.id+message
    key = ECC.import_key(open('pubkey.pem').read())
    h = SHA256.new(message)
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h,signature)
        vehicle.credentials=str(m)
      # print("The message is authentic.")
    except ValueError:
      # print("The message is not authentic.")
        vehicle.credentials=str(m)
    # return signature_public_key
    
    
    
    # print(await request.json())
# @app.get("/connect/")
# async def Connect():
#     data={"secret":vehicle.credentials,"id":str(vehicle.id)}
#     response=requests.post('http://localhost:5550/authenticate_vehicle/',json=json.dumps(data))
#     print(response.content)
    




@app.get("/connect/")
async def Connect():
    data = {"secret": vehicle.credentials, "id": str(vehicle.id)}
    response = requests.post('http://localhost:5550/authenticate_vehicle/', json=json.dumps(data))
    print(response.content)
    if response.content == b'"{\\"Authenticated\\": true}"':
        print("Authenticated successfully")
        return RedirectResponse(url="/success")
    else:
        print("Authentication failed")
        return "Authentication failed"

@app.get("/success", response_class=HTMLResponse)
async def success():
    return FileResponse("templates/success.html")