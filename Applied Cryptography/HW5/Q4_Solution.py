"""
Carnegie Mellon University
18733 Spring 2017 Homework 5
ecc_template.py

credit to Kyle Soska
"""

#!/usr/bin/env python3

import collections
import random

#Used to refer to the curve group in an easy way
EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

#Used for computing modular inverses
import gmpy2
from gmpy2 import mpz

#PyCrypto
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Hash import SHA512
from Crypto.Hash import MD5

#Used to talk to the server
import urllib2
import urllib

#The public key of the server
server_public = (115298373626060981610489104680377423125111708405387674176313279119248115540205, 80069216135050533043624383887358773219529004216055598993959563334003920950746)

#secp256k1 elliptic curve standard - the group we will be using
curve = EllipticCurve(
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    h=1,
)


#Downloads 2 "games" which are just strings
#Return (game1, signature1, game2, signature2)
def download_games():
    try:
        request = urllib2.urlopen("http://katsuura.andrew.cmu.edu/~ksoska/18733/download_games.php")
    except urllib2.HTTPError, e:
        print "HTTP ERROR: " + str(e.code)

    contents = request.read()

    m1 = contents.split(",")[0]
    r1 = int(contents.split(",")[1])
    s1 = int(contents.split(",")[2])
    m2 = contents.split(",")[3]
    r2 = int(contents.split(",")[4])
    s2 = int(contents.split(",")[5])
    
    #The details for "game 1"
    print "m1: " + str(m1)
    print "r1: " + str(r1)
    print "s1: " + str(s1)

    #The details for "game 2"
    print "m2: " + str(m2)
    print "r2: " + str(r2)
    print "s2: " + str(s2)

    return (m1, (r1, s1), m2, (r2, s2))

#Upload our forgery to the server and see if it is accepted
#game: string
#signature: (r, s) where r and s are integers
def upload_game(game, signature):

    content = urllib.quote_plus(game + "," + str(signature[0]) + "," + str(signature[1]))
    try:
        request = urllib2.urlopen("http://katsuura.andrew.cmu.edu/~ksoska/18733/upload_game.php?content=" + content)
        return 1
    except:
        pass
    return




"""
**********************************************************
To be implemented
**********************************************************
"""

#Take in a point P, and return -P
def point_negation(p):
	#print("point_negation needs implementation!")
	if p is None:
		return None
	a, b = p
	return (a, -b%curve.p)


#Take in two points, P1, P2, return P1+P2
def point_addition(p1, p2):

    #print("point_addition needs implementation!")
	if p1 is None:
		return p2
	
	if p2 is None:
		return p1
    
	a1, b1 = p1
	a2, b2 = p2
	
	if a1 == a2 and b1 != b2:
		return None
	
	if a1 == a2:
		m = (3 * a1 * a1 + curve.a) * gmpy2.invert(2 * b1, curve.p)
		
	else:
		m = (b1 - b2) * gmpy2.invert(a1 - a2, curve.p)
	
	a3 = m * m - a1 - a2
	b3 = b1 + m * (a3 - a1)
	res = (a3 % curve.p, -b3 % curve.p)
	
	print "Point Addition: " + str(p1) + " + " + str(p2) + "is: " + str(res)
	return res

#Take in a point P and a scalar s, return sP
def scalar_multiplication(scalar, p):

    #print("scalar_multiplication needs implementation!")
    if scalar % curve.n == 0 or p is None:
        return None

    if scalar < 0:
        return scalar_mult(-scalar, point_neg(p))

    res = None
    add = p

    while scalar:
        if scalar & 1:
            res = point_addition(res, add)

        add = point_addition(add, add)

        scalar >>= 1

    return res

def sign_message(private_key, message):

    #For any input message, compute the SHA512 of the message and sign that
    h = SHA512.new()
    h.update(message)
    z = int(h.digest().encode('hex'), 16)

    #print("sign_message needs implementation!")
    a = 0
    b = 0
            
    while not a or not b:
        k = random.randrange(1, curve.n)
        x, y = scalar_multiplication(k, curve.g)
                                    
        a = x % curve.n
        b = ((z + a * private_key) * gmpy2.invert(k, curve.n)) % curve.n
                                                    
    return (a, b)


#If signature is valid, resturn "Valid", otherwise return "Invalid"
def verify_signature(public_key, message, signature):
    h = SHA512.new()
    h.update(message)
    z = int(h.digest().encode('hex'), 16)
        
    #print("verify_signature needs implementation!") 
    r, s = signature
                                                                
    w = gmpy2.invert(s, curve.n)
    a1 = (z * w) % curve.n
    a2 = (r * w) % curve.n
                                                                            
    x, y = point_addition(scalar_multiplication(a1, curve.g),
    scalar_multiplication(a2, public_key))
                                                                                
    if (r % curve.n) == (x % curve.n):
        return 'Valid'
    else:
        return 'Invalid'


def make_keypair():
    #print("make_keypair needs implementation!")
    private = random.randrange(1, curve.n)
    public = scalar_multiplication(private, curve.g)
    return private, public



def generate_forgery(m, game1, game2, sig1, sig2):
	
    #print("generate_forgery needs implementation!")
    r1, s1 = sig1
    r2, s2 = sig2
		  

    h = SHA512.new()
    h.update(game1)
    a1 = int(h.digest().encode('hex'), 16)

    h = SHA512.new()
    h.update(game2)
    a2 = int(h.digest().encode('hex'), 16)

    k = (a1 - a2) * gmpy2.invert(s1 - s2, curve.n) % curve.n

    pk = gmpy2.invert(r1, curve.n) * (k*s1 - a1) % curve.n

    return sign_message(int(pk), m)
	
	
#Lets simulate ECDH (Elliptic Curve Diffie-Hellman between two parties A and B

#Generate keypairs for two parties, A and B
skA, pkA = make_keypair()
skB, pkB = make_keypair()

print("Performing ECDH between A and B")
#Lets simulate ECDH (Elliptic Curve Diffie-Hellman) between A and B
#Recall the shared secret S = d_A*H_B = d_B*H_A = skA*pkB = skB*pkA
s1 = scalar_multiplication(skA, pkB)
s2 = scalar_multiplication(skB, pkA)
assert s1 == s2

print("ECDH Shared Secret: " + str(s1))



#Lets now take a look at how A and B might use this shared secret
#to communicate with each other

#Alice hashes the x-coordinate of the shared point to 256 bits
hx1 = SHA256.new()
hx1.update(str(s1[0]))

#Alice hashes the y-coordinate of the shared point to 128 bits
hy1 = MD5.new()
hy1.update(str(s1[1]))

#Bob hashes the x-coordinate of the shared point to 256 bits
hx2 = SHA256.new()
hx2.update(str(s2[0]))

#Bob hashes the y-coordinate of the shared point to 128 bits
hy2 = MD5.new()
hy2.update(str(s2[1]))


#We can use the hashed x-coordinate of the shared point as a secret key
#We can use the hashed y-coordinate of the shared point as an IV
#Alternatively it often makes sense to derive both the key and IV
#from the x-coordinate of the shared point
alice_aes = AES.new(hx1.digest(), AES.MODE_CBC, hy1.digest())
cipher_text = alice_aes.encrypt("This is a super secret message from Alice to Bob")
print("Alice Sends Ciphertext [" + str(cipher_text).encode('hex') + "] to Bob")

#Bob creates his own AES state exactly the same as Alice did
bob_aes = AES.new(hx2.digest(), AES.MODE_CBC, hy2.digest())
plain_text = bob_aes.decrypt(cipher_text)
print "Bob Recovers [" + str(plain_text) + "] From Alice"



#Now lets play with ECDSA (Elliptic Curve Digital Signature Algorithm)
message = "This is a message that we want Alice to sign"
signature = sign_message(skA, message)
verification = verify_signature(pkA, message, signature)

print("The signature [" + str(signature).encode('hex') + "] on [" + message + "] was [" + str(verification) + "]")




#Now that we have tested the code and know everything works, lets break
#An incorrect use of ECDSA from the server.

#The server uses the same key K for each pair of messages that it signs
#Use this to create a forgery of a valid server signature for a 
#random message of your choosing


#Download the games and signatures
game1, sig1, game2, sig2 = download_games()

#Perform a sanity check and make sure the downloaded games are valid
verification = verify_signature(server_public, game1, sig1)
print("Game 1 Signature Check: " + str(verification))

verification = verify_signature(server_public, game2, sig2)
print("Game 2 Signature Check: " + str(verification))

forgery_message = "Don't use the same K or different signatures!"
forgery_signature = generate_forgery(forgery_message, game1, game2, sig1, sig2)
result = upload_game(forgery_message, forgery_signature)

if result == 1:
    print("The server appears to have accepted the forgery, now visit the link in your browser!")
	#TNXQLIJSMKAUPEWFDSFIUUDBFDYEWVQTTUWMVXCBUDYWMILPFQGGKLPRLEWHVTQSYVTQSPDSGNDLRFWXKPDDPLNENYFXGMDSOYUTRMPUGKABYANYCSLWAXSUWGGAREANQTVULRDOHTIAAVSQEPBXVRRNLBYRCWKGTMFWVRXVFUVTPTQAAFTAPRMMIGMRASGUOPCTNVAYLMPLJLSSOYBCXGXCOHTINBLYLYHUIOKYJRHMSGUJKPYOFCTLMNKISXXMLRXOJLNBRPUYDOEFKRNPMRJBEANRKLMTPRLNPEXXHDDYYYEMNYLNRODJRUVFXMOXGPJDRNYGMKDHXNWXYKRUFPSDVXMCHHXCVOVVXVIYVVNRIARNPXSVVIADDVUETDBDVPWFXWDBTQYCALRBYOWMQTPODQYURVYGQCJKOWXDSQXHVJOLFGVAVBYMPEEIXMNEGBLBDURAOKSUXQCJNTRTJAUIROAQOOOWWHAVLEUREGFOTMSOVQDJQUPSCPUSKAKGASTSAGEUIGGPNAXPAQGBCLVQSTLTOLUGDRMEILTGEXSYOYPPHGETIFYHSPAOIQPEUUVBNQEHVMKTTBVNKFOFKOXNJUFAUFMTMEGXMRFWOUCLXJHEGRCNYTJOUYTLBFIYHYDHNBAIMJYJVPTOHLWBPIOHFDMDEFXXQCOCVOYCQCAXTQEXEVYKMRLPQNAGJFWSJVDSXYYJCJSEKBKNIQLEHXUTESUFQCICQRXKSITYSLCDUXBYMKRDRWGKAVPBOXQESQTJKGDICSAFHLAYNTAWJBUFYXNSPOSAMKXTJCAMYCUMIDXTXGFMNRBVIIFYJXHYYQOOSXHJAGFTYTACLWDHYBVTJUKDYBXGVFJLAHMTQTJQBBBMQOTEVJJWSQGEIMISEWCQDFXJSJFFPPVHGPELHNTAFSUNPEHDRUCTXWPUTOCQDNMGCMIHKTVGHHDIDDHLBNYMDUIHUPLQPMCGIOATXWNFLPYROPKWLMETVMQF,41487167248842446128257075879390222465206616485938837739603254886774352606339,85669209571785632377379514741348716983273424137693283026219929198782926677580,ROLWPFTAKHQVDFPYOPSXGEKACIAWNUYLEONAWTQQGPOPSDMOGLTAPONODGTJLMCOIVJAMQRYIBNDSNFMOUSOIQLQPPKGLFXLBQTQSPOBVQFDVYTVASYJWMIWJSKFYIVCBHIRURTHINKXFQFNEONQFWHFWWFGXRDHTXUXBEQOYODUMBQJTESAFJLQEAFMCIJSUFDWWOSRGHXXGCMRYAUDLETYWOAENOQYMKHLSPWHBYQRXRBRQWUESDDECMNJUMLEWAKWMSVOOEMKKRFYOTIVTRKWHBFUIHQAQJEMNOADYGPVEJMVSOMVDSQWVNTKJLVMMPGLXCTYQDVKENMFNBCAKFSAVBPDUEMJPTUWYPSKPAYYOGBVDKSDBHIWVHYRWFKBAWNMFQIXNITMLCQCJYKOPFUSKXLNCKKTDXUVAMPKLXVQFFKHGWBJDMNNHGUOCPXACGXLTFKFOWLDHLRUWICCNIYHWTOHXDKMVBOXTEKLGMRHQQHNYOBWMXMGVGTPVFOHQXMFSQNNRNHWSUHGMJNTJKCMEGODQRWIMYMKPHGVPCRQKCXURFSIVDVHPXALRCYFAGGISATINHNHAEXNXVEFGNMQMWGWLWBMJQPBSRYWEAJPFTHUPGATDTKDUSWFPYTMMEGORNWSRTWNSPBEJWJJAMYUSSPKOOAMLCWCCMSMCGBRTPPDCUURRHBNPMUNEBGULNGSUCHSLIUSLMDDVQCITTQYQVIQBUQUHYPROACBVGRTKOHEBNIRLRLBVEALDHWGDCEFQGDFFXBRHTTPDXGGNWGLCSEGNPCPYKXEMVNOQLQBWAHDYTYEUJVCPHWJJIJGFVFOAVARVIQKTQWLABPQCHKGCCIWVFXAQHYGVENCUTMDVFRWWNMHWLDVVEUJLJNRWSJAFGQXGEBESLRJHWCUVMFFGMODICKYGGWDFKVNTCLXSJNIMWXOODFADVFRSFFVEOSWSHUEQKACEKXHKTMSNQEAIBNOWIMYMISMMFGS,41487167248842446128257075879390222465206616485938837739603254886774352606339,8525118099001834277319445245638563234324031709137918641431655943955875473386 
	# ON visiting the site the value returned is JHHCWYVLAEHVUNOGXKWYEHLEHGDVHRDVFITVPFRBYIXBORPNDGJYTUJWOOFFUFIICSQJCCLLFMBLBIGXFOYCSEEWXCMTNJRSIHIQPYCTFEPBDDQQCMAVVXGRSLQSMHNATCUVFJRODAPFFCKYGRQDHBUOLOFXLJMRQLRDYROFQJXSWFNGUKACHASSRHIDWKJQSORPSWMJITJOBKFDLGBQRNPRDVLIFXLYKBRPMIRIIFMUCKNHTHBCKWKNBPSELIXAXRWHJSERSPDHDYSNQTSRWBORIXPQJTUCWOAIDUCBPOLVHEBYPIFUIFGWPBXVRUPQSPEJEHAKDBDFXFEPOQCTDSRDJLYTVQBAUYDOMCYEWGWKCLXMCOCWRBGPHMEMIKFDSPCDBBGKETUMCSRAKCAEKPFWNCKXGXYDDWIKSETSRMLMPJKUCVCWJQCKCVXBXXISIQNNIWCQHXMXROLGMARUWUSUSBUOHGSMOHIXBMBENKILEPIPACKBVIROGIULOPASMDQRNQXOKJDAJRNWRERGNYXTFTWVDDKJVYUQHBDTJSVCNGRWLHACBHCUKMNLCMSWCCTDXIYQVGSALFACYRPSQEJGXTCLLYSWMUTNTRXBKGNVQREKPRYXJUFUMMWGYWFIRLRUCONEWHIVNIOBXYTMNSCEQLNYSLSXMCGAQETKDTXYNXONFFHEUONTBECKBXFQTAKFSGFULUACHUGMNHDSJESJFRPXMTUMOOBDCVOSFSGGNWAMUHYTYLDVJSDLNSDGTSKKRTMGFETTOMIPNNOGYFMJVDCFPIWJYFPMUMYISUFPCLWEUHQWCVSPPAWPUKMNFKVGADFDMXHMKHBABXWMXTCKJCVLGVRLDQLNJNIBVLYNQIOHLAMLIIRKJGNYLWDHJUWUIGSGCARKJBKEHFNVXJRLQUDGPPUSTNYLLOSPJJOOEMRJAFYQMRWUSJCPQYWLJHTSQAAPGUPKLHOCWYADYSJMOKAEHVEIVSFRUUGL
else:
    print("Forgery Rejected") 
