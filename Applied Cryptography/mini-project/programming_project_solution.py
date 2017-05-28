"""

Kyle Soska
Carnegie Mellon University

18-733 Spring 2016 Programming Assignment
"""

from z3 import *
import struct
import sha256_template
import certificates_template
import urllib

class_certificate = "1.0,1,sha256-18RSA,Kyle Soska,1458864000,1460332800,18-733 Students,RSA2048,-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1YS52957a3EZ03k43Svz\nYx37HgmQxPGbDacPPKkUUfJ7e6m1THc+uS4U/ufGn4BtLxst/fF21QXvoFX3heWh\n491Nt+lM6NH8/uXp1juAtS7OEQcp1VMizdyIbHS47wLnEOx0I1SCh291FntE2mYS\naFSG5JHUoZm3TGvgIOYazrf16APk+/sqybi4s+c0KEKtmXT6GbI2Ku3GAGVItv7g\nu0P1zrCd9zMGQdUxrcE+zVtvAO1mew09k9r2vNAj8eR3RLtc2Ik9MHwLXXSkaGqM\nwLWAiKNsVmAJn8sGDBVcnDUapHbP3ft06kMkTTDubS50JORvprETjHj3Mr6Ofh0F\nxQIDAQAB\n-----END PUBLIC KEY-----,0,,,39ab19dff73349515dd34669ae1b5123e294ffe4129e7da8e0db30031b6ea1b718a9732fce878c8aa3a4fc18f42f5a2e84aead8b0101d90e9b90d4d6a20ddca6e05beea65ac1a08e6bab4e0afd1ab6e818f820da0c6c2b608b6e406444a5aa9885a5821980a564a6932b03f9fb354fe4dca4d60aebeb651233bb321903cfbcb620e3cb14e55d8debaf47c2b110ff1491b3cb2e1b3a48c11ede5f34351b1c0fb28416c64856715c6139dc44836f27a32526ab01097861b86383f9a994f067c234e3d56bdd304e1712e29049629a71f5d25cff99430cdf04f7830484d73d414773294833c684b8b6907b4db2809b8e18dff8710c841724ee39385edb26d3caed1"




#Returns a message for which the hash of it is 'output'
#_h: the initial state of _h for the hash collision, useful for generating rogue certificate
#output: the desired hash value of the message this function will find
#forbidden_input: this is an optional parameter that can be used to restrict the found message to be anything but forbidden_input
def sha_collision(_h, output, forbidden_input = None):

    num_iterations = 18

    _k = (0x428a2f98L, 0x71374491L, 0xb5c0fbcfL, 0xe9b5dba5L,
          0x3956c25bL, 0x59f111f1L, 0x923f82a4L, 0xab1c5ed5L,
          0xd807aa98L, 0x12835b01L, 0x243185beL, 0x550c7dc3L,
          0x72be5d74L, 0x80deb1feL, 0x9bdc06a7L, 0xc19bf174L,
          0xe49b69c1L, 0xefbe4786L, 0x0fc19dc6L, 0x240ca1ccL,
          0x2de92c6fL, 0x4a7484aaL, 0x5cb0a9dcL, 0x76f988daL,
          0x983e5152L, 0xa831c66dL, 0xb00327c8L, 0xbf597fc7L,
          0xc6e00bf3L, 0xd5a79147L, 0x06ca6351L, 0x14292967L,
          0x27b70a85L, 0x2e1b2138L, 0x4d2c6dfcL, 0x53380d13L,
          0x650a7354L, 0x766a0abbL, 0x81c2c92eL, 0x92722c85L,
          0xa2bfe8a1L, 0xa81a664bL, 0xc24b8b70L, 0xc76c51a3L,
          0xd192e819L, 0xd6990624L, 0xf40e3585L, 0x106aa070L,
          0x19a4c116L, 0x1e376c08L, 0x2748774cL, 0x34b0bcb5L,
          0x391c0cb3L, 0x4ed8aa4aL, 0x5b9cca4fL, 0x682e6ff3L,
          0x748f82eeL, 0x78a5636fL, 0x84c87814L, 0x8cc70208L,
          0x90befffaL, 0xa4506cebL, 0xbef9a3f7L, 0xc67178f2L) 
    
    s = Solver()
    
    x = [BitVec('x%s' % i, 32) for i in range(16)]
    w1 = [BitVec('w1_%s' % i, 32) for i in range(64)]
    a = [BitVec('a%s' % i, 32) for i in range(20)]
    b = [BitVec('b%s' % i, 32) for i in range(20)]
    c = [BitVec('c%s' % i, 32) for i in range(20)]
    d = [BitVec('d%s' % i, 32) for i in range(20)]
    e = [BitVec('e%s' % i, 32) for i in range(20)]
    f = [BitVec('f%s' % i, 32) for i in range(20)]
    g = [BitVec('g%s' % i, 32) for i in range(20)]
    h = [BitVec('h%s' % i, 32) for i in range(20)]
    s0 = [BitVec('s0_%s' % i, 32) for i in range(20)]
    maj = [BitVec('maj_%s' % i, 32) for i in range(20)]
    t2 = [BitVec('t2_%s' % i, 32) for i in range(20)]
    s1 = [BitVec('s1_%s' % i, 32) for i in range(20)]
    ch = [BitVec('ch_%s' % i, 32) for i in range(20)]
    t1 = [BitVec('t1_%s' % i, 32) for i in range(20)]

    for i in range(0, 16):
    	s.add(w1[i] == x[i])
    

    for i in range(16, num_iterations):
        s.add(w1[i] == (RotateRight(w1[i-15], 7) ^ RotateRight(w1[i-15], 18) ^ LShR(w1[i-15], 3)) + (RotateRight(w1[i-2], 17) ^ RotateRight(w1[i-2], 19) ^ LShR(w1[i-2], 10)) + w1[i-16] + w1[i-7])

 
    
    #Set the initial value of the hash
    s.add(a[0] == _h[0])
    s.add(b[0] == _h[1])
    s.add(c[0] == _h[2])
    s.add(d[0] == _h[3])
    s.add(e[0] == _h[4])
    s.add(f[0] == _h[5])
    s.add(g[0] == _h[6])
    s.add(h[0] == _h[7])



    #Execute the 18 inner loops of SHA256-18
    for i in range(num_iterations):

        s.add(s0[i] == RotateRight(a[i], 2) ^ RotateRight(a[i], 13) ^ RotateRight(a[i], 22))
        s.add(maj[i] == (a[i] & b[i]) ^ (a[i] & c[i]) ^ (b[i] & c[i]))
        s.add(t2[i] == s0[i] + maj[i])
        s.add(s1[i] == RotateRight(e[i], 6) ^ RotateRight(e[i], 11) ^ RotateRight(e[i], 25))
        s.add(ch[i] == (e[i] & f[i]) ^ ((~e[i]) & g[i]))
        s.add(t1[i] == h[i] + s1[i] + ch[i] + _k[i] + w1[i])

        s.add(h[i+1] == g[i])
        s.add(g[i+1] == f[i])
	s.add(f[i+1] == e[i])
        s.add(e[i+1] == d[i] + t1[i])
        s.add(d[i+1] == c[i])
        s.add(c[i+1] == b[i])
	s.add(b[i+1] == a[i])
        s.add(a[i+1] == t1[i] + t2[i])
        
    
    #Some finishing touches
    s.add(a[num_iterations+1] == a[0] + a[num_iterations]) 
    s.add(b[num_iterations+1] == b[0] + b[num_iterations])
    s.add(c[num_iterations+1] == c[0] + c[num_iterations])
    s.add(d[num_iterations+1] == d[0] + d[num_iterations])
    s.add(e[num_iterations+1] == e[0] + e[num_iterations])
    s.add(f[num_iterations+1] == f[0] + f[num_iterations])
    s.add(g[num_iterations+1] == g[0] + g[num_iterations])
    s.add(h[num_iterations+1] == h[0] + h[num_iterations])


    #Need to tell z3 to generate a collision of course
    s.add(a[num_iterations+1] == output[0])
    s.add(b[num_iterations+1] == output[1]) 
    s.add(c[num_iterations+1] == output[2])
    s.add(d[num_iterations+1] == output[3])
    s.add(e[num_iterations+1] == output[4])
    s.add(f[num_iterations+1] == output[5])
    s.add(g[num_iterations+1] == output[6])
    s.add(h[num_iterations+1] == output[7])


    #Solve the model
    print(s.check())
    model = s.model()

    print model
    collision = []
    print "x values: "+ str(collision)
    for i in range(16):
        collision.append(int(str(model[x[i]])))
    
    return ''.join([struct.pack('!L', i) for i in collision])


#Finds some m != message such that SHA256-18(m) = SHA256-18(message)
def generate_hash_collision(message):

    digest = sha256_template.sha256(message).digest()
    _h = (0x6a09e667L, 0xbb67ae85L, 0x3c6ef372L, 0xa54ff53aL, 0x510e527fL, 0x9b05688cL, 0x1f83d9abL, 0x5be0cd19L)
    output = struct.unpack('!8L', digest)
    collision = sha_collision(_h, output, None)
    collision_digest = sha256_template.sha256(collision).digest()
    
    print "hash collision (hex): " + str(collision.encode('hex'))

    #Just double check to make sure we didnt make a mistake
    if collision_digest == digest:
        print "The collision is valid"
    else:
        print "The collision is invalid"



def generate_rogue_ca_cert(version = 1.0, serial = 1, sig_algorithm = "sha256-18RSA", issuer = "Kyle Soska", validity_start = 1458864000, validity_end = 1460332800, subject_name = "18-733 Students", subject_public_key_algorithm = "RSA2048", subject_public_key = "0", is_ca = 1, issuer_unique_id = "", subject_unique_id = "", signer_private_key_str = ""):


    #Create the certificate that we want to have
    cert = "" 
    cert += str(version) + ","
    cert += str(serial) + ","
    cert += str(sig_algorithm) + ","
    cert += str(issuer) + ","
    cert += str(validity_start) + ","
    cert += str(validity_end) + ","
    cert += str(subject_name) + ","
    cert += str(subject_public_key_algorithm) + ","
    cert += str(subject_public_key) + ","
    cert += str(is_ca) + ","
    cert += str(issuer_unique_id) + ","

    #Pad the certificate up to a block size, we can do this more intellegent ways, but this is fine
    cert += str(subject_unique_id)
    cert += '\x00'*(64 - (len(cert) % 64))

    #We want the output of the new cert to be the same as the one made for the class
    digest = sha256_template.sha256(cert).digest()
    _h = struct.unpack('!8L', digest)
    
    #Figure out what the hash of the certificate is so far
    digest = sha256_template.sha256(class_certificate[:(class_certificate.rfind(","))]).digest()
    output = struct.unpack('!8L', digest)

    collision = sha_collision(_h, output, None)
    
    #Add our new magical block onto the certificate
    cert += collision

    #Add the old signature onto the new certificate
    cert += class_certificate[530:]

    print "Rogue Cert: " + cert
    print "Url Encoded Rogue Cert: " + urllib.quote_plus(cert)
    

    print "URL: http://katsuura.andrew.cmu.edu/~ksoska/18733/check_cert.php?cert=" + urllib.quote_plus(cert)

    return cert




generate_hash_collision("Random String For Generating Collision")
generate_rogue_ca_cert()