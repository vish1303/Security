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

print "Connecting WITHOUT going over Tor"
initial = nanotime.now().nanoseconds()
print "Intial Connection without going over tor",initial     
response = urllib.urlopen('http://www.cmu.edu').getcode()
final = nanotime.now().nanoseconds()
print "Final Connection without going over tor",final   

time_diff = final - initial           
print "Time difference in nanoseconds: ",time_diff

print "--------------------------------------------------"

print "Connecting OVER Tor"
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9150,True)
socket.socket=socks.socksocket
initial = nanotime.now().nanoseconds()
print "Intial Connection going over tor",initial                 
response = urllib.urlopen('http://www.cmu.edu').getcode()
final = nanotime.now().nanoseconds()
print "Final Connection going over tor",final         

time_diff = final - initial
print "Time difference in nanoseconds: ",time_diff



