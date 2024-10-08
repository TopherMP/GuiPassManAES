from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def deriveKey(masterPass, salt): # Derive master password
    key = PBKDF2(masterPass, salt, dkLen=32, count=125000, hmac_hash_module=SHA256)
    return key

def encryptMasterPass(masterPass, pswrd):
    salt = get_random_bytes(16)
    key = deriveKey(masterPass,salt)

    cipher = AES.new(key,AES.MODE_EAX)
    nonce = cipher.nonce
    cipherText, tag = cipher.encrypt_and_digest(pswrd.encode('utf-8'))

    return salt, nonce, cipherText, tag

def decryptMasterPass(masterPass, salt, nonce, tag, cipherText):

    key = deriveKey(masterPass, salt)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plainText = cipher.decrypt_and_verify(cipherText, tag)

    return plainText.decode('utf-8')