import urllib
import nanotime
import socket
import socks
import nanotime

print "Connecting duckduckgo WITHOUT going over Tor"

for i in range(0,10):
	initial = nanotime.now().nanoseconds()
	response = urllib.urlopen('https://duckduckgo.com').getcode()
	final = nanotime.now().nanoseconds()

	time_diff = final - initial           
	print "Time difference in nanoseconds: ",time_diff

