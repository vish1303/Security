package DataTypes;

import sun.net.NetworkServer;

public class SPE extends SPETA{
	/**
	 * Creates a new SPE, with a virtual pointer set
	 * @param	VTPointer the VT number to be set for this SPE
	 */
	public SPE(int VTPointer){
		super(VTPointer);
	}
	
	/**
	 * Increases the delay that this SPE has encountered during it's travel
	 * @param	delay the additional delay to be added
	 */
	public void addDelay(int delay){
		super.delay +=delay;
	}
	
	/**
	 * Returns a clone of this SPE object
	 */
	public SPE clone(){ 
		System.out.println("Calling clone\n");
		SPE a = new SPE(this.getVTPointer());
	    return a; }

	public static SPE getSPE() {
		// TODO Auto-generated method stub
		return null;
	}
}
