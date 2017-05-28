import socks
import socket
import nanotime

sum = 0
print "Duckduckgo.com over tor"
for i in range(0,10):
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
	s = socks.socksocket()

	t1 = nanotime.now().nanoseconds()
	s.connect(('duckduckgo.com',443))
	t2 = nanotime.now().nanoseconds()

	t = t2-t1
	#sum = sum + t

	print 'Time difference for hidden clearnet service:',t      
