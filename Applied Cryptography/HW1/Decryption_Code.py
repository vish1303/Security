import re
import sys

def strxor(a, b):   
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def Decrypt():
    # obtain ASCII values of the given cipher texts
    cipher_ASCII = map(lambda x: x.decode("hex"), CT)
    msg = '' 
    for _ in xrange(60): 
        # loop from a to z
        nextChar = map(lambda x: msg+x, chars)
        for char in nextChar:
            # xor ciphertext to each of the letters
            key = strxor(cipher_ASCII[1], char)
            # xor the key so obtained for each cipher text in CT
            r = filter(lambda x: bool(re.search('^[a-z]+$', strxor(x, key))) == True, cipher_ASCII) 
            if len(r) == 10:
                #store the macthed letter and continue 
                 msg = char 

    print 'The secret message is: %s' %(strxor(secret_key, key))
    print "Key used for encryption is: %s"%key.encode('hex')
    print "Decrypted cipher texts using the key:"
    for i, cipher in enumerate(cipher_ASCII):
        print "[%d] %s" % (i+1, strxor(cipher, key))
    

CT = ["4a2c3819d63a04baa08757d3daa67deb114f30e8c199c8c6aae8fa2c5d9eea9a",
"533f280fc62512a4a98244cbdabc75e2184039f0d197c4d5b1f2e53b5394e196",
"5e2d3a04db3113a5a7924ecbd3a763f3125e34e5d59ddbdcbae0ef23469bf389",
"50222517cd2b18b1a59445dbceb877e10f5638e4d797ddd8a7e3e73e5483e290",
"473a2e16c53815bdb09c49d5c8a879e7025821eddb8cdbc9b3fae8394a92f482",
"5d362117de2203a9b99a5ec5d6ac7ae90a4425f9c685c5cea9efef285287f895",
"5b34371edf3d1fb7ba9558cadebe74f117532bf1cd9cceccaeebf3355a8be780",
"52333e0aca2f1fb6b48d40dec6b769f81f4c2efec293d6d0a2e5275291e38f",
"4f242f03d3280aacad9056c3dcb06de91a4d30e3cf89d0dfbcfcf62d429cec85",
"502c341cd73a08b9a18055ddd7ba70e41a4738f9cc95cad5b9e2f2255181e98d"]

secret_key = "7a392803d92704bdb18e0392d2a63be41e5432a9f49ec8cda4e4b3".decode('hex')
chars = map(lambda x: chr(x), range(97, 123))

Decrypt()
