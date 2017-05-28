import io
import pycurl
import stem.process
import socks
import socket
import urllib

from stem.util import term

SOCKS_PORT = 9150

f=open('countries.txt','r')
lines=f.read().splitlines()

def call_sock():
   socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
   socket.socket = socks.socksocket
   socket.getaddrinfo = getaddrinfo

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
	
call_sock();

def query(url):
  try:
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url


def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))

a = '{ru}'
for code in lines:
	print(term.format("Starting Tor:\n", term.Attr.BOLD))
	try:
		tor_process = stem.process.launch_tor_with_config(
  			tor_cmd='/home/osboxes/Downloads/tor-browser_en-US/Browser/TorBrowser/Tor/tor',
  			config = {
    			'SocksPort': str(SOCKS_PORT),
    			'ExitNodes': code.strip(),
  			},
  			init_msg_handler = print_bootstrap_lines,
		)
	except:
		print("Timed out in country %s \n" % code)
		continue
		if(tor_process is not None):
			tor_process.kill()  # stops tor

#print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
print(term.format(query("http://dogo.ece.cmu.edu/tor-homework/secret/"), term.Color.BLUE))

#tor_process.kill()
