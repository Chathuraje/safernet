import nmap
import socket

def scan_domain(domain: str):
    ip_address = socket.gethostbyname(domain)
    nm = nmap.PortScanner()
    nm.scan(ip_address, '22-443')
    return {"data": nm}


async def perform_nmap_scan(target):
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
        
        output_file = f"nmap_scan_{host}.txt"
        with open(output_file, 'w') as file:
            for result in results:
                file.write(f"Host: {result['host']}\n")
                file.write(f"State: {result['state']}\n")
                file.write(f"Open Ports: {result['open_ports']}\n")
                file.write(f"Vulnerabilities: {result['vulnerabilities']}\n")
                file.write("\n")

    return None


async def vuln_scan(domain: str):
    output_file = f"nmap_scan_{domain}.txt"
    await perform_nmap_scan(domain, output_file)
    return {"results": "Result Will be Available Soon, You can download the file from /download/nmap_scan_{domain}.txt"}