import scapy.all as s

request = s.ARP()  # 1. Creates an ARP packet request

# 2. Set the network range
request.pdst = '10.5.19.80/24' #ip range from 10.5.19.80 to 10.5.19.254

# 3. Create an Ethernet packet using Ether() method
broadcast = s.Ether()

# 4. Set the destination to broadcast using hwdst
broadcast.hwdst = "ff:ff:ff:ff:ff:ff"

# 5. Combine ARP request packet and Ethernet frame using "/"
packet = request/broadcast

# 6. Send this to the network and capture the response from different devices
client = s.srp(packet, timeout=3, verbose=0)

# 7. Print the IP and MAC address from the response packets
for sent, received in client:
    print("IP:{}\t MAC:{}".format(received.psrc, received.hwsrc))

print(request.summary())  # Prints the summary of that request
print(request.show()) # Shows more details about the packet