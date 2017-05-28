#
# Question 1.1.2.b
#
# Vishruta Rudresh
# vrudresh
#
from stem.control import Controller
from stem.util.str_tools import get_size_label
from geoip import geolite2
from stem import CircStatus

# Entry nodes only
with Controller.from_port(port = 9151) as controller:
        controller.authenticate()

        print "Entry nodes are : "
	print "\n"
        for circ in controller.get_circuits():
                if circ.status != CircStatus.BUILT:
                        continue

                entry_fingerprint = circ.path[0][0]
		print "Fingerprint = ",entry_fingerprint
                desc = controller.get_network_status(entry_fingerprint, None)
                if entry_fingerprint:
                        print "Circuit %s has IP %s" % (circ.id, desc.address)
                else:
                        print "IP not found for circuit %s" % circ.id

                location = geolite2.lookup(desc.address)
                print "Location is: ",location
		print "Current bandwidth: ",desc.bandwidth
                print "\n"
print "---------------------------------------------------------------------------"
print "\n"
# Middle nodes only
with Controller.from_port(port = 9151) as controller:
        controller.authenticate()

        print "Middle nodes are : "
	print "\n"
        for circ in controller.get_circuits():
                if circ.status != CircStatus.BUILT:
                        continue

                num_of_middle_nodes = len(circ.path)
                for i in range(1,num_of_middle_nodes - 1):
                        middle_fingerprint = circ.path[i][0]
                        middle_desc = controller.get_network_status(middle_fingerprint, None)
                        print "Fingerprint = ",middle_fingerprint

                        if middle_fingerprint:
                                print "Circuit %s has IP %s" % (circ.id, middle_desc.address)
                        else:
                                print "IP not found for circuit %s" % circ.id

                        location = geolite2.lookup(middle_desc.address)
                        print "Location is: ",location
			print "Current bandwidth: ", middle_desc.bandwidth
                        print "\n"
print "---------------------------------------------------------------------------"
print "\n"

# Exit nodes only
with Controller.from_port(port = 9151) as controller:
        controller.authenticate()

        print "Exit nodes are: "
	print "\n"
        for circ in controller.get_circuits():
                if circ.status != CircStatus.BUILT:
                        continue

                exit_fingerprint = circ.path[-1][0]
                exit_desc = controller.get_network_status(exit_fingerprint, None)
                print "Fingerprint = ",exit_fingerprint

                if exit_fingerprint:
                        print "Circuit %s has IP %s" % (circ.id, exit_desc.address)
                else:
                        print "IP not found for circuit %s" % circ.id

                location = geolite2.lookup(exit_desc.address)
                print "Location is: ",location
		print "Current bandwidth: ", exit_desc.bandwidth
                print "\n"

