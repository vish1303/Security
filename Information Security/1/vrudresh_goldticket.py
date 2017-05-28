#VISHRUTA RUDRESH
#vrudresh@andrew.cmu.edu

import httplib
import urllib

status = urllib.urlopen("http://127.0.0.1/oracle.php?ticket="+ticket1);

ticket1="0c80353a2c634be44096f9d7977bad4d60dcd000224743105c8eacc3f872e37a2e6c8afdaecba65e8d94754e15a587ea1620cf6b6bc59a0fe5d74400a7cabebbe9fa63236a1a6c90";

golden_ticket='{"username":"vrudresh","is_admin":"true","expired":"2015-12-21"}'
block_dec="77a24049491125852df3dbedb51cd82813a8f22c002e304f3deac1aa9650d958480de68ecbe98a7ce8ec052767c0e3c82c02fd5b5bf5b73fd4fa773185b7bcb9"
hex_gold="7b22757365726e616d65223a22616a68616e776131222c2269735f61646d696e223a2274727565222c2265787069726564223a22323031382d31322d3331227d0808080808080808"

def Convert_to_hex(IV):
	res="";
	for i in range(0,len(IV),1):
		val=hex(IV[i]).lstrip('0x');
		if(len(val)==1):
			val='0'+val;
		elif (len(val)==0):
			val='00';	
		res+=val;
	return res;

def ci_text(Decry,plain):
	C=[];
	for i in range(72):
		C.append(0);
	di=Decry[len(Decry)-16:];
	pi=plain[len(plain)-16:];
	IV=[None]*8;
	k=71;
	for i in range(15,-1,-2):
		IV[i/2]=int(di[i-1:i+1],16)^int(pi[i-1:i+1],16);
		C[k]=IV[i/2];
		k=k-1;
	for i in range(len(plain)-32,-1,-16):
		pi=plain[i:i+16];
		ci=gethexfromlist(IV);
		di=oneblock(ci);
		for j in range(15,-1,-2):
			IV[j/2]=di[j/2]^int(pi[j-1:j+1],16);
			C[k]=IV[j/2];
			k=k-1;
		
	return C;

