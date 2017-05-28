package NetworkElements;

import DataTypes.IPPacket;

public class Computer implements IPConsumer{
	private IPNIC nic=null;
	private Boolean trace=true;
	
	/**
	 * The default constructor for a computer
	 */
	public Computer(){}
	
	/**
	 * Sinks a packet to the console
	 * @param packet the packet to be outputted
	 */
	public void sinkIPPacket(IPPacket packet){
		System.out.println("(Computer): Received a packet " + packet);
	}
	
	/**
	 * adds a nic to this computer
	 * @param nic the nic to be added (only one nic per computer)
	 */
	public void addNIC(IPNIC nic){
		this.nic = nic;
	}
	
	/**
	 * Sends a packet from this computer to another ip address
	 * @param dest the destination address of the packet
	 * @param size the size of the packet
	 */
	public void sendPacket(String dest, int size){
		if(this.nic==null)
			System.err.println("The computer you are sending from does not have a NIC!");
		
		if(trace)
			System.out.println("(Computer) Trace: sending packet from computer");
		nic.sendIPPacket(new IPPacket(this.nic.getHostAddress(), dest, size));
	}
	
	/**
	 * receives a packet from the NIC
	 * @param packet the packet received
	 * @param nic the nic the packet was received on
	 */
	public void receivePacket(IPPacket packet, IPNIC nic){
		this.sinkIPPacket(packet);
	}
}
