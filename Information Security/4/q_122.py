#
# Vishruta Rudresh
# vrudresh
#
# Question 1.2.2

import urllib
import nanotime
import time
import socket
import socks
from stem import Signal
from stem.control import Controller

num = 10
sum = 0
print "Connecting over Tor"
with Controller.from_port(port = 9151) as controller:
	controller.authenticate()

	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
	socket.socket = socks.socksocket
	for i in range(0,num):
		controller.signal(Signal.NEWNYM)
		time.sleep(10)
		initial_time = nanotime.now().nanoseconds()
		urllib.urlopen('http://www.cmu.edu').getcode()	
		final_time = nanotime.now().nanoseconds()
		time_diff = final_time - initial_time
		print "Round ",i,time_diff
		sum = sum + time_diff

print "Average over the samples(over tor) = ",sum/num
print "------------------------------------------"

print "Connecting without Tor"
for i in range(0,num):
	initial_time = nanotime.now().nanoseconds()
        urllib.urlopen('http://www.cmu.edu').getcode()
        final_time = nanotime.now().nanoseconds()
        time_diff = final_time - initial_time
        print "Round ",i,time_diff
        sum = sum + time_diff

print "Average over the samples(without tor) = ",sum/num

	
