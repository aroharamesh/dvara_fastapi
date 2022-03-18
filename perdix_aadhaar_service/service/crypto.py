from commons import env
import base64
from Crypto import Random
from Crypto.Cipher import AES, DES3
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence

pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

def encrypt_req_data_block(req_data: str):
    keyStr = env['app-mantra-server']['secret-key']
    secret_cipher = DES3.new(keyStr, DES3.MODE_CBC)
    enc = base64.b64encode(secret_cipher.encrypt(bytes(pad(req_data), 'utf-8'))).decode("utf-8").strip()
    print(enc)
    return enc

def encrypt(req_xml: str):
    with open(env['certificate']['public-key']) as f1:
        pem = f1.read()
        lines = pem.replace(" ",'').split()
        der = base64.b64decode(''.join(lines[1:-1]))
        cert = DerSequence()
        cert.decode(der)
        tbs_cert = DerSequence()
        tbs_cert.decode(cert[0])
        subject_public_key_info = tbs_cert[6]
        public_key = RSA.importKey(subject_public_key_info)
        public_cipher = PKCS1_v1_5.new(public_key)

        # Step 1: create random secret key
        random = Random.new().read(AES.block_size)
        encrypted_key = base64.b64encode(public_cipher.encrypt(random))

        # Step 2: iv + encrypt data
        iv = Random.new().read(AES.block_size)
        data_cypher = AES.new(random, AES.MODE_CBC, iv)
        encrypted_data = base64.b64encode(iv + data_cypher.encrypt(bytes(pad(req_xml), 'utf-8')))

        return (encrypted_key.strip(), encrypted_data.strip(), base64.b64encode(iv).strip())

def decrypt(encrypted_key, encrypted_data):
    with open(env['certificate']['private-key']) as f1:
        key = f1.read()
        lines = key.replace(" ",'').split()
        der = base64.b64decode(''.join(lines[1:-1]))
        private_key = RSA.importKey(der)
        private_cipher = PKCS1_v1_5.new(private_key)
        random = private_cipher.decrypt(base64.b64decode(encrypted_key), 'Failure')
        data_cypher = AES.new(random, AES.MODE_CBC)
        d = data_cypher.decrypt(base64.b64decode(encrypted_data))[16:]
        data = str(d.decode("utf-8"))
        return data.rstrip(data[-1])
