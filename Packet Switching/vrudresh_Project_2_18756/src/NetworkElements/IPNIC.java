package NetworkElements;

import DataTypes.*;
import java.net.*;

public class IPNIC {
	private IPConsumer parent;
	private Inet4Address IPAddress;
	private Cat5e link=null;
	private Boolean trace=false;

	/**
	 * Default constructor for an IP NIC
	 * @param IPAddress this IP address of the nic
	 * @param parent the parent of this nic (where the nic is)
	 */
	public IPNIC(String IPAddress, IPConsumer parent){
		this.parent = parent;
		this.parent.addNIC(this);
		
		try{
			this.IPAddress = (Inet4Address) InetAddress.getByName(IPAddress);
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}
	
	/**
	 * returns the parent of this nic
	 * @return the parent of this nic
	 */
	public IPConsumer getParent(){
		return this.parent;
	}
	
	/**
	 * Connects a cat5e cable to this nic
	 * @param link the cat5e cable that is connected
	 */
	public void connectCat5e(Cat5e link){
		this.link = link;
	}
	
	/**
	 * Tries to send a packet down the link connected to this nic
	 * @param packet the packet to be sent
	 */
	public void sendIPPacket(IPPacket packet){
		if(this.link == null)
			System.err.println("(IPNIC) Error: The nic is not conencted to anything");
		else{
			if(trace)
				System.out.println("(IPNIC) Trace: Sending packet");
			this.link.sendIPPacket(packet, this);
		}
	}
	
	/**
	 * called when a packet is received from the link this nic is connected to
	 * @param packet the packet received
	 */
	public void receivePacket(IPPacket packet){
		if(trace)
			System.out.println("(IPNIC) Trace: Received packet");
		
		this.parent.receivePacket(packet, this);
	}
	
	/**
	 * returns the host address of this nic
	 * @return the host address of this nic
	 */
	public String getHostAddress(){
		return this.IPAddress.getHostAddress();
	}
	
	/**
	 * returns the IP address object of this nic
	 * @return the IP address object of this nic
	 */
	public Inet4Address getIPAddress(){
		return this.IPAddress;
	}
}
