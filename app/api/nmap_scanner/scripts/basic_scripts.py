import nmap
import socket

def scan_domain(domain: str):
    ip_address = socket.gethostbyname(domain)
    nm = nmap.PortScanner()
    nm.scan(ip_address, '22-443')
    return {"data": nm}