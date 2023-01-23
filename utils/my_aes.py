import base64
from Crypto.Cipher import AES
from Crypto import Random
from MyTools import settings


def AesEncrypt(data):
    aes = AES.new(settings.AES_KEY,AES.MODE_ECB) 
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    en_text = aes.encrypt(pad(data)) #加密明文
    en_base64 = str(base64.b64encode(en_text), encoding="utf8")
    return en_base64


def AesDecrypt(data):
    aes = AES.new(settings.AES_KEY,AES.MODE_ECB) 
    en_text = base64.b64decode(data) #将进行base64解码，返回值依然是bytes
    den_text = aes.decrypt(en_text)
    unpad = lambda s : s[0:-ord(s[-1])]
    aes_result = unpad(str(den_text, encoding="utf8"))
    return aes_result
