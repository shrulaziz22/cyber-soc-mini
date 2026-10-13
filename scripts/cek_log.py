#!/usr/bin/env python3
"""
cek_log.py - Latihan Hari 2-3: analis log untuk keamanan defensif
Cara pakai di Termux:
  python3 ~/cyber-lab/scripts/cek_log.py ~/cyber-lab/logs/auth-sample.log
Hanya untuk menganalisis log milik sendiri di lab.
"""
import sys
import re
from collections import Counter

def analisis(path):
    gagal = []
    sukses = []
    pola_gagal = re.compile(r"Failed password for (\S+) from (\S+)")
    pola_sukses = re.compile(r"Accepted password for (\S+) from (\S+)")

    with open(path) as f:
        for baris in f:
            m = pola_gagal.search(baris)
            if m:
                gagal.append(m.group(2))
                continue
            m2 = pola_sukses.search(baris)
            if m2:
                sukses.append(m2.group(2))

    print(f"Total sukses: {len(sukses)}")
    print(f"Total gagal: {len(gagal)}")
    print("\nTop IP gagal:")
    for ip, jml in Counter(gagal).most_common(5):
        status = " <-- ALERT: kemungkinan brute-force, cek & blok di firewall sendiri" if jml >= 5 else ""
        print(f"  {ip}: {jml}x{status}")

    if not gagal:
        print("Aman: tidak ada login gagal.")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else input("Path log: ")
    analisis(path)
