import os, sys, json, nmap, socket, MySQLdb
from netaddr import *
from pprint import pprint

path = os.path.dirname(os.path.abspath(__file__)) + '/'

#==========================================================
# NmappahPahRappah - rap the webs
# sudo scan.py
# targets.txt should be in same directory (1 IPv4 per line)
#==========================================================
# MySQL connection variables
dbhost = "hostname"
dbuser = "username"
dbpass = "password"
dbname = "database"
#===========================================================
def main():

    if os.geteuid() != 0: # check if running as root
        exit("This script was designed to be run as root")

    db = MySQLdb.connect(dbhost,dbuser,dbpass,dbname)
    cursor = db.cursor()

    file = path + 'targets.txt' # path of targets file (1 IPv4 per line)

    #=== NMap Configuration Options ===#
    nm = nmap.PortScanner()
    ports = [1,5,7,11,13,17,18,19,20,21,22,23,25,27,29,31,33,37,38,39,42,43,49,53,57,59,63,66,68,69,70,79,80,88,95,98,101,102,105,107,108,109,110,111,113,115,117,118,119,120,123,124,133,135,137,138,139,143,150,161,179,220,363,366,387,389,396,443,444,445,458,500,512,513,514,515,517,520,521,531,545,548,546,547,554,563,569,593,631,636,648,666,873,989,992,993,995,1080,1085,1433,1434,1521,1604,1758,1812,1813,1818,1985,1999,2049,2543,3128,3306,3389,4000,4321,4333,5000,5004,5005,5190,5432,5800,5801,5900,5901,6000,6667,6970,8008,8080,8081,8181,8383,11371,40193,32773,32776,32779,38036] # list of common ports
    args = '-sS -O' # nmap arguments
    proto = 'tcp'
    #==================================#

    with open(file) as f:
        for line in f: # loop on lines in file. should be 1 ip address per line
            ip = str(IPAddress(line))
            hostname = None
            state = None
            print ip

            try:
                nm.scan(ip, arguments = args) #, translate_ports(ports), arguments = args)
            except nmap.PortScannerError:
                print "nmap error!"
                continue
				            #=== Host Operations Logic ===#
            try: # python nmap returns None for dead hosts, so we use this try as a host alive check
                hostname = str(nm[ip].hostname())
                state = str(nm[ip].state())

                cursor.execute("INSERT INTO host(ip_address, hostname, state, environment_id) VALUES(%s, %s, %s, %s)"
                    " ON DUPLICATE KEY UPDATE hostname = %s, state = %s",
                    (ip, hostname, state, 3, hostname, state))
                db.commit()
            except:
                cursor.execute("INSERT INTO host(ip_address, state, environment_id) VALUES(%s, %s, %s)"
                    " ON DUPLICATE KEY UPDATE state = %s", (ip, 'down', 3, 'down'))
                db.commit()

            #=== Port Operations Logic ===#
            if state == 'up':
                for port in ports:
                    try: # python nmap returns None for closed ports, so we use this try as an open port check
                        port_info = json.loads(json.dumps({port:nm[ip].tcp(int(port))}))
                        # ^ this needs explination. it takes the json string from nmap output
                        # adds some extra info, encodes it to json string, decodes to array
                        port_state = port_info[str(port)]['state']
                        port_reason = port_info[str(port)]['reason']
                        port_name = port_info[str(port)]['name']

                        cursor.execute("INSERT INTO port(host_ip, protocol, number, state, reason, name, timestamp) "
                            "VALUES(%s, %s, %s, %s, %s, %s, now()) ON DUPLICATE KEY "
                            "UPDATE state = %s, reason = %s, timestamp = now()",
                            (ip, proto, str(port), port_state, port_reason, port_name, port_state, port_reason))
                        db.commit()
                    except KeyError, e: # else if port closed
                        # this is super inefficient on the database. too many unneeded calls. rethink this logic
                        cursor.execute("DELETE FROM port WHERE host_ip = %s AND protocol = %s AND number = %s",
                            (ip, proto, str(port)))
                        db.commit()

    cursor.execute("UPDATE knocker.environment SET last_scanned = now() WHERE id = 3")
    db.commit()
	
# Helper function to translate port array to nmap port string
def translate_ports( array ):
    string = ''
    length = len(array)

    for i, val in enumerate(array):
        if i == 0:
            string += str(val)
        else:
            string += (',' + str(val))

    return string


# Helper function to filter out linux metacharacters (strip() is recursive)
# not perfect, i kno, shaddup
def shell_filter( str ):
    str = str.strip()
    str = str.strip('|')
    str = str.strip('||')
    str = str.strip('?')
    str = str.strip(';')
    str = str.strip('&')
    str = str.strip('&&')
    str = str.strip('=')
    str = str.strip('>')
    str = str.strip('<')
    str = str.strip('>>')
    str = str.strip('<<')
    str = str.strip('\\')
    str = str.strip('(')
    str = str.strip(')')
    str = str.strip('"')
    str = str.strip('\'')
    str = str.strip('$')
    str = str.strip('$(')
    str = str.strip('`')
    str = str.strip('[')
    str = str.strip(']')
    str = str.strip('#')
    return str

if __name__ == '__main__': main()
