#
# Question 1.1.2.a
#
# Vishruta Rudresh
# vrudresh
#

from stem import CircStatus
from stem.control import Controller

with Controller.from_port(port = 9151) as controller:
	controller.authenticate()

	for circuit in sorted(controller.get_circuits()):
		if circuit.status != CircStatus.BUILT:
			continue

		print("")
		print("Circuit %s (%s)" % (circuit.id, circuit.purpose))

		for i, entry in enumerate(circuit.path):
			div = '+' if (i == len(circuit.path) - 1) else '|'
			fingerprint, nickname = entry

			desc = controller.get_network_status(fingerprint, None)
			address = desc.address if desc else 'unknown'
	
			print(" %s- %s (%s, %s)" % (div, fingerprint, nickname, address))
	
	  
