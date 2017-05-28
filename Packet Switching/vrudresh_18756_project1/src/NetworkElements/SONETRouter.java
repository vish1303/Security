package NetworkElements;

import DataTypes.*;
import java.util.*;

public class SONETRouter extends SONETRouterTA{
	/**
	 * Construct a new SONET router with a given address
	 * @param	address the address of the new SONET router
	 */
	public SONETRouter(String address){
		super(address);
	}
	
	/**
	 * This method processes a frame when it is received from any location (including being created on this router
	 * from the source method). It either drops the frame from the line, or forwards it around the ring
	 * @param	frame the SONET frame to be processed
	 * @param	wavelength the wavelength the frame was received on
	 * @param	nic the NIC the frame was received on
	 */
	public void receiveFrame(SONETFrame frame, int wavelength, OpticalNICTA nic){

		//tests for If a frame is on the routers drop frequency.
	if (this.dropFrequency.contains(wavelength)){
		//Tests for if a frame is  also the routers destination frequency
		if(wavelength==this.destinationFrequencies.get(getAddress())){
			//Frame is forwarded to the sink
			if (nic.getWorkingNIC()==null)
			{this.sink(frame, wavelength);} 
			else { System.out.println("Take frame off the line"); }
		}
		else {
			System.out.println("Do nothing");
		}
	}
	else {
		//frame is forwarded on all interfaces, except the interface the frame was received on
		sendRingFrame(frame, wavelength, nic);
	}
	}
	
	
	/**
	 * Sends a frame out onto the ring that this SONET router is joined to
	 * @param	frame the frame to be sent
	 * @param	wavelength the wavelength to send the frame on
	 * @param	nic the wavelength this frame originally came from (as we don't want to send it back to the sender)
	 */
	public void sendRingFrame(SONETFrame frame, int wavelength, OpticalNICTA nic){
			
		ArrayList<OpticalNICTA> Pro_NICs = new ArrayList<OpticalNICTA>();
		// Checking if the frame’s frequency matches with the router’s destination frequency
		if(!(this.destinationFrequencies.containsValue(wavelength))){
			//Frame is forwarded to the sink
			System.out.println("Do Nothing");
		}
		else {
			
		// Loop through the interfaces sending the frame on interfaces that are on the ring
		// except the one it was received on. Basically what UPSR does
		for(OpticalNICTA NIC:NICs)
		{
			//Code for question 2.d, , check for working link and send frame if link is fine else do the same for protection in the else part
			if(NIC.getIsOnRing() && !NIC.equals(nic) && ((NIC.getWorkingNIC()== null)) && !NIC.getHasError()) {
				System.out.println("id "+ NIC.getID() + " Working");
			SPE a = frame.getSPE();
			SPE b = a.clone();
			int del = a.getDealy();
			b.addDelay(del);
			//Creating new cloned frame
			SONETFrame frame_clone = new SONETFrame(b);
			NIC.sendFrame(frame_clone, wavelength);
			
			}
			else {
				
			if( NIC.getIsOnRing() && !NIC.equals(nic) && !NIC.equals(NIC)&& (NIC.getProtectionNIC() == null) && !NIC.getHasError()) {
					System.out.println("id "+ NIC.getID()+ " Protection");
				SPE c = frame.getSPE();
				SPE d = c.clone();
				int dela = c.getDealy();
				d.addDelay(dela);
				//Creating new cloned frame
				SONETFrame frame_clone2 = new SONETFrame(d);
				OpticalNICTA pro_nic = NIC.getWorkingNIC();
				NIC.sendFrame(frame_clone2, wavelength);
				}
	     }
		} 
	}
}
	
}


