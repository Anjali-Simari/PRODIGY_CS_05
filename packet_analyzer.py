# ============================================================
# Task 5 - Network Packet Analyzer
# Prodigy InfoTech Cybersecurity Internship
# Author: Anjali Kunwar Simari
#
# install : pip install scapy
#           windows users also need npcap -> https://npcap.com
# run     : windows -> run as Administrator: python packet_analyzer.py
#           linux/mac -> sudo python3 packet_analyzer.py
# ============================================================
from scapy.all import sniff, IP, TCP, UDP, ICMP
import datetime

PACKET_COUNT = 15   # change this to capture more or fewer packets

# counter to track how many packets have been captured so far
packet_number = 0

def get_protocol(packet):
    # check which protocol this packet is using
    if packet.haslayer(TCP):    return "TCP"
    elif packet.haslayer(UDP):  return "UDP"
    elif packet.haslayer(ICMP): return "ICMP"
    else:                       return "Other"

def get_ports(packet):
    # extract source and destination port numbers
    # ports only exist in TCP and UDP packets, not ICMP
    if packet.haslayer(TCP):
        return packet[TCP].sport, packet[TCP].dport
    elif packet.haslayer(UDP):
        return packet[UDP].sport, packet[UDP].dport
    else:
        return None, None

def get_payload(packet):
    # try to read the data inside the packet
    try:
        if packet.haslayer(TCP):       raw = bytes(packet[TCP].payload)
        elif packet.haslayer(UDP):     raw = bytes(packet[UDP].payload)
        else:                          raw = bytes(packet[IP].payload)
        return raw.decode("utf-8", errors="ignore").strip()[:50] or "binary data"
    except Exception:
        return "could not read"

def analyze_packet(packet):
    # scapy calls this automatically for every packet it captures
    if not packet.haslayer(IP):
        return   # skip non-IP packets like ARP

    global packet_number
    packet_number += 1

    src      = packet[IP].src
    dst      = packet[IP].dst
    time     = datetime.datetime.now().strftime("%H:%M:%S")
    protocol = get_protocol(packet)
    sport, dport = get_ports(packet)
    payload  = get_payload(packet)

    # format IP:port if port exists, otherwise just IP (for ICMP)
    src_display = f"{src}:{sport}" if sport else src
    dst_display = f"{dst}:{dport}" if dport else dst

    print(f"\n  Packet {packet_number}/{PACKET_COUNT}  [{time}]")
    print(f"  {src_display}  -->  {dst_display}")
    print(f"  Protocol : {protocol}")
    print(f"  Data     : {payload}")
    print("  " + "-" * 40)


def main():
    print("=" * 45)
    print("  Network Packet Analyzer")
    print("  Prodigy InfoTech Cybersecurity Internship")
    print("=" * 45)
    print()
    print("  WARNING: only use this on your own network!")
    print("  this tool is for educational purposes only.")
    print()

    answer = input("  do you agree? (yes/no): ").strip().lower()
    if answer not in ("yes", "y"):
        print("  exiting.")
        return

    print(f"\n  capturing {PACKET_COUNT} packets... press Ctrl+C to stop early\n")

    try:
        sniff(prn=analyze_packet, count=PACKET_COUNT, store=False, filter="ip")
    except KeyboardInterrupt:
        print("\n  stopped by user.")
    except Exception as e:
        print(f"  filter failed ({e}), trying without filter...")
        try:
            sniff(prn=analyze_packet, count=PACKET_COUNT, store=False)
        except KeyboardInterrupt:
            print("\n  stopped by user.")
        except Exception as e:
            print(f"  capture failed: {e}")

    print("\n  done! capture complete.")


if __name__ == "__main__":
    main()
