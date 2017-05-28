#
# Vishruta Rudresh
# vrudresh
#
# q 1.2.3
#

import urllib
import nanotime
import socket
import socks
import nanotime

print "Connecting Clearnet version not over Tor"
for i in range(0,10):
	initial = nanotime.now().nanoseconds()
#	print "Intial Connection without going over tor",initial     
	response = urllib.urlopen('https://duckduckgo.com/').getcode()
	final = nanotime.now().nanoseconds()
#	print "Final Connection without going over tor",final   

	time_diff = final - initial           
	print "Time difference in nanoseconds: ",time_diff

print "--------------------------------------------------"

print "Connecting Clearnet version over Tor"
for i in range(0,10):
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9150,True)
	socket.socket=socks.socksocket
	initial = nanotime.now().nanoseconds()
#	print "Intial Connection going over tor",initial
	response = urllib.urlopen('https://duckduckgo.com/').getcode()
	final = nanotime.now().nanoseconds()
#	print "Final Connection going over tor",final

	time_diff = final - initial
	print "Time difference in nanoseconds: ",time_diff

print "--------------------------------------------------"

print "Connecting Tor Hidden Service"
for i in range(0,10):
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9150,True)
	socket.socket=socks.socksocket
	initial = nanotime.now().nanoseconds()
	#print "Intial Connection going over tor",initial                 
	response = urllib.urlopen('http://3g2up14pq6kufc4m.onion/').getcode()
	final = nanotime.now().nanoseconds()
	#print "Final Connection going over tor",final         
	time_diff = final - initial
	print "Time difference in nanoseconds: ",time_diff



