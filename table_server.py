from TABLE import table_instance
import json

from fastapi.responses import FileResponse
from fastapi import FastAPI
app = FastAPI()

from pydantic import BaseModel

from fastapi import Request
import pickle

#port=5530

tasks = []

@app.post("/register_rsu_table/")
async def Register_rsu_table(request:Request):
    data=await request.json()
    print(data)
    data=json.loads(data)
    table=table_instance.add_rsu_routing_table(data)
    print(table_instance.table)
    # return secrets

@app.post("/get_port/")
async def get_port(request:Request):
    data=await request.json()
    print(data)
    data=json.loads(data)
    port=table_instance.get_port(data["id"])
    print(port)
    return port

