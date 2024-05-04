# from TA import ta_instance

import json
import RSU
from Crypto.Cipher import PKCS1_OAEP
from fastapi import FastAPI
app = FastAPI()
import ast
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from fastapi import Request
import requests

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Protocol.SecretSharing import Shamir
import pickle

host='127.0.0.1'

from RSU import Rsu

rsu=Rsu(host,5551,0,1000)
rsu.id="2"
rsu.Ta_public_key=public_key=ECC.import_key(open('pubkey.pem').read())


@app.get("/register_table/")
async def Register_rsu():
    rsu_data={"host":str(rsu.host),"port":str(rsu.port),"x":str(rsu.x),"y":str(rsu.y),"id":rsu.id}
    rsu_data_json=json.dumps(rsu_data)
    response=requests.post('http://localhost:5530/register_rsu_table/',json=rsu_data_json)
  # print(response)

    

@app.post("/authenticate_vehicle/")
async def authenticate_vehicle(request:Request):
    data=await request.json()
    data=(eval(data))
    secret=eval(data["secret"])
    id=eval(data["id"])
    next_rsu_id=str((int(rsu.id)+1)%5)
    data_id={"id":next_rsu_id}
    data_id_json=json.dumps(data_id)
    response=requests.post('http://localhost:5530/get_port/',json=data_id_json)
    port=response.content.decode()
    response=requests.get(f'http://localhost:{port[1:-1]}/get_secret/')
    content=ast.literal_eval( json.loads(response.content))
    secret_other=[]
    id_other=content['id']
    for item in content['secret']:
        secret_other.append((id_other,eval(item[1])))
    # print(secret_other)
    signature,message_temp=secret.split(id)
    message=id+message_temp
    h = SHA256.new(message)
    rsu.Ta_public_key=ECC.import_key(open('pubkey.pem').read())
    verifier = DSS.new(rsu.Ta_public_key, 'fips-186-3')
    try:
        verifier.verify(h,signature)
      # print('not here')
      # print("The message is authentic.")
    
        # content=eval(content)
        # print(dict1)
        

        secret_shameer_self=rsu.secret_shameer
        key_comp=bytes()
      # print('here')
        for i in range(len(secret_shameer_self)):
            shares = []
            shares.append(secret_shameer_self[i])
            # secret_shameer_other[i][1]=eval(secret_shameer_other[i][1])
            shares.append(secret_other[i])
            # print(shares)
            key = Shamir.combine(shares)
            key_comp=key_comp+key
        key_comp=key_comp[:-8]
        # print(key_comp)
        # # print(key_comp.decode())
        # # key_comp=eval(key_comp)
        # print(message_temp)
        key_comp=b'-----BEGIN RSA PRIVATE KEY-----\n'+key_comp+b'\n-----END RSA PRIVATE KEY-----'

        # with open("secret.pem", "rb") as f:
        #     data = f.read()
        #   # print(data)
        #     mykey = RSA.import_key(data)
        mk=RSA.import_key(key_comp)
        # print(mykey)
        # print('\n\n\n')
        # print(key_comp)
        cipher=PKCS1_OAEP.new(mk)
        mes=cipher.decrypt(message_temp)
        if mes==id:
            return json.dumps({"Authenticated":True})
        # print(secret.split(id))
        



    except Exception as e:
        print(e)
        print("The message is not authentic.")
    



    
@app.get("/get_secret_shameer/")
async def get_secret_shameer():
    rsu_data={"host":str(rsu.host),"port":str(rsu.port),"x":str(rsu.x),"y":str(rsu.y),"id":rsu.id}
    rsu_data_json=json.dumps(rsu_data)
    response=requests.post('http://localhost:5549/register/',json=rsu_data_json)

    data=ast.literal_eval(json.loads(response.content))
    shameer_secret=[]
    for item in data["secret"]:
        shameer_secret.append((1,eval(item[1])))
    rsu.secret_shameer=shameer_secret


@app.get("/get_secret/")
async def get_secret():
    # rsu_data={"host":str(rsu2.host),"port":str(rsu2.port),"x":str(rsu2.x),"y":str(rsu2.y),"id":rsu2.id}
    # rsu_data_json=json.dumps(rsu_data)
    # response=requests.post('http://localhost:5530/register_rsu_table/',json=rsu_data_json)
    # print(response) 
    secret_data={}
    for i in range(len(rsu.secret_shameer)):
        # print(rsu2.secret_shameer[i])
        rsu.secret_shameer[i]=[2,str(rsu.secret_shameer[i][1])]
    secret_data={"secret":rsu.secret_shameer,"id":2}

    return json.dumps(secret_data)
