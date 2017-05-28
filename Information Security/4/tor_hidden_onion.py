import socks
import socket
import nanotime

sum = 0
print "Tor hidden service"
for i in range(0,10):
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
	s = socks.socksocket()

	t1 = nanotime.now().nanoseconds()
	s.connect(('3g2upl4pq6kufc4m.onion',80))
	t2 = nanotime.now().nanoseconds()

	t = t2-t1

	print 'Time difference for hidden onion service:',t      
