import nmap
import socket

def scan_domain(domain: str):
    ip_address = socket.gethostbyname(domain)
    nm = nmap.PortScanner()
    nm.scan(ip_address, '22-443')
    return {"data": nm}


def perform_nmap_scan(target):
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-p- --script vuln')

    results = []
    for host in nm.all_hosts():
        host_info = {
            "host": host,
            "state": nm[host].state(),
            "open_ports": nm[host].all_tcp(),
            "vulnerabilities": nm[host]['vulners']
        }
        results.append(host_info)

    return results


def vuln_scan(domain: str):
    scan_results = perform_nmap_scan(domain)
    return {"results": scan_results}