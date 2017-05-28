#ifndef CLICK_STATEFULFIREWALL_HH
#define CLICK_STATEFULFIREWALL_HH
#include <click/element.hh>
#include <clicknet/ip.h>
#include <clicknet/tcp.h>
#include <clicknet/udp.h>
#include <map>
#include <iostream>
#include <vector>
#include <arpa/inet.h> // for marshalling
#include <string>
#include <fstream>

CLICK_DECLS

using namespace std;

/* Handshake status */
#define SYN 0
#define SYNACK 1
#define HS_DONE 2

class Connection{
private:
	String sourceip;
    String destip;
    int sourceport;
    int destport;
    int proto;
    unsigned long sourceseq;
    unsigned long destseq;
    int handshake_stat;
    bool isfw; //true if forward connection. false if reverse connection.
public:
	Connection(String s, String d, int sp, int dp, unsigned long seq_s, unsigned long seq_d, int pr, bool fwdflag)
	{
		sourceip = s;
		destip = d;
		sourceport = sp;
		destport = dp;
		sourceseq = seq_s;
		destseq = seq_d;
		proto = pr;
		isfw = fwdflag;

	}

	Connection(String s, String d, int sp, int dp, int pr, bool fwdflag)
	{
            sourceip = s;
            destip = d;
            sourceport = sp;
            destport = dp;
            proto = pr;
	    isfw = fwdflag;
	}

	Connection()
	{
	}
	~Connection()
	{

	}

    Connection(const Connection & RaConn)
    {
            this->sourceip = RaConn.sourceip;
            this->destip = RaConn.destip;
            this->sourceport = RaConn.sourceport;
            this->destport = RaConn.destport;
            this->proto = RaConn.proto;
            this->isfw = RaConn.isfw;

    }

	/* Can be useful for debugging*/
	void print() const
	{
		cout<<"Source IP: "<<sourceip.c_str()<<"\n";
		cout<<"Source Port: "<<sourceport<<"\n";
		cout<<"Destination IP: "<<destip.c_str()<<"\n";
		cout<<"Destination Port: "<<destport<<"\n";
		cout<<"Protocol: "<<proto<<"\n";
//		cout<<"Action: "<<action<<"\n";
	}

	/* Reverse the connection */
	void revConn() {
		int revport;
		String revIP;

	//SourceIP -> DestinationIP and vice versa
		revIP = this->sourceip;
		this->sourceip = this->destip;
		this->destip = revIP;

	//Source Port -> Destination Port and vice versa
		revport = this->sourceport;
		this->sourceport = this->destport;
		this->destport = revport;
}
	/* Overlaod == operator to check if two Connection objects are equal.
	 * You may or may not want to ignore the isfw flag for comparison depending on your implementation.
	 * Return true if equal. false otherwise. */
    bool operator==(const Connection &other) const
    {

	//Check if the source, destination ports and protocol number matches
        if(this->sourceport == other.sourceport && this->destport == other.destport && this->proto == other.proto){ return true; }

	//Check if Source IP matches
	if(strcmp(this->sourceip.c_str(), other.sourceip.c_str()) != 0){ return false; }

	//Check if Destination IP matches
	if(strcmp(this->destip.c_str(), other.destip.c_str()) !=0){ return false;}

	return false;
    }

    /*Compare two connections to determine the sequence in map.*/
    int compare(const Connection other) const
    {
	struct sockaddr_in this_seq_sourceip, this_seq_destip, other_seq_sourceip, other_seq_destip;
	unsigned this_sourceip, this_destip, other_sourceip, other_destip;

        inet_aton(this->sourceip.c_str(), &this_seq_sourceip.sin_addr);
	inet_aton(other.sourceip.c_str(), &other_seq_sourceip.sin_addr);
        inet_aton(this->destip.c_str(), &this_seq_destip.sin_addr);
        inet_aton(other.destip.c_str(), &other_seq_destip.sin_addr);

        this_sourceip = htonl(this_seq_sourceip.sin_addr.s_addr);
	other_sourceip = htonl(other_seq_sourceip.sin_addr.s_addr);
        this_destip = htonl(this_seq_destip.sin_addr.s_addr);
        other_destip = htonl(other_seq_destip.sin_addr.s_addr);

    	if(this->sourceport < other.sourceport) return -1;
        else if(this->sourceport > other.sourceport) return 1;
        
    	if(this->destport < other.destport) return -1;
        else if(this->destport > other.destport) return 1;

    	if(this_sourceip < other_sourceip) return -1;
        else if(this_sourceip > other_sourceip) return 1;

    	if(this_destip < other_destip) return -1;
        else if(this_destip > other_destip) return 1;
    }


    unsigned long get_sourceseq() 
    {
        return sourceseq;                      
    }

    unsigned long get_destseq()
    {
        return destseq;                      
    }

    void set_sourceseq( unsigned long seq_s )
    {
        sourceseq = seq_s;                     
    }

    void set_destseq( unsigned long seq_d )
    {
        destseq = seq_d;                      
    }

    int get_handshake_stat()
    {
        return handshake_stat;             
    }

    /* Update the status of the handshake */
    void update_handshake_stat()
    {
        //Add your implementation here.
    }

	/* Return value of isfw*/
	bool is_forward() { return this->isfw; }
};

class Policy{
private:
	String sourceip;
	String destip;
	int sourceport;
	int destport;
	int proto;
	int action;
public:
	Policy(String s, String d, int sp, int dp, int p, int act)
	{
	   	sourceip = s;
           	destip = d;
        	sourceport = sp;
        	destport = dp;
        	proto = p;
        	action = act;
	}
	~Policy()
	{

	}
	/* Return a Connection object representing policy */
	Connection getConnection()
	{
		Connection policy_conn(sourceip, destip, sourceport, destport, proto, action);
		return policy_conn;
	}
	/* Return action for this Policy */
	int getAction() { return this->action; }
};

struct cmp_connection
{
   bool operator()(Connection const a, Connection const b)
   {
      return a.compare(b) < 0;
   }
};

class StatefulFirewall : public Element {
private:
	std::map<Connection,int, cmp_connection> Connections; //Map of connections to their actions.
	std::vector<Policy> list_of_policies;
public:
	StatefulFirewall()
	{
	}

    ~StatefulFirewall()
	{
	}

    /* Take the configuration paramenters as input corresponding to
     * POLICYFILE and DEFAULT where
     * POLICYFILE : Path of policy file
     * DEFAULT : Default action (0/1)
     *
     * Hint: Refer to configure methods in other elemsnts.*/
    int configure(Vector<String> &conf, ErrorHandler *errh);

    const char *class_name() const		{ return "StatefulFirewall"; }
    const char *port_count() const		{ return "1/2"; }
    const char *processing() const		{ return PUSH; }
    // this element does not need AlignmentInfo; override Classifier's "A" flag
    const char *flags() const			{ return ""; }

    /* return true if Packet represents a new connection
     * i.e., check if the connection exists in the map.
     * You can also check the SYN flag in the header to be sure.
     * else return false.
     * Hint: Check the connection ID database.
     */
    bool check_if_new_connection(const Packet *p);

    /*Check if the packet represent Connection reset
     * i.e., if the RST flag is set in the header.
     * Return true if connection reset
     * else return false.*/
    bool check_if_connection_reset(const Packet *p);

    /* Add a new connection to the map along with its action.*/
    void add_connection(Connection &c, int action);

    /* Delete the connection from map*/
    void delete_connection(Connection &c);

    /* Create a new connection object for Packet.
     * Make sure you canonicalize the source and destination ip address and port number.
     * i.e, make the source less than the destination and
     * update isfw to false if you have to swap source and destination.
     * return NULL on error. */
    Connection get_canonicalized_connection(const Packet *p);

    /* Read policy from a config file whose path is passed as parameter.
     * Update the policy database.
     * Policy config file structure would be space separated list of
     * <source_ip source_port destination_ip destination_port protocol action>
     * Add Policy objects to the list_of_policies
     * */
    int read_policy_config(String str);

    int get_policy_action(Connection &c);

    /* Convert the integer ip address to string in dotted format.
     * Store the string in s.
     *
     * Hint: ntohl could be useful.*/
    void dotted_addr(const uint32_t *addr, char *s);


   /* Check if Packet belongs to new connection.
    * If new connection, apply the policy on this packet
    * and add the result to the connection map.
    * Else return the action in map.
    * If Packet indicates connection reset,
    * delete the connection from connection map.
    *
    * Return 1 if packet is allowed to pass
    * Return 0 if packet is to be discarded
    */
    int filter_packet(const Packet *p);

    /* Push valid traffic on port 1
    * Push discarded traffic on port 0*/
    void push(int port, Packet *);

    /*The default action configured for the firewall.*/
    int DEFAULTACTION;
};

CLICK_ENDDECLS
#endif
