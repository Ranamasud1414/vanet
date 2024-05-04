import socket
import threading

class Rsu:
    id=-1
    def __init__(self,host,ports,x,y):
        Rsu.id=Rsu.id+1
        self.id=str(Rsu.id)
        self.host=host
        self.port=ports
        self.x=x
        self.y=y
        self.clients=[]
        self.list_message=[]
        self.Ta_public_key='get if after instantiation of each classes neccessary'
        self.secret_shameer=[]#'get it through registering a bunch of rsus list of 52 secret parts'
        self.next_fwd='trusted RSU forward direction'
        self.next_bwd='trusted rsu backward direction'


    def authenticate_vehicle(self):
        #authenticate vehicle using shameer algorithm and public key of Tsu
        pass

    def authenticate_vehicle_frm__rsu(self,vehicle,rsu):
        # if vehicle is authenticated by some trusted rsu then don't reauthenticate again
        pass

    def connect(self,port,host,vehicle):
        #connect with a vehicle on a given port and host
        pass

    def disconnect(self,port,host,vehicle):
        #disconnect with a vehicle
        pass

    

#Authentication  

#Connect and disconnect
        

        
