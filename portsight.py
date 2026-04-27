
#!/usr/bin/env python3
"""
PortSight
A clean terminal-based TCP port scanner.

Run:
    python portsight.py
"""

import socket
import sys
import time
import ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


# Settings used for the scan
START_PORT = 1
END_PORT = 1024
THREADS = 200
TIMEOUT = 0.75
BAR_WIDTH = 30


# Common services for nicer output
SERVICES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    445: "smb",
    587: "smtp-tls",
    993: "imaps",
    995: "pop3s",
}


def divider(width=48):
    return "─" * width


def show_banner():
    print()
    print("╭──────────────────────────────────────╮")
    print("│              PortSight              │")
    print("│         TCP Port Scanner            │")
    print("╰──────────────────────────────────────╯")
    print()
    print(f" Default Range : {START_PORT}-{END_PORT}")
    print(divider())
    print()


def update_line(text):
    sys.stdout.write("\r\033[2K" + text)
    sys.stdout.flush()


def progress_bar(done, total):
    ratio = done / total
    filled = int(BAR_WIDTH * ratio)
    empty = BAR_WIDTH - filled
    return "[" + ("█" * filled) + ("░" * empty) + f"] {ratio*100:5.1f}%"


def get_service(port):
    if port in SERVICES:
        return SERVICES[port]

    try:
        return socket.getservbyport(port, "tcp")
    except:
        return "unknown"


def resolve_target(value):
    value = value.strip()

    if not value:
        raise ValueError("Please enter an IP address.")

    try:
        ip = ipaddress.ip_address(value)
        return str(ip), str(ip)
    except ValueError:
        pass

    try:
        ip = socket.gethostbyname(value)
        return ip, f"{value} ({ip})"
    except:
        raise ValueError("Could not resolve target.")


def ask_target():
    while True:
        try:
            target = input(" Target IP : ").strip()
            return resolve_target(target)
        except KeyboardInterrupt:
            print("\n")
            sys.exit()
        except ValueError as err:
            print(err)
            print()


def scan_port(ip, port):
    start = time.perf_counter()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)

            if sock.connect_ex((ip, port)) == 0:
                delay = (time.perf_counter() - start) * 1000
                return {
                    "port": port,
                    "service": get_service(port),
                    "delay": round(delay, 1)
                }

    except:
        pass

    return None


def run_scan(ip):
    total = END_PORT - START_PORT + 1
    checked = 0
    open_ports = []

    print()
    print(" Starting scan...")
    print(divider())
    print(f" Host    : {ip}")
    print(f" Ports   : {START_PORT}-{END_PORT}")
    print(f" Threads : {THREADS}")
    print(divider())
    print()

    begin = time.perf_counter()

    ports = range(START_PORT, END_PORT + 1)

    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        futures = [pool.submit(scan_port, ip, port) for port in ports]

        for future in as_completed(futures):
            result = future.result()

            if result:
                open_ports.append(result)

            checked += 1

            update_line(
                f"{progress_bar(checked, total)}  "
                f"{checked}/{total}  "
                f"Open: {len(open_ports)}"
            )

    update_line("")
    print()

    elapsed = time.perf_counter() - begin
    open_ports.sort(key=lambda x: x["port"])

    return open_ports, elapsed


def show_results(results, target, elapsed):
    print(" Open Ports")
    print(divider())
    print()

    if not results:
        print(" No open ports found.\n")
    else:
        print(" Port   Service       Response")
        print(" ----   -----------   --------")

        for item in results:
            print(
                f" {item['port']:<5}  "
                f"{item['service']:<12}  "
                f"{item['delay']} ms"
            )

        print()

    print(" Scan Summary")
    print(divider())
    print(f" Target     : {target}")
    print(f" Found      : {len(results)}")
    print(f" Duration   : {elapsed:.2f}s")
    print(f" Finished   : {datetime.now().strftime('%H:%M:%S')}")
    print()


def main():
    show_banner()

    ip, display = ask_target()

    results, elapsed = run_scan(ip)

    show_results(results, display, elapsed)


if __name__ == "__main__":
    main()
