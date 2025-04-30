import argparse
import socket
import time
from threading import Semaphore, Thread
from socket import gethostbyname, gethostbyaddr, gaierror, herror, setdefaulttimeout

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'GET / HTTP/1.1\r\nHost: ' + tgtHost.encode() + b'\r\n\r\n')
        results = connSkt.recv(100)
        with screenLock:
            print(f'[+] {tgtPort}/tcp open')
            print(f'[+] {results.decode("utf-8")}')
    except Exception as e:
        with screenLock:
            print(f'[-] {tgtPort}/tcp closed: {str(e)}')
    finally:
        connSkt.close()

def banner_grab(tgtHost, tgtPort):
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.settimeout(5)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'HEAD / HTTP/1.1\r\nHost: ' + tgtHost.encode() + b'\r\n\r\n')
        banner = connSkt.recv(1024).decode('utf-8', errors='ignore')
        return banner.strip()
    except Exception:
        return None
    finally:
        connSkt.close()

def advancedScan(tgtHost, tgtPorts):
    print(f"\n[+] Starting Advanced Scan on {tgtHost}")
    for tgtPort in tgtPorts:
        tgtPort = int(tgtPort)
        try:
            connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connSkt.settimeout(1)
            start_time = time.time()
            result = connSkt.connect_ex((tgtHost, tgtPort))
            end_time = time.time()
            if result == 0:
                banner = banner_grab(tgtHost, tgtPort)
                print(f"[+] {tgtPort}/tcp open (Response Time: {end_time - start_time:.2f}s)")
                if banner:
                    print(f"    Banner: {banner}")
        finally:
            connSkt.close()

def portScan(tgtHost, tgtPorts, advanced=False):
    try:
        tgtIP = gethostbyname(tgtHost)
    except gaierror:
        print(f"[-] Cannot resolve '{tgtHost}': Unknown host")
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print(f'\n[+] Scan Results for: {tgtName[0]}')
    except herror:
        print(f'\n[+] Scan Results for: {tgtIP}')

    setdefaulttimeout(1)

    if advanced:
        advancedScan(tgtHost, tgtPorts)
    else:
        for tgtPort in tgtPorts:
            t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
            t.start()

def main():
    parser = argparse.ArgumentParser(description='Simple Port Scanner')
    parser.add_argument('-u', '-U', dest='tgtHost', type=str, help='Specify target host')
    parser.add_argument('-p', '-P', dest='tgtPorts', type=str, help='Specify target port(s), comma-separated')
    parser.add_argument('-a', '-A', dest='advanced', action='store_true', help='Enable advanced scan')
    parser.add_argument('--all', dest='scanAll', action='store_true', help='Scan all ports (1-65535)')

    args = parser.parse_args()

    tgtHost = args.tgtHost
    tgtPorts = []

    if args.scanAll:
        tgtPorts = list(range(1, 65536))
    elif args.tgtPorts:
        tgtPorts = [int(port.strip()) for port in args.tgtPorts.split(',')]

    if tgtHost is None or not tgtPorts:
        parser.print_help()
        exit(0)

    portScan(tgtHost, tgtPorts, advanced=args.advanced)

if __name__ == '__main__':
    main()
