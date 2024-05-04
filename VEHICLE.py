import math
# import TA
from Crypto.Random import get_random_bytes
import random 
import string

def calculate_distance(point1,point2):
    xsqrd=math.pow((point2[0]-point1[0]),2)
    ysqrd=math.pow((point2[1]-point1[1]),2)
    dist=math.sqrt(xsqrd,ysqrd)
    return dist

class Vehicle:
    key_range=string.ascii_letters+string.digits
    def __init__(self,host,port,x,y,table):
        
        self.id=bytes(''.join(random.choices(Vehicle.key_range,k=8)).encode('utf_8'))
        self.matrix={}
        self.host=host
        self.port=port
        self.x=x
        self.y=y
        self.connected=-1
        self.list_message=[]
        # for key,value in table.items():
        #     self.matrix[key]=[value[2],value[3]]
        self.credentials='not registered yet'

    def move_x(self,dist=1):
        self.x=self.x+dist
    
    def move_y(self,dist=1):
        self.y=self.y+dist

    def update_matrix(self,key,table):
        self.matrix[key]=[table[key][2],table[key][2]]

    def replace_matrix(self,table):
        for key,value in table.items():
            self.matrix[key]=[value[2],value[3]]




    #Equivalent to vehicles sensor detecting nearest sensor
    def poll_rsu(self,table):
        point1=[self.x,self.y]
        min_distance=[-1,math.inf]
        for key,values in table.items():
            point2=[values[2],values[3]]
            dist=calculate_distance(point1,point2)
            if dist<min_distance[1]:
                min_distance[1]=dist
                min_distance[0]=key

        return min_distance
    
    def connect(self,host,port,rsu):
        #connect with a rsu on given host and port
        pass

    def disconnect(self,host,port,rsu):
        #disconnect with a rsu on given host and port
        pass
    