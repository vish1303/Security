import DataTypes.SONETFrame;
import DataTypes.SPE;
import NetworkElements.OpticalNICTA;
import NetworkElements.OtoOLink;
import NetworkElements.SONETRouter;


public class q2a {
	public void ring(){
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
		//OpticalNICTA nicRouter12 = new OpticalNICTA(router1);
		//nicRouter12.setID(12);
		OpticalNICTA nicRouter13 = new OpticalNICTA(router1);
		nicRouter13.setID(13);
		
		OpticalNICTA nicRouter21 = new OpticalNICTA(router2);
		nicRouter21.setID(21);
		//OpticalNICTA nicRouter22 = new OpticalNICTA(router2);
		//nicRouter22.setID(22);
		OpticalNICTA nicRouter23 = new OpticalNICTA(router2);
		nicRouter23.setID(23);
		
		//OpticalNICTA nicRouter33 = new OpticalNICTA(router3);
		//nicRouter11.setID(33);
		OpticalNICTA nicRouter31 = new OpticalNICTA(router3);
		nicRouter31.setID(31);
		OpticalNICTA nicRouter32 = new OpticalNICTA(router3);
		nicRouter32.setID(32);
		
		// Create two-uni directional links between the routers
		OtoOLink OneToTwo1 = new OtoOLink(nicRouter11, nicRouter21);
		OtoOLink TwoToOne1 = new OtoOLink(nicRouter21, nicRouter11);
		//OtoOLink OneToTwo2 = new OtoOLink(nicRouter12, nicRouter22);
		//OtoOLink TwoToOne2 = new OtoOLink(nicRouter22, nicRouter12);
		OtoOLink OneToThree1 = new OtoOLink(nicRouter13, nicRouter31);
		OtoOLink ThreeToOne1 = new OtoOLink(nicRouter31, nicRouter13);
		OtoOLink TwoToThree2 = new OtoOLink(nicRouter23, nicRouter32);
		OtoOLink ThreeToTwo2 = new OtoOLink(nicRouter32, nicRouter23);
		/*
		 * Sent a frame on the network
		 */
		router1.source(new SONETFrame(new SPE(0)), 1490);
		//router1.source(new SONETFrame(new SPE(0)), 1310); 
		//router1.source(new SONETFrame(new SPE(0)), 1550);
		//router1.source(new SONETFrame(new SPE(0)), 4343);
	}
	
	public static void main(String args[]){
		q2a go = new q2a();
		go.ring();
	}
}
