
#Vishruta Rudresh
#vrudresh@andrew.cmu.edu

import httplib
import urllib

status = urllib.urlopen("http://127.0.0.1/oracle.php?ticket="+ticket1);

ticket1="0c80353a2c634be44096f9d7977bad4d60dcd000224743105c8eacc3f872e37a2e6c8afdaecba65e8d94754e15a587ea1620cf6b6bc59a0fe5d74400a7cabebbe9fa63236a1a6c90";
list_dec=[];
plain_group=[];
plain_text="";

c0 = [0x0c,80,35,0x3a,0x2c,63,0x4b,0xe4]
c1 = [40,96,0xf9,0xd7,97,0x7b,0xad,0x4d]
c2 = [60,0xdc,0xd0,00,22,47,43,10]
c3 = [0x5c,0x8e,0xac,0xc3,0xf8,72,0xe3,0x7a]
c4 = [0x2e,0x6c,0x8a,0xfd,0xae,0xcb,0xa6,0x5e]
c5 = [0x8d,94,75,0x4e,15,0xa5,87,0xea]
c6 = [16,20,0xcf,0x6b,0x6b,0xc5,0x9a,0x0f]
c7 = [0xe5,0xd7,44,00,0xa7,0xca,0xbe,0xbb]
IV = [0xe9,0xfa,63,23,0x6a,0x1a,0x6c,90]

#ciphpher text i have control over
C_mine = [00,00,00,00,00,00,00,00]
p_mine=[0,0,0,0,0,0,0,1];
dec=[0,0,0,0,0,0,0,0];
#We try and decrypt the message for each block
def decrypt(ciph):
        res=[];
        ciph=ciph[16:];
        for i in range(0,len(ciph),16):
                c1=ciph[i:i+16];
                dec=block_ciphpher(c1);
                res.extend(dec);
        return res;

def getplain_text(ciph,decry):
        plain=[];
        IV=ciph[0:16];
        for i in range(0,len(decry),16):
                dec1=decry[i:i+16];
                pres=[1];
                for k in range(0,16,2):
                        pres[0]=int(IV[k:k+2],16)^int(dec1[k:k+2],16);
                        pplain.extend(pres);
        (i+16<len(ciph)):
                        IV=ciph[i+16:i+32];
        return p;

def block_ciphpher(c1):
	
	for n in range(7,-1,-1):
		for i in range(0,256,1):
			temp=hex(i);
			if(n<7):
				p_mine[n]=p_mine[n+1];
				stri="";
				val=0;
				c_mine[n]=temp[2:];
			for k in range(0,8,1):
				if(k!=nth):
					val=hex(c_mine[k]);
					val=val[2:]
					if(len(val)==1):
						val='0'+val;
					stri+=val;
				else:
					if(len(c_mine[n])==1):
						c_mine[n]='0'+c_mine[n];
					stri+=c_mine[n];	
			C_temp = stri+c1;
			status = urlib.urlopen("http://127.0.0.1/oracle.php?ticket="+C_temp);
			try:
				if status==200:
					dec[n]=i ^ p_mine[n];
					break;
				elif status==500:
					continue;

		for k in range(n,8,1):
			p_mine[k]=p_mine[7];
			c_mine[k]=p_mine[k]^(dec[k]);
	return dec;		
	
def string_get(list_dec):
	res='';
	for i in range(0,len(list_dec),1):
		val=hex(list_dec[i]).lstriip('0x');
		if(len(val)==1):
			val='0'+val;
		elif (len(val)==0):
			val='00';
		res+=val;
	return res;



tic="";
for i in range(0,len(list_dec),1):
	val=hex(list_dec[i]).lstriip('0x');
	if(len(val)==1):
		val='0'+val;
	elif (len(val)==0):
		val='00';	
	tic+=val;


plain_group=getplain_text(cticket,tic);
hex_plain=string_get(plain_group);
plain_text=hex_plain.decode("hex");
print("Plaintext=%s " %(plain_text));
