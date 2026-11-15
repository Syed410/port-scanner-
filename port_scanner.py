import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def scan_port(target_ip, port):
    """
    Attempts to connect to a specific port on the target IP.
    """
    try:
        # Create a socket object (IPv4, TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        
        # Connect to target
        result = s.connect_ex((target_ip, port))
        s.close()
        
        if result == 0:
            return port
    except Exception:
        pass
    return None

def run_scanner(target_host, ports_to_scan):
    """
    Scans a list of ports using a thread pool for speed.
    """
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print(f"[x] Hostname could not be resolved: {target_host}")
        return

    print(f"[*] Starting scan on target: {target_ip}")
    start_time = time.time()
    
    open_ports = []
    # Use ThreadPoolExecutor for fast concurrent scanning
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in ports_to_scan}
        for future in futures:
            port = futures[future]
            try:
                result = future.result()
                if result:
                    print(f"[+] Port {port} is OPEN")
                    open_ports.append(port)
            except Exception as e:
                print(f"[x] Error scanning port {port}: {e}")

    duration = time.time() - start_time
    print(f"\n[*] Scan completed in {duration:.2f} seconds.")
    print(f"[*] Open ports found: {open_ports if open_ports else 'None'}")

if __name__ == "__main__":
    # Target and common ports to check (e.g., FTP, SSH, HTTP, HTTPS)
    target = "127.0.0.1" 
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 8080]
    
    run_scanner(target, common_ports)
