import psutil
import socket

import nmap
from prettytable import PrettyTable


def get_network_info():
    """Get current network information using psutil instead of netifaces"""
    # Get default gateway
    gateways = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    # Find the active interface
    for interface, addrs in gateways.items():
        if interface in stats and stats[interface].isup:
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address != '127.0.0.1':
                    # Get the IP and assume /24 network
                    ip_parts = addr.address.split('.')
                    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
                    gateway = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
                    return gateway, network

    return "192.168.1.1", "192.168.1.0/24"


def scan_network_with_nmap():
    """Scan the network using nmap"""
    try:
        gateway, network = get_network_info()
        print(f"Gateway: {gateway}")
        print(f"Scanning network: {network}")
        print("-" * 60)

        # Initialize nmap scanner
        nm = nmap.PortScanner()

        # Scan the network
        nm.scan(hosts=network, arguments='-sn')

        # Create table
        table = PrettyTable()
        table.field_names = ["IP Address", "Hostname", "MAC Address", "Vendor", "Status"]

        all_hosts = nm.all_hosts()
        print(f"Found {len(all_hosts)} devices:")

        for host in all_hosts:
            if nm[host].state() == 'up':
                # Get IP address
                ip = host

                # Get hostname
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "Unknown"

                # Get MAC address and vendor
                mac_address = "Unknown"
                vendor = "Unknown"

                if 'addresses' in nm[host]:
                    if 'mac' in nm[host]['addresses']:
                        mac_address = nm[host]['addresses']['mac']
                        vendor = nm[host]['vendor'].get(mac_address, "Unknown")

                table.add_row([ip, hostname, mac_address, vendor, nm[host].state()])

        print(table)

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure nmap is installed and you have proper permissions")


if __name__ == "__main__":
    scan_network_with_nmap()