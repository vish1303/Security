
package DataTypes;
import NetworkElements.*;
import NetworkElements.Cat5e;
import NetworkElements.IPRouter;
import NetworkElements.IPNIC;

public class Example {
	public Example(){}
	
	public void go(){
		// Create some computers with NICs
		Computer hostA = new Computer();
		IPNIC hostANIC = new IPNIC("10.0.0.1", hostA);
		Computer hostB = new Computer();
		IPNIC hostBNIC = new IPNIC("10.0.0.2", hostB);
		Computer hostC = new Computer();
		IPNIC hostCNIC = new IPNIC("10.0.0.3", hostC);
		Computer hostD = new Computer();
		IPNIC hostDNIC = new IPNIC("10.0.0.4", hostD);
		
		// Create a router
		IPRouter router = new IPRouter();
		
		// Create NIC on the router and add a cable to the computers
		IPNIC routerNICA = new IPNIC("10.0.0.100", router);
		Cat5e linkAtoR = new Cat5e(hostANIC, routerNICA);
		
		IPNIC routerNICB = new IPNIC("10.0.0.100", router);
		Cat5e linkBtoR = new Cat5e(hostBNIC, routerNICB);
		
		IPNIC routerNICC = new IPNIC("10.0.0.100", router);
		Cat5e linkCtoR = new Cat5e(hostCNIC, routerNICC);
		
		IPNIC routerNICD = new IPNIC("10.0.0.100", router);
		Cat5e linkDtoR = new Cat5e(hostDNIC, routerNICD);
		
		// Add a record in the forwarding table for traffic to B
		router.addForwardingAddress(hostANIC.getIPAddress(), routerNICA);
		router.addForwardingAddress(hostBNIC.getIPAddress(), routerNICB);
		router.addForwardingAddress(hostCNIC.getIPAddress(), routerNICC);
		router.addForwardingAddress(hostDNIC.getIPAddress(), routerNICD);
		
		// Send a packet from A to B
		//hostA.sendPacket("10.0.0.2", 50);
		
		/*
		 * Remove comment marks to test FIFO
		 * should be
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.2 took 50 time
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.3 took 100 time
		 * (Computer): Received a packet 10.0.0.2 > 10.0.0.1 took 120 time
		 */
	/*router.setIsFIFO();
		hostA.sendPacket("10.0.0.2", 50);
		hostA.sendPacket("10.0.0.3", 50);
		hostB.sendPacket("10.0.0.1", 20);
		for(int i=0; i<125; i++)
			router.tock();
		*/
		/*
		 * Remove comment marks to test RR bit-by-bit
		 * should be
		 * (Computer): Received a packet 10.0.0.2 > 10.0.0.1 took 40 time
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.2 took 70 time
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.3 took 120 time
		 */
	/*	router.setIsRoundRobin();
		router.setRouteEntirePacket(false);
		hostA.sendPacket("10.0.0.2", 50);
		hostA.sendPacket("10.0.0.3", 50);
		hostB.sendPacket("10.0.0.1", 20);
		for(int i=0; i<200; i++)
		router.tock();
*/
		/*
		 * Remove comment marks to test RR, packet-by-packet
		 * should be
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.2 took 50 time
		 * (Computer): Received a packet 10.0.0.2 > 10.0.0.1 took 70 time
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.3 took 120 time
		 */
	/*	router.setIsRoundRobin();
		router.setRouteEntirePacket(true);
		hostA.sendPacket("10.0.0.2", 50);
		hostA.sendPacket("10.0.0.3", 50);
		hostB.sendPacket("10.0.0.1", 20);
		for(int i=0; i<200; i++)
			router.tock();
		
		/*
		 * Remove comment marks to test WRR, bit-by-bit
		 * should be
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.2 took 66 time
		 * (Computer): Received a packet 10.0.0.2 > 10.0.0.1 took 80 time
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.3 took 120 time
		 */
		/*router.setIsWeightedRoundRobin();
		router.setRouteEntirePacket(false);
		router.setQueueWeight(routerNICA, 3);
		router.setQueueWeight(routerNICB, 1);
		hostA.sendPacket("10.0.0.2", 50);
		hostA.sendPacket("10.0.0.3", 50);
		hostB.sendPacket("10.0.0.1", 20);
		for(int i=0; i<170; i++)
			router.tock();
		*/
		/*
		 * Remove comment marks to test WRR, packet-by-packet
		 * should be
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.2 took 50 time
		 * (Computer): Received a packet 10.0.0.2 > 10.0.0.1 took 70 time
		 * (Computer): Received a packet 10.0.0.1 > 10.0.0.3 took 120 time
		 */
	/*	router.setIsWeightedRoundRobin();
		router.setRouteEntirePacket(true);
		router.setQueueWeight(routerNICA, 6);
		router.setQueueWeight(routerNICB, 2);
		hostA.sendPacket("10.0.0.2", 50);
		hostA.sendPacket("10.0.0.3", 50);
		hostB.sendPacket("10.0.0.1", 20);
		for(int i=0; i<200; i++)
			router.tock();
		*/
		/*
		 * Remove comment marks to test WFQ, packet-by-packet
		 * should be
		(Computer) Trace: sending packet from computer
		est fin: 8.333333333333334
		(Computer) Trace: sending packet from computer
		est fin: 13.333333333333334
		(Computer) Trace: sending packet from computer
		est fin: 10.0
		(Computer) Trace: sending packet from computer
		est fin: 7.125
		(Computer): Received a packet 10.0.0.1 > 10.0.0.2 took 50 time
		(Computer) Trace: sending packet from computer
		est fin: 8.125
		(Computer): Received a packet 10.0.0.3 > 10.0.0.4 took 2 time
		(Computer) Trace: sending packet from computer
		est fin: 9.125
		(Computer): Received a packet 10.0.0.3 > 10.0.0.4 took 2 time
		(Computer): Received a packet 10.0.0.3 > 10.0.0.4 took 2 time
		(Computer) Trace: sending packet from computer
		est fin: 10.125
		(Computer): Received a packet 10.0.0.2 > 10.0.0.1 took 73 time
		(Computer): Received a packet 10.0.0.3 > 10.0.0.4 took 20 time
		(Computer) Trace: sending packet from computer
		est fin: 14.125
		(Computer) Trace: sending packet from computer
		est fin: 15.125
		(Computer): Received a packet 10.0.0.1 > 10.0.0.3 took 104 time
		(Computer): Received a packet 10.0.0.3 > 10.0.0.4 took 34 time
		(Computer): Received a packet 10.0.0.3 > 10.0.0.4 took 35 time

		 */
		router.setIsWeightedFairQueuing();
		router.setQueueWeight(routerNICA, 6);
		router.setQueueWeight(routerNICB, 2);
		hostA.sendPacket("10.0.0.2", 50);
		hostA.sendPacket("10.0.0.3", 30);
		hostB.sendPacket("10.0.0.1", 20);
		for(int i=0; i<49; i++)
			router.tock();
		hostC.sendPacket("10.0.0.4", 1);
		router.tock();
		hostC.sendPacket("10.0.0.4", 1);
		router.tock();
		hostC.sendPacket("10.0.0.4", 1);
		router.tock();
		router.tock();
		router.tock();
		hostC.sendPacket("10.0.0.4", 1);
		for(int i=0; i<20; i++)
			router.tock();
		hostC.sendPacket("10.0.0.4", 4);
		hostC.sendPacket("10.0.0.4", 1);
		for(int i=0; i<50; i++)
			router.tock();
		
		
	}
	
	public static void main(String args[]){
		Example go = new Example();
		go.go();
		
	}
}