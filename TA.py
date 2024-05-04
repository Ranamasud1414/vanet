from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify
import string
import random
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.PublicKey import RSA




class TA:
    id=-1
    rsu_key_id=0
    def __init__(self):
        key = ECC.generate(curve='p256')
        encryption_key=RSA.generate(1024)
        self.private_key=encryption_key
        with open('secret.pem','wb') as f:
            f.write(encryption_key.export_key())
        public_key=encryption_key.publickey()
        self.public_key=public_key
        TA.id=TA.id+1
        self.id=TA.id
        self.signature_private_key=key
        with open("pubKey.pem", "wt") as f:
            data = key.public_key().export_key(format='PEM')
            f.write(data)
      # print(key.public_key().export_key(format='PEM'))
        self.signature_public_key=key.public_key()
        # self.private_key=encryption_key
        self.table=[]
        self.vehicle_table=[]
        self.rsu_secret=[]
        

    
    def register_vehicle(self,Vehicle):
        # key_range=string.ascii_letters+string.digits
        # unecrypted_key=bytes(''.join(random.choices(key_range,8)))

        unencrypted_key=eval(Vehicle['id'])
        # print(type(unencrypted_key))
        # print(self.public_key)
        cipher=PKCS1_OAEP.new(self.public_key)
        
        encrypted_key=cipher.encrypt(unencrypted_key)
        message=unencrypted_key+encrypted_key
      # print('message',message)
        h = SHA256.new(message)
        # print('hashed value',h)
        signer = DSS.new(self.signature_private_key, 'fips-186-3')
        signature = signer.sign(h)
      # print('signed value',signature+b' '+message)
        signature=signature+message
        return signature

    def register_rsu(self,value):
        
        rsu_data={'id':value['id'],'host':value['host'],'port':value['port']}
        self.table.append(rsu_data)
        # print(self.signature_public_key)
        if TA.rsu_key_id==0:
            self.rsu_secret=self.generate_shamir()
        secret= self.rsu_secret[self.rsu_key_id] 
      # print('id now == ',self.rsu_key_id)
        TA.rsu_key_id=(TA.rsu_key_id+1)%5
        return secret

           

            # signature_public_key= self.signature_public_key
        
            #use shameer's algorithm to generate a secret for list of nrsus and distribute them among them
    def generate_shamir(self):
        private_key=self.private_key
        private_key=private_key.export_key()[32:-30]

        secret=[]

        length=len(private_key)//16
        for i in range(length):
            start=16*i
            end=16*(i+1)
            # print((start,end))
            secret.append(private_key[start:end])
        # print(16*length)
        secret.append(private_key[16*length:])


        # str1=b''.join(secret)

        # print(str1==private_key)

        padding=get_random_bytes(8)
        secret[-1]=secret[-1]+padding
        # print(len(str1))

        parts=[]

        for key in secret:
            # print(key)
            shares = Shamir.split(2, 5, key)
            temp=[]
            # print(type(key),'----->')
            for idx, share in shares:
                # print(share)
                temp.append([idx,share])

                # print ("Index #%d: %s" % (idx, hexlify(share)))
            parts.append(temp)


        secret_by_rsu=[[],[],[],[],[]]
        for part in parts:
            #print(part)
            for i in range(0,5):
                secret_by_rsu[i].append(part[i])
      # print(secret_by_rsu[0]==secret_by_rsu[1])
        return secret_by_rsu

  


# print(len(parts))

# for item in parts:
#   # print(item)



# idx=[parts[0][0][0],parts[0][1][0]]
# share=[parts[0][0][1],parts[0][1][1]]
# key_comp=bytes()
# for i in range(len(parts)):
#     shares = []
#     shares.append((parts[i][0][0],parts[i][0][1]))
#     shares.append((parts[i][1][0],parts[i][1][1]))
#     key = Shamir.combine(shares)
#     # print(type(key))
#     # print(key)
#     key_comp=key_comp+key
# print(key_comp[:-8]==private_key)


# key = Shamir.combine(shares)

