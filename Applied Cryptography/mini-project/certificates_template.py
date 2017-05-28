"""
Kyle Soska
Carnegie Mellon University
18-733 Spring 2016 Programming Assignment

certificates.py
"""

from Crypto.PublicKey import RSA
import sha256_template
import urllib

kyle_public = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqP1Im3QSIeuB2JBXq7Ip\nRoFXvT8HVDIBsQnGPiTylMpFw2cmZbNgEUlRQI0ne2OJv+HWis/ZGAA98fMwYbOo\nd5cxbCVEYpOpggaDMbUw9PBfEtzqcXB3FKR/Nz3uwJ/GIWurr95nxB2Kcvb6XVWs\nAkwJbpc9eWDSrtjmjIQi0RpGtsBm+vyQbRhdPadeticQCIdqNMqfwZ++2ltJYC2L\nkw8wCJPppdwFB8doDMk3Np0F7PjWD4Q0dEBnLYhkFNrECJhKjv6Dy3S5F5C0zK4Q\ncIPWqwBGOC+It9GYRGx4tnGdnOVfl5s+n8Jff1H72oOyhMqSLZrm3qeJFdu50hHb\nYwIDAQAB\n-----END PUBLIC KEY-----"

class_public = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu4/FPM7qqOoUlfIYxuB/\nMQVlLVW4+qubaEpJHOKFMl+1PoZ7vboaJx+EupwPgWcnBAJ7AOSZ4RNVlVq2ISKU\n0i+a2xDw/WFTdP/85S3Wi5D+VAvpT7S4UTXIWA+u/VYAZvqrLX7Pvj2aLOaxleD3\nMfkYpYGfBkC9AjiCrOH+HXY6J3sbLW2NmFthAqVRjRBp2+B8Z5UHh4FR2ht/j2JY\n/BH5/pyc5FFRSUxrvTGHrOJM7CG7JsSVwEwuXNIf3R6ol+d6AsMV051BnLX352IU\n+1yEHe1LY7m3X/GSl1dX5MrrmjUCvizRDjGw8dzXn761ZkHxBdnqiMjyP97mLm4q\n5wIDAQAB\n-----END PUBLIC KEY-----"

class_private = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAu4/FPM7qqOoUlfIYxuB/MQVlLVW4+qubaEpJHOKFMl+1PoZ7\nvboaJx+EupwPgWcnBAJ7AOSZ4RNVlVq2ISKU0i+a2xDw/WFTdP/85S3Wi5D+VAvp\nT7S4UTXIWA+u/VYAZvqrLX7Pvj2aLOaxleD3MfkYpYGfBkC9AjiCrOH+HXY6J3sb\nLW2NmFthAqVRjRBp2+B8Z5UHh4FR2ht/j2JY/BH5/pyc5FFRSUxrvTGHrOJM7CG7\nJsSVwEwuXNIf3R6ol+d6AsMV051BnLX352IU+1yEHe1LY7m3X/GSl1dX5MrrmjUC\nvizRDjGw8dzXn761ZkHxBdnqiMjyP97mLm4q5wIDAQABAoIBAQCIovj+DoMWoMh0\nX9S69QrTrGmDuEI0otVpCUzv9PkxtFV2AkSc97lbrPNlepE1JO9gVWpEQUT0mcAs\nONQbmXSvFi0Kz/GvtLo2rtIOJvF35R3SHodOIIpx5utXc714IrHSU2RmlU5D+d6a\nPUk7tZJ/XkcdMyulQ34t4vsXdN9Jl/raiRXb9Qymc4Rb9gf4fUtC9oXrDI03Lf4q\noxsPgt/L3ZOMdnWUfErznXH6myZBQhwfgvnzCq/nemyx4u1pWVXJYetK9ePqlRUh\ntUlyYBE0GeMlGUDgyZHOjCqu80gR17f1Gr1lS1kc3qU6Fu1o8rALmITaO1U8GCJe\n9x22Y1vJAoGBANOo7lWuB0sdmcXjwD4Yw9PttRHuXj8W0vTGye8vZSiOBnzinPSK\neD08oJnaN+jWBzzyTYNj+AW4bcYSW87NS4BP4LHINg3Fw0PuxlYK7R1AQEPyNHQj\n1VPutqktLjNnYlI8MhtkJsN8fw+CljFakvHD4/Yk2gEB/A6PdRwVElozAoGBAOLa\neiGClGLWNdslcfVrMAi8VJ+0bKzpsih1sG5Lvgcs+te7qKcjsoc7ZjTm3gMV+cjs\n7Wf+DpSTrUpHIQbCLa8Zx8vEr9ZO0sqPEIWveNNEorJ7993L4ceAtILM955c8qra\nkr5BvCaxynhAD/b22NnZANgiW0ol9brGtLyHx2B9AoGBAIEcVi4Ll0VZzBhrYjQ+\n1Q2svbwvZGwllw9bR4jQp2tCn3CEp2uAH/JyziCrfVlZXVbvExtn2r5ajxO41Snk\nDv85On4X++kQzpjcyT1pMtSaAdmwoBCMXy/wuJmgBsOyd8ZkE8ijogWzJqqmZMm8\nT1CMxry6JAVjWYbkOXKk4+oDAoGAfsFK2qyG0w8UOqYaneHNjiQFONNsodVWuerA\nsXBa9tF4O9DcdL+qgot7GXYieSDvWAiiwqefZ/94JXfHCWq4cg16qO32vk1+1LXJ\nqpkYbxv7uLUyE1lXh8zvj+KNPYx7/2Fv+yTpx8kx86z//qOBGYB6S0ovLig1vK5I\n0MshaVUCgYBwmuK0qWXvCZd7fY5qgmRvgO6sClUt1fJ+yxe2q+GSw2ZzdErI+sU5\njSAAierwe769HE8jFzCFtFArC0lTGQYiqrze4DTd82Vdjd0aGzYV19t9vwjYUCwx\nlFBvGaymLYeiX2c80/+w4nwFZGgm2ud/GAGbG1BjV86EmWF/y6w9cg==\n-----END RSA PRIVATE KEY-----"


#Certificate for the class signed by kyle's private key
class_certificate = "1.0,1,sha256-18RSA,Kyle Soska,1458864000,1460332800,18-733 Students,RSA2048,-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1YS52957a3EZ03k43Svz\nYx37HgmQxPGbDacPPKkUUfJ7e6m1THc+uS4U/ufGn4BtLxst/fF21QXvoFX3heWh\n491Nt+lM6NH8/uXp1juAtS7OEQcp1VMizdyIbHS47wLnEOx0I1SCh291FntE2mYS\naFSG5JHUoZm3TGvgIOYazrf16APk+/sqybi4s+c0KEKtmXT6GbI2Ku3GAGVItv7g\nu0P1zrCd9zMGQdUxrcE+zVtvAO1mew09k9r2vNAj8eR3RLtc2Ik9MHwLXXSkaGqM\nwLWAiKNsVmAJn8sGDBVcnDUapHbP3ft06kMkTTDubS50JORvprETjHj3Mr6Ofh0F\nxQIDAQAB\n-----END PUBLIC KEY-----,0,,,39ab19dff73349515dd34669ae1b5123e294ffe4129e7da8e0db30031b6ea1b718a9732fce878c8aa3a4fc18f42f5a2e84aead8b0101d90e9b90d4d6a20ddca6e05beea65ac1a08e6bab4e0afd1ab6e818f820da0c6c2b608b6e406444a5aa9885a5821980a564a6932b03f9fb354fe4dca4d60aebeb651233bb321903cfbcb620e3cb14e55d8debaf47c2b110ff1491b3cb2e1b3a48c11ede5f34351b1c0fb28416c64856715c6139dc44836f27a32526ab01097861b86383f9a994f067c234e3d56bdd304e1712e29049629a71f5d25cff99430cdf04f7830484d73d414773294833c684b8b6907b4db2809b8e18dff8710c841724ee39385edb26d3caed1"


def createCertificate(version = 1.0, serial = 1, sig_algorithm = "sha256-18RSA", issuer = "Kyle Soska", validity_start = 1458864000, validity_end = 1460332800, subject_name = "18-733 Students", subject_public_key_algorithm = "RSA2048", subject_public_key = "0", is_ca = 0, issuer_unique_id = "", subject_unique_id = "", signer_private_key_str = ""):

    privKeyObj = RSA.importKey(signer_private_key_str)

    cert = "" #This is the string that will become the certificate
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
    cert += str(subject_unique_id)
    cert += "," + str(format(privKeyObj.sign(sha256_template.sha256(cert).digest(), K = "")[0], 'x'))
    return cert


def verifyCertificate(cert, pk_str):
    pubKeyObj = RSA.importKey(kyle_public)

    version = float(cert.split(",")[0])
    serial = int(cert.split(",")[1])
    sig_algorithm = cert.split(",")[2]
    issuer = cert.split(",")[3]
    validity_start = int(cert.split(",")[4])
    validity_end = int(cert.split(",")[5])
    subject_name = cert.split(",")[6]
    subject_public_key_algorithm = cert.split(",")[7]
    subject_public_key = cert.split(",")[8]
    is_ca = int(cert.split(",")[9])
    issuer_unique_id = cert.split(",")[10]
    subject_unique_id = cert.split(",")[11]
    sig = (long(cert.split(",")[12], 16),)

    pk = RSA.importKey(pk_str)
    return pk.verify(sha256_template.sha256(cert[:(cert.rfind(","))]).digest(), sig)


def urlencodeCertificate(cert):
    return urllib.quote_plus(cert)

def testCertificates():
    cert = createCertificate(subject_public_key = class_public, signer_private_key_str = class_private)
    print ("Created Certificate: " + str(cert))
    print ("Certificate Verify: " + str(verifyCertificate(cert, class_public)))
    print ("Class Verify: " + str(verifyCertificate(class_certificate, kyle_public)))
    print ("URL Encoded Cert: " + str(urlencodeCertificate(class_certificate)))
