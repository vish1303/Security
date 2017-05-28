package NetworkElements;

import DataTypes.*;

public interface IPConsumer {
	/**
	 * receives a packet from the NIC
	 * @param packet the packet received
	 * @param nic the nic the packet was received on
	 */
	public void receivePacket(IPPacket packet, IPNIC nic);
	
	/**
	 * adds a nic to the consumer 
	 * @param nic the nic to be added
	 */
	public void addNIC(IPNIC nic);
}
