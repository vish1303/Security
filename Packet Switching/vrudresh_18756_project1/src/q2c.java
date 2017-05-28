import java.util.ArrayList;

import DataTypes.SONETFrame;
import DataTypes.SPE;
import NetworkElements.OpticalNICTA;
import NetworkElements.OtoOLink;
import NetworkElements.SONETRouter;


public class q2c {
	public void twoRings(){
		/*
		 * Setup the network
		 */
		System.out.println("Setting up three routers");
		// Create three SONET routers
		SONETRouter router1 = new SONETRouter("00:11:22");
		SONETRouter router2 = new SONETRouter("88:77:66");
		SONETRouter router3 = new SONETRouter("33:44:55");
		
		// tell routers a wavelength to add/drop on (in this case their own frequencies)
		router1.addDropWavelength(1310);
		router2.addDropWavelength(1490);
		router3.addDropWavelength(1550);
		
		// tell router 1 the wavelength each router is add/dropping on
		router1.addDestinationFrequency("00:11:22", 1310);
		router1.addDestinationFrequency("88:77:66", 1490);
		router1.addDestinationFrequency("33:44:55", 1550);
		
		// tell router 2 the wavelength each router is add/dropping on
		router2.addDestinationFrequency("00:11:22", 1310);
		router2.addDestinationFrequency("88:77:66", 1490);
		router2.addDestinationFrequency("33:44:55", 1550);
		
		// tell router 3 the wavelength each router is add/dropping on
		router3.addDestinationFrequency("00:11:22", 1310);
		router3.addDestinationFrequency("88:77:66", 1490);
		router3.addDestinationFrequency("33:44:55", 1550);
		
		// Create an interface for each router
		OpticalNICTA nicRouter11 = new OpticalNICTA(router1);
		nicRouter11.setID(11);
		OpticalNICTA nicRouter12 = new OpticalNICTA(router1);
		nicRouter12.setID(12);
		OpticalNICTA nicRouter13 = new OpticalNICTA(router1);
		nicRouter13.setID(13);
		OpticalNICTA nicRouter113 = new OpticalNICTA(router1);
		nicRouter113.setID(113);
		
		OpticalNICTA nicRouter21 = new OpticalNICTA(router2);
		nicRouter21.setID(21);
		OpticalNICTA nicRouter22 = new OpticalNICTA(router2);
		nicRouter22.setID(22);
		OpticalNICTA nicRouter23 = new OpticalNICTA(router2);
		nicRouter23.setID(23);
		OpticalNICTA nicRouter223 = new OpticalNICTA(router2);
		nicRouter223.setID(223);
		
		OpticalNICTA nicRouter331 = new OpticalNICTA(router3);
		nicRouter331.setID(331);
		OpticalNICTA nicRouter332 = new OpticalNICTA(router3);
		nicRouter332.setID(332);
		OpticalNICTA nicRouter31 = new OpticalNICTA(router3);
		nicRouter31.setID(31);
		OpticalNICTA nicRouter32 = new OpticalNICTA(router3);
		nicRouter32.setID(32);
		
		// Create two bi-directional links between the routers
		//Working links
		OtoOLink OneToTwo1 = new OtoOLink(nicRouter11, nicRouter21);
		OtoOLink TwoToOne1 = new OtoOLink(nicRouter21, nicRouter11);
		OtoOLink OneoneToThree1 = new OtoOLink(nicRouter113, nicRouter331);
		OtoOLink ThreethreeToOne1 = new OtoOLink(nicRouter331, nicRouter113);
		OtoOLink TwoTwoToThree2 = new OtoOLink(nicRouter223, nicRouter332);
		OtoOLink ThreethreeTotwo2 = new OtoOLink(nicRouter332, nicRouter223);
		
		//Protection Links
		OtoOLink OneToTwo2 = new OtoOLink(nicRouter12, nicRouter22);
		OtoOLink TwoToOne2 = new OtoOLink(nicRouter22, nicRouter12);
		OtoOLink OneToThree1 = new OtoOLink(nicRouter13, nicRouter31);
		OtoOLink ThreeToOne1 = new OtoOLink(nicRouter31, nicRouter13);
		OtoOLink TwoToThree2 = new OtoOLink(nicRouter23, nicRouter32);
		OtoOLink ThreeToTwo2 = new OtoOLink(nicRouter32, nicRouter23);
		
		//Assign Protection and Working NIC
		nicRouter11.setIsWorking(nicRouter12); // 11 is working
		nicRouter12.setIsProtection(nicRouter11); // 12 is protection
		
		nicRouter21.setIsWorking(nicRouter22); // 21 is working
		nicRouter22.setIsProtection(nicRouter21); // 22 is protection
		
		nicRouter113.setIsWorking(nicRouter13); // 113 is working
		nicRouter13.setIsProtection(nicRouter113); // 13 is protection
		
		nicRouter331.setIsWorking(nicRouter31); // 331 is working
		nicRouter31.setIsProtection(nicRouter331); // 31 is protection
		
		nicRouter332.setIsWorking(nicRouter32); // 332 is working
		nicRouter32.setIsProtection(nicRouter332); // 32 is protection
		
		nicRouter223.setIsWorking(nicRouter23); // 223 is working
		nicRouter23.setIsProtection(nicRouter223); // 23 is protection
		
		
		//Preferred routes for each router.
		// Router 1 to router 2
		ArrayList<Integer> r1Tor2 = new ArrayList<Integer>();
				
		r1Tor2.add(0,11); //working
		r1Tor2.add(1,12); //protection
		r1Tor2.add(2,13); //protection
		r1Tor2.add(3,113); //working
		router1.addDestinationHopCount(1490, r1Tor2);
		
		// Router 1 to router 3
		ArrayList<Integer> r1Tor3 = new ArrayList<Integer>();
		
		r1Tor3.add(0,11); //working
		r1Tor3.add(1,12); //protection
		r1Tor3.add(2,13); //protection
		r1Tor3.add(3,113); //working
		router1.addDestinationHopCount(1550, r1Tor3);
		
		// Router 2 to router 1
		ArrayList<Integer> r2Tor1 = new ArrayList<Integer>();
		
		r2Tor1.add(0,21); //working
		r2Tor1.add(1,22); //protection
		r2Tor1.add(2,23); //protection
		r2Tor1.add(3,223); //working
		router2.addDestinationHopCount(1310, r2Tor1);
		
		// Router 2 to router 3
		ArrayList<Integer> r2Tor3 = new ArrayList<Integer>();
		
		r2Tor3.add(0,21); //working
		r2Tor3.add(1,22); //protection
		r2Tor3.add(2,23); //protection
		r2Tor3.add(3,223); //working
		router2.addDestinationHopCount(1550, r2Tor3);
		
		// Router 3 to router 1
		ArrayList<Integer> r3Tor1 = new ArrayList<Integer>();
		
		r3Tor1.add(0,332); //working
		r3Tor1.add(1,32); //protection
		r3Tor1.add(2,331); //protection
		r3Tor1.add(3,31); //working
		router3.addDestinationHopCount(1310, r3Tor1);
		
		// Router 3 to router 2
		ArrayList<Integer> r3Tor2 = new ArrayList<Integer>();
				
		r3Tor2.add(0,332); //working
		r3Tor2.add(1,32); //protection
		r3Tor2.add(2,331); //protection
		r3Tor2.add(3,31); //working
		router3.addDestinationHopCount(1490, r3Tor2);
		
		// Sent a router across network from 00:11:22 - Case 1
		//router1.source(new SONETFrame(new SPE(0)), 1490); // r1 to r2
				
		//Case2
		OneToTwo1.cutLink();
		TwoToOne1.cutLink();
		TwoTwoToThree2.cutLink();
		ThreethreeTotwo2.cutLink();
		router1.source(new SONETFrame(new SPE(0)), 1490);
			}
	
	public static void main(String args[]){
		q2c go = new q2c();
		go.twoRings();
	}
}
