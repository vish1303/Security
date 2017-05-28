/*
 * statefulipfilter.{cc,hh} -- Stateful IP-packet filter
 * Author: Vishruta Rudresh
 * Andrew ID: vrudresh
 *
 */

#include <click/config.h>
#include <click/confparse.hh>
#include "statefulfirewall.hh"
#include <click/args.hh> 
#include <fstream>
#include <iostream>
#include <string>
#include <arpa/inet.h>
#include <clicknet/ip.h>
#include <clicknet/tcp.h>
#include <clicknet/udp.h>
#include <map>
#include <vector>
#include <string>
#include <stdio.h>
#include <sstream>

/* Add header files as required*/
CLICK_DECLS

using namespace std;

vector<Policy> policy_list;

/* Configure function */
int StatefulFirewall::configure(Vector<String> &conf, ErrorHandler *errh)
{
        String POLICYFILE;
	int DEFAULT = -1;

        // parse config file for POLICYFILE and DEFAULT values
        if(cp_va_kparse(conf, this, errh, "POLICYFILE", cpkP+cpkM, cpString, &POLICYFILE, "DEFAULT", cpkM, cpInteger, &DEFAULT, cpEnd) < 0) return -1;
        
        // set default policy action 
        DEFAULTACTION = DEFAULT;

	// read the policy configuration
        read_policy_config(POLICYFILE);
}

/* push: to add or drop packet decision function */
void StatefulFirewall::push(int port, Packet *p)
{ 
    	// filter packets: to add ot to drop
         if(filter_packet(p) == 1) 
		output(1).push(p); 
         else 
		output(0).push(p);    
}

/* add_connection: adds a connection to the maps of connections 
 * maintained by the firewall */
void StatefulFirewall::add_connection(Connection &c, int action)
{
        pair<map<Connection, int>::iterator,bool> test = Connections.insert(std::pair<Connection,int>(c, action));
	if (test.second == false) cout<<"Unable to add"<<"\n";
	
}

/*delete_connection: deletes a connection */
void StatefulFirewall::delete_connection(Connection &c)
{
        Connections.erase(c);
}

/* check_if_new_connection: checks if the connection is new,
 * if it is, extracts the ip header and inserts into the list 
 * of connections
 */
bool StatefulFirewall::check_if_new_connection(const Packet *p)
{

	Connection connection = get_canonicalized_connection(p);
  
  	map<Connection, int>::iterator con = Connections.find(connection);

  	if ((con == Connections.end()) && (p->tcp_header()->th_flags & TH_SYN))
		return true;
  	else
		return false;
}

/*check_if_connection_reset: checks if the connection is a recurring
 * connection
 */
bool StatefulFirewall::check_if_connection_reset(const Packet * p)
{ 

  	if ((p->tcp_header()->th_flags & TH_RST) || (p->tcp_header()->th_flags & TH_FIN))
		return true;
  	else
		return false;
}

/* read_policy_config: regads the policy configuration file
 */
int StatefulFirewall::read_policy_config(String policyfile){
    	string line;
    	char *s;
   	 int i;
    	string tokens[6];
    	ifstream myfile (policyfile.c_str());

    	if (myfile.is_open()){
		while (getline(myfile, line)){
	   		if (line[0] == '#')
				continue;
	   		else {
				stringstream ss(line);
				string s;
				i = 0;
				while (getline(ss, s, ' ')){
		  			tokens[i] = s;
		  			i++;
				}
				String sourceip = tokens[0].c_str();
				String destip = tokens[2].c_str();
				int sp = atoi(tokens[1].c_str());
				int dp = atoi(tokens[3].c_str());
				int proto = atoi(tokens[4].c_str());
				int action = atoi(tokens[5].c_str());

				Policy pol(sourceip, destip, sp, dp, proto, action);
				policy_list.push_back(pol);
	   		}
		}		
	}
    
	else {
		cout << "Error: File might not exist " << policyfile << endl;
        }  
    
    	return 0;  
}

/* filter_packet: filters the incoming packets based on the policy
 */
int StatefulFirewall::filter_packet(const Packet *p)
{
    String sourceip, destip;
    int sourceport, destport, proto;
    bool isfw;

    Connection recv_conn(get_canonicalized_connection(p));

    if(check_if_new_connection(p))
   {
      if(get_policy_action(recv_conn) == 1)
     {
     add_connection(recv_conn, 1);
      return 1;
     }
     else
    { 
     add_connection(recv_conn, 0);
     return 0;
     }
    }
     else
    {
    add_connection(recv_conn, Connections.find(recv_conn)->second);
	cout<<Connections.find(recv_conn)->second;
       return(Connections.find(recv_conn)->second);
     }
                               
    return DEFAULTACTION;
}

/* get_canonicalized_connection */
Connection StatefulFirewall::get_canonicalized_connection(const Packet * p)
{
    String sourceip, destip, temp;
    unsigned sourceport, destport, proto, sourceip_int, destip_int, temp_int;
    struct sockaddr_in str_sourceip, str_destip;
    bool isfw = 1;

    // IP parsing    
    sourceip = inet_ntoa(p->ip_header()->ip_src);
    destip = inet_ntoa(p->ip_header()->ip_dst); 

    // Port parsing   
    sourceport = htons(p->tcp_header()->th_sport);
    destport = htons(p->tcp_header()->th_dport);

    // proto parsing   
    proto = p->ip_header()->ip_p;

    inet_aton(sourceip.c_str(), &str_sourceip.sin_addr);
    inet_aton(destip.c_str(), &str_destip.sin_addr);

    sourceip_int = htonl(str_sourceip.sin_addr.s_addr);
    destip_int = htonl(str_destip.sin_addr.s_addr);

    if(sourceip_int > destip_int){
        temp = sourceip;
        sourceip = destip;
        destip = temp;
    
        temp_int = sourceport;
        sourceport = destport;
        destport = temp_int;
	//Reverse connection
        isfw = false;
    }

    Connection recv_conn(sourceip, destip, sourceport, destport, proto, isfw);
    return recv_conn;
}


int StatefulFirewall::get_policy_action(Connection &recv_conn)
{
    // verfy policy                           
    for(std::vector<Policy>::iterator pol = list_of_policies.begin(); pol != list_of_policies.end(); ++pol)
    {
    Connection pol_conn;
    pol_conn = (*pol).getConnection(); //Create verified connection
    if(pol_conn == recv_conn){
    if((*pol).getAction() == 1) // Checks action and returns its value
      return 1;
    else
      return 0;        
     }
    }

     return DEFAULTACTION; //no match, send Defauly value
}


CLICK_ENDDECLS
EXPORT_ELEMENT(StatefulFirewall)
