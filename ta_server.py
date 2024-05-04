import TA
import TABLE
import json

from fastapi.responses import FileResponse
from fastapi import FastAPI
app = FastAPI()

from pydantic import BaseModel

from fastapi import Request
import pickle

ta_instance=TA.TA()  

tasks = []


@app.get("/tasks/")
def get_tasks():
	return '{"status":"running"}'
	# return tasks



@app.post("/register/")
async def Register_rsu(request:Request):
    data=await request.json()
    
    data=json.loads(data)

    secrets=ta_instance.register_rsu(data)
    
    for item in secrets:
         item[1]=str(item[1])
    secret_json={"secret":secrets}
    # print(len(secrets))
    # secret_json={}
    # i=0
    # for secret in secrets:
    #      secret_json[str(i)]=secret
    #      i=i+1
    # # print(secret_json)

    # for key,value in secret_json.items():
    #      for val in value:
    #         #   print(val[1])
    #           val[1]=str(val[1])
    # print(secret_json)

    return json.dumps(secret_json)
    # return secrets

@app.post("/register_vehicle/")
async def Register_vehicle(request:Request):
    data=await request.json()   
    data=json.loads(data)
    print(data)
    value=ta_instance.register_vehicle(data)
    print(value)
    file1=open('ta_server_file/signature.pkl','wb')
    pickle.dump(value,file1)
    file1.close()
    return FileResponse('ta_server_file/signature.pkl')
    # return signature_public_key
    
    
    
    # print(await request.json())