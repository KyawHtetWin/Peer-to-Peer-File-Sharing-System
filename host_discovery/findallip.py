import nmap

class Network():
    def __init__(self):
        ip = input("Enter IP(Default-192.168.1.1/192.168.0.1):")
        self.ip = ip

    def networkScanner(self):
        if len(self.ip) == 0:
            network = '192.168.1.1/24'
        else:
            network = self.ip + '/24'

        print("Scanning Please wait ----> ")

        nm = nmap.PortScanner()
        nm.scan(hosts= network, arguments='-sn')
        host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for host in host_list:
            print("Host\t{}".format(host))

if __name__ == "__main__":
    D = Network()
    D.networkScanner()