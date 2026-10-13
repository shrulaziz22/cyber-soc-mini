#!/usr/bin/env python3
"""
Hari 3: cek_log + CSV + ALERT otomatis (defensif, lab sendiri)
Pakai:
  python3 ~/cyber-lab/scripts/cek_log_hari3.py
Output:
  ~/cyber-lab/logs/hasil.csv + alert jika >5 gagal dari 1 IP
"""
import re
from collections import Counter
from pathlib import Path
import csv
from datetime import datetime

BASE = Path.home() / "cyber-lab" / "logs"
LOG = BASE / "auth-sample.log"
OUT = BASE / "hasil.csv"

pola_gagal = re.compile(r"Failed password for (\S+) from (\S+)")

gagal = []
with open(LOG) as f:
    for baris in f:
        m = pola_gagal.search(baris)
        if m:
            gagal.append(m.group(2))

hitung = Counter(gagal)

# tulis CSV
with open(OUT, "w", newline="") as csvf:
    w = csv.writer(csvf)
    w.writerow(["waktu_cek", "ip", "jumlah_gagal", "status"])
    now = datetime.now().isoformat(timespec="seconds")
    for ip, jml in hitung.most_common():
        status = "ALERT" if jml >= 5 else "OK"
        w.writerow([now, ip, jml, status])

print(f"[OK] ditulis: {OUT}")
for ip, jml in hitung.most_common():
    if jml >= 5:
        print(f"ALERT: {ip} gagal {jml}x -> cek firewall sendiri, jangan balas menyerang")
    else:
        print(f"OK: {ip} gagal {jml}x")

print("\nIsi CSV:")
print(open(OUT).read())
