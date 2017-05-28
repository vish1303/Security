package DataTypes;

import java.net.*;

public class IPPacket {
	private int size=0;
	private Inet4Address source=null, dest=null;
	private int delay=0;
	private double finishTime=0;
	
	/**
	 * The default constructor for a packet
	 * @param source the source ip address of this packet
	 * @param dest the destination ip address of this packet
	 * @param size the size of this packet (in bits)
	 */
	public IPPacket(String source, String dest, int size){
		try{
			this.source = (Inet4Address) InetAddress.getByName(source);
			this.dest = (Inet4Address) InetAddress.getByName(dest);
			this.size = size;
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}
	
	/**
	 * Returns the size of this packet
	 * @return the size of this packet (in bits)
	 */
	public int getSize(){
		return this.size;
	}
	
	/**
	 * Returns the source ip address of this packet
	 * @return the source ip address of this packet
	 */
	public Inet4Address getSource(){
		return this.source;
	}
	
	/**
	 * Returns the destination ip address of this packet
	 * @return the destination ip address of this packet
	 */
	public Inet4Address getDest(){
		return this.dest;
	}
	
	/**
	 * Adds delay to this packet
	 * @param delay the amount of delay this packet has experienced
	 */
	public void addDelay(int delay){
		this.delay +=delay;
	}
	
	/**
	 * Returns the delay this packet has experienced
	 * @return the total delay of this packet
	 */
	public int getDelay(){
		return this.delay;
	}
	
	/**
	 * Returns this packet as a String
	 * @return the string version of this packet
	 */
	public String toString(){
		return this.source.getHostAddress() + " > " + this.dest.getHostAddress() + " took " + this.getDelay() + " time"; 
	}
	
	/**
	 * Sets the expected finishTime of this packet
	 * @param finishTime the expected finish time of this packet
	 */
	public void setFinishTime(double finishTime){
		this.finishTime = finishTime;
	}
	
	/**
	 * returns the expected finish time
	 * @return the expected finish time
	 */
	public double getFinishTime(){
		return this.finishTime;
	}
}
