package NetworkElements;

import java.util.*;
import java.net.*;
import DataTypes.*;

public class IPRouter implements IPConsumer{
	private ArrayList<IPNIC> nics = new ArrayList<IPNIC>();
	private HashMap<Inet4Address, IPNIC> forwardingTable = new HashMap<Inet4Address, IPNIC>();
	private int time = 0;
	private Boolean fifo=false, rr=false, wrr=false, wfq=false, routeEntirePacket=true;
	private HashMap<IPNIC, FIFOQueue> inputQueues = new HashMap<IPNIC, FIFOQueue>();
	
	private int lastNicServiced=-1, weightFulfilled=1;
	// remembering the queue rather than the interface number is useful for wfq
	private FIFOQueue lastServicedQueue = null;
	private double virtualTime = 0.0;
	private FIFOQueue fifoqueue = new FIFOQueue();
	private int NIC_route, i=1;
	public double rt=0;
	public double wt=0;
	public double[] finish_time = new double[100];
//	public FIFOQueue rem_queue = null;
	public boolean b =true;
	public double[] finish_time2 = new double[100];
	
	/**
	 * The default constructor of a router
	 */
	public IPRouter(){
		
	}
	/**
	 * Calculates the maximum of two numbers
	 * @param values to be compared
	 * @return returns the larger number
	 */
	
	public double max(double a, double b){
		if (a>b) return a;
		else return b;
	}

	/**
	 * Sorting the packets as per their finish times.
	 * @return sorted list
	 */
	public void sort() {
		
	int i, n = finish_time.length;
	double temp;
	for (i=1;i<n;i++)
		for(int k=i;k>1 & finish_time[k]<finish_time[k-1];k--) {
			temp = finish_time[k];
			finish_time[k]=finish_time[k-1];
			finish_time[k-1]=temp;
			}

	}
	
	/**
	 * Inserting the packets as per their finish times.
	 * @return inserted list
	 */
	public void ins() {
		int i=0;
		
		for(Iterator<FIFOQueue> queues = this.inputQueues.values().iterator(); queues.hasNext();){
	
			FIFOQueue queue = queues.next();
		//	int size = queue.packets.size();
			//while(size!=0) {
		
			if(queue.peek()!=null){
			finish_time[i] = queue.peek().getFinishTime();
			i++;
		//	size--;
			}
		  //}
		}
		
		//sort
		sort();
	}
	

	/**
	 * adds a forwarding address in the forwarding table
	 * @param destAddress the address of the destination
	 * @param nic the nic the packet should be sent on if the destination address matches
	 */
	public void addForwardingAddress(Inet4Address destAddress, IPNIC nic){
		forwardingTable.put(destAddress, nic);
	}
	
	/**
	 * receives a packet from the NIC
	 * @param packet the packet received
	 * @param nic the nic the packet was received on
	 */
	public void receivePacket(IPPacket packet, IPNIC nic){
		
		//add packets to the nic queue

		FIFOQueue nic_queue = this.inputQueues.get(nic);
		nic_queue.offer(packet);

		// If wfq set the expected finish time
		if(this.wfq){
		
			if(nic_queue.secondLastPeek().getFinishTime()==0) {
				double pac_fin = max(nic_queue.keep_track, rt);
				double fin_time = (double)packet.getSize()/(double)nic_queue.getWeight();
				double sum = pac_fin+fin_time;
				packet.setFinishTime(sum);
				System.out.println("est time " + sum);
				ins();
				}
			else { 
		double pac_fin = max(nic_queue.secondLastPeek().getFinishTime(), rt);
		double fin_time = (double)packet.getSize()/(double)nic_queue.getWeight();
		double sum = pac_fin+fin_time;
		packet.setFinishTime(sum);
		System.out.println("est time " + sum);
		ins();
		}
	}
	}
	
	public void forwardPacket(IPPacket packet){
		forwardingTable.get(packet.getDest()).sendIPPacket(packet);
	}
	
	public void routeBit(){
		/*
		 *  FIFO scheduler
		 */
		if(this.fifo) this.fifo();
			
		
		/*
		 *  RR scheduler
		 */
		if(this.rr) this.rr();
			
		
		/*
		 *  WRR scheduler
		 */
		if(this.wrr) this.wrr();
			
		
		/*
		 * WFQ scheduler
		 */
		if(this.wfq) this.wfq();
	}
	
	/**
	 * Perform FIFO scheduler on the queue
	 */
	private void fifo(){
		int packet_size=0;
		IPPacket head = null;
		fifoqueue.routeBit();
		head = fifoqueue.peek();
		if(head!=null) {
		packet_size = head.getSize();
		if(packet_size == fifoqueue.getBitsRoutedSinceLastPacketSent()){
			this.forwardPacket(head);
			fifoqueue.remove();
		}
		}	
		} 
		

	
	/**
	 * Perform round robin on the queue
	 */
	private void rr(){
		
		if(routeEntirePacket == false){
		int packet_size = 0; 
		IPPacket head = null; 
		FIFOQueue nic_queue = null;
		int size = nics.size();
		boolean a = true;
		//get NIC's corresponding queue
		while(a) {
			IPNIC NIC = nics.get(NIC_route);
			nic_queue = this.inputQueues.get(NIC);
			head = nic_queue.peek();
			if(head!=null) {	
			packet_size = head.getSize();
			nic_queue.routeBit();
			a = false;
			NIC_route+=1;
			if (packet_size == nic_queue.getBitsRoutedSinceLastPacketSent()) {
				this.forwardPacket(head);
				nic_queue.remove();
			}
			}
			else {
			NIC_route+=1;
				}
			if(NIC_route==size) {
				NIC_route=NIC_route%size;
			}
		}
		}
		
	else {
		int packet_size = 0; 
		IPPacket head = null; 
		FIFOQueue nic_queue = null;
		int size = nics.size();
		boolean a = true;
		//get NIC's corresponding queue
		while(a) {
			IPNIC NIC = nics.get(NIC_route);
			nic_queue = this.inputQueues.get(NIC);
			head = nic_queue.peek();
			if(head!=null) {	
			packet_size = head.getSize();
			nic_queue.routeBit();
			a = false;
			if (packet_size == nic_queue.getBitsRoutedSinceLastPacketSent()) {
			this.forwardPacket(head);
			nic_queue.remove();
			NIC_route+=1;
			}
			}
			else {
			NIC_route+=1;
				}
			if(NIC_route==size) {
				NIC_route=NIC_route%size;
			}
		}	
		}
	}
	
	
	
	/**
	 * Perform weighted round robin on the queue
	 */
	private void wrr(){
		
		if(routeEntirePacket == false){
			int packet_size = 0; 
			IPPacket head = null; 
			FIFOQueue nic_queue = null;
			int size = nics.size();
			boolean a = true;
			int weight = 0;
			
			//get NIC's corresponding queue
			while(a) {
				IPNIC NIC = nics.get(NIC_route);
				nic_queue = this.inputQueues.get(NIC);
				head = nic_queue.peek();
				
				if(head!=null) {
				weight = nic_queue.getWeight();	
				packet_size = head.getSize();
				nic_queue.routeBit();
				a = false;
				if(weight == i) { weight=0;} else {i++;}
				if(weight==0) 	{	NIC_route+=1;i=1;}
				if (packet_size==nic_queue.getBitsRoutedSinceLastPacketSent()) {
					this.forwardPacket(head);
					nic_queue.remove();
				}
				}
				else {
				NIC_route+=1;
					}
				if(NIC_route==size) {
					NIC_route=NIC_route%size;
				}
			}
			
		}
					
		else {
			int packet_size = 0; 
			IPPacket head = null; 
			FIFOQueue nic_queue = null;
			int size = nics.size();
			boolean a = true;
			int weight = 0;
			
			//get NIC's corresponding queue
			while(a) {
				IPNIC NIC = nics.get(NIC_route);
				nic_queue = this.inputQueues.get(NIC);
				head = nic_queue.peek();
				
				if(head!=null) {
				weight = nic_queue.getWeight();	
				packet_size = head.getSize();
				nic_queue.routeBit();
				a = false;
				if(weight == i) { weight=0;} else {i++;}
				//System.out.println("weight: " + weight + "\n" + "i: "+i+"\n"+"bits routed: "+nic_queue.getBitsRoutedSinceLastPacketSent());
				if (packet_size==nic_queue.getBitsRoutedSinceLastPacketSent()) {
					this.forwardPacket(head);
					nic_queue.remove();
					if(weight==0){ 	
						NIC_route+=1;
						i=0;
					}
				}
				
				}
				else {
				NIC_route+=1;
					}
				if(NIC_route==size) {
					NIC_route=NIC_route%size;
				}
			}
		}
	}
		
		/**
	 * Perform weighted fair queuing on the queue
	 */
	private void wfq(){

		int packet_size = 0; 
		IPPacket head = null, head1=null; 
		boolean a = true;
		int i=0, d=0;
		int c;
		double minFinish = 200000;
		FIFOQueue rem_queue=null;
		
		//get NIC's corresponding queue	
					
		for(Iterator<FIFOQueue> queues = this.inputQueues.values().iterator(); queues.hasNext();){
				FIFOQueue some_queue = queues.next();
					head = some_queue.peek();
					if(head==null){ continue;}
					if(minFinish > head.getFinishTime()){
						rem_queue = some_queue;
					}
			}
		
		
		
	
		
		
		
		
		while(a && rem_queue!=null){
			
				head1=rem_queue.peek();
				if(head1!=null) {
					packet_size = head1.getSize();
					rem_queue.routeBit();
				if (packet_size==rem_queue.getBitsRoutedSinceLastPacketSent()) {
							rem_queue.keep_track=head1.getFinishTime();
							this.forwardPacket(head1);
							rem_queue.remove();
							//rem_queue=null;
							a = false;
							ins();
							}
				else break;
					}
			
					}
		}
		
		
	/**
	 * adds a nic to the consumer 
	 * @param nic the nic to be added
	 */
	public void addNIC(IPNIC nic){
		this.nics.add(nic);
	}
	
	/**
	 * sets the weight of queues, used when a weighted algorithm is used.
	 * Example
	 * Nic A = 1
	 * Nic B = 4
	 * 
	 * For every 5 bits of service, A would get one, B would get 4.
	 * @param nic the nic queue to set the weight of
	 * @param weight the weight of the queue
	 */
	public void setQueueWeight(IPNIC nic, int weight){
		if(this.inputQueues.containsKey(nic))
			this.inputQueues.get(nic).setWeight(weight);
		
		else System.err.println("(IPRouter) Error: The given NIC does not have a queue associated with it");
	}
	
	/**
	 * moves time forward 1 millisecond
	 */
	public void tock(){
		this.time+=1;
		
		// Add 1 delay to all packets in queues
		ArrayList<FIFOQueue> delayedQueues = new ArrayList<FIFOQueue>();
		for(Iterator<FIFOQueue> queues = this.inputQueues.values().iterator(); queues.hasNext();){
			FIFOQueue queue = queues.next();
			if(!delayedQueues.contains(queue)){
				delayedQueues.add(queue);
				queue.tock();
			}
		}
		
		// calculate the new virtual time for the next round
		if(this.wfq){
			
			for(Iterator<FIFOQueue> queues = this.inputQueues.values().iterator(); queues.hasNext();){
				FIFOQueue queue = queues.next();
				if(queue.peek()!=null)
				wt += queue.getWeight();
			}
		
				rt = (rt*wt + 1)/(wt);
				wt=0;
		}
		
		//route bit for this round
		this.routeBit();
	}
	
	/**
	 * set the router to use FIFO service
	 */
	public void setIsFIFO(){
		this.fifo = true;
		this.rr = false;
		this.wrr = false;
		this.wfq = false;
		
		// Setup router for FIFO under here
		
		this.setRouteEntirePacket(false);
		for (IPNIC NIC: nics){
			this.inputQueues.put(NIC, fifoqueue);
			}
	}
	
	/**
	 * set the router to use Round Robin service
	 */
	public void setIsRoundRobin(){
		this.fifo = false;
		this.rr = true;
		this.wrr = false;
		this.wfq = false;
		
		// Setup router for Round Robin under here
		//this.setRouteEntirePacket(false);
		for (IPNIC NIC: nics){
			this.inputQueues.put(NIC, new FIFOQueue());
			}
	}
	
	/**
	 * sets the router to use weighted round robin service
	 */
	public void setIsWeightedRoundRobin(){
		this.fifo = false;
		this.rr = false;
		this.wrr = true;
		this.wfq = false;
		
		// Setup router for Weighted Round Robin under here
		for (IPNIC NIC: nics){
			this.inputQueues.put(NIC, new FIFOQueue());
			}
	}
	
	/**
	 * sets the router to use weighted fair queuing
	 */
	public void setIsWeightedFairQueuing(){
		this.fifo = false;
		this.rr = false;
		this.wrr = false;
		this.wfq = true;
		
		// Setup router for Weighted Fair Queuing under here
		for (IPNIC NIC: nics){
			this.inputQueues.put(NIC, new FIFOQueue());
			}
	}
	
	/**
	 * sets if the router should route bit-by-bit, or entire packets at a time
	 * @param	routeEntirePacket if the entire packet should be routed
	 */
	public void setRouteEntirePacket(Boolean routeEntirePacket){
		this.routeEntirePacket=routeEntirePacket;
	}
}
