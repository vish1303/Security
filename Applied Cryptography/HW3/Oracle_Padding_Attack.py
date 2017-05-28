import urllib2

def strxor(a, b):
	if len(a) > len(b):
		return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
	else:
		return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def solution(ct):
	ct = ct.decode("hex")
	RPT = ""
	PT = [chr(0) for i in range(len(ct))]
	pad = [chr(0) for i in range(len(ct))]
	for b in range(5):
		for i in range(1, 17):
			CRI = 0
			for k in range(i):
				pad[-16 - k - 1] = chr(i)
			for j in range(256):
				PT[-16 - i] = chr(j)
				tmp = strxor(PT, pad)
				r = oracle(strxor(tmp, ct))
				if r == 1:
					RPT = chr(j) + RPT
					print "Real text: " + str(RPT)
					break
				if r == 2:
					CRI = j
					if j == 255:
						PT[-16 - i] = chr(CRI)
						RPT = chr(CRI) + RPT
						break
        	if i == 16:
				ct = ct[:len(ct) - 16]
				PT = [chr(0) for i in range(len(ct))]
				pad = [chr(0) for i in range(len(ct))]
				break
	print "Plain Text: " + str(RPT)
	return

def oracle(decimal_token):
	try:
		page = "http://katsuura.andrew.cmu.edu/~ksoska/18733/banking.php?arg="
		url = page + decimal_token.encode('hex')
		#print page
		request = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		#print "HTTP ERROR: " + str(e.code)
		if e.code == 404:
			#print "404 error"
			return 0

		if e.code == 403:
			print "403 error"
			return 1
		else:
			#print "no error in request"
			return 2
			
solution("89c2a77f920d6d70632ec6a9121fe5b9c460c64b915bbd8cbc334602375b66d071ed0f1870c2902982948fe79ac5412fa467fca75c2091fad93e4b96d43b992b0c402a953a41a56749dfde36240c1df6299e9a8237b50e7bf968faa7ebb1a85d")
