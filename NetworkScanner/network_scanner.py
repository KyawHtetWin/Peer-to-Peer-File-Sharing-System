'''
Network Scanner using ARP requests
'''


#from scapy.all import *
import scapy.all as s

target_ip = "192.168.1.1/24"
# IP Address for the destination
# create ARP packet
arp = s.ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = s.Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp

result = s.srp(packet, timeout=3, verbose=0)[0]

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
