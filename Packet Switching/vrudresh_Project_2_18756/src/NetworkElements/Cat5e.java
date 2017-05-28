package NetworkElements;

import DataTypes.IPPacket;

public class Cat5e {
	private IPNIC computerNIC=null, routerNIC=null;
	private Boolean trace=false;
	
	/**
	 * The default constructor for a Cat5e cable
	 * @param computerNIC
	 * @param routerNIC
	 */
	public Cat5e(IPNIC computerNIC, IPNIC routerNIC){
		if(computerNIC==null)
			System.err.println("(Cat5e) Error: The computer NIC is null");
		if(routerNIC==null)
			System.err.println("(Cat5e) Error: The router NIC is null");
		
		this.computerNIC = computerNIC;
		this.computerNIC.connectCat5e(this);
		this.routerNIC = routerNIC;
		this.routerNIC.connectCat5e(this);
	}
	
	/**
	 * Sends a packet from one end of the link to the other
	 * @param packet
	 * @param nic
	 */
	public void sendIPPacket(IPPacket packet, IPNIC nic){
		if(this.computerNIC.equals(nic)){
			if(trace)
				System.out.println("(Cat5e) Trace: sending packet from computer to router");
			
			this.routerNIC.receivePacket(packet);
		}
		else if(this.routerNIC.equals(nic)){
			if(trace)
				System.out.println("(Cat5e) Trace: sending packet from router to computer");
			
			this.computerNIC.receivePacket(packet);
		}
		else
			System.err.println("(Cat5e) Error: You are trying to send a packet down a link that you are not connected to");
	}
}
