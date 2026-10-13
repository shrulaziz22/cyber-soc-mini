#!/usr/bin/env python3
"""
Hari 4 HP: Pengganti Wireshark (tanpa GUI/root)
- Di PC: filter dns, http, tcp.flags.syn
- Di HP: pakai dig + python requests + nmap --packet-trace
Hanya ke lab sendiri / situs legal.
"""
import socket, time
import requests

print("=== 1. DNS (pengganti filter 'dns') ===")
for domain in ["example.com", "google.com"]:
    try:
        ip = socket.gethostbyname(domain)
        print(f"{domain} -> {ip}")
    except Exception as e:
        print(f"{domain} gagal: {e}")

print("\n=== 2. HTTP (pengganti filter 'http') ===")
try:
    t0 = time.time()
    r = requests.get("https://example.com", timeout=10)
    dt = (time.time()-t0)*1000
    print(f"GET https://example.com = {r.status_code} dalam {dt:.0f}ms, {len(r.content)} bytes")
    print(f"Server: {r.headers.get('Content-Type','?')}")
except Exception as e:
    print(f"HTTP gagal: {e}")

print("\n=== 3. TCP handshake (pengganti 'tcp.flags') ===")
print("Jalankan manual di Termux untuk lihat SYN:")
print("  nmap --packet-trace -F 127.0.0.1")
print("Normal: SYN -> RST (refused) karena port closed = aman")
print("Kalau SYN -> SYN-ACK = port OPEN, harus diselidiki")
print("\nTugas: bandingkan 'ping -c 2 8.8.8.8' vs 'dig example.com' - mana DNS, mana ICMP?")
