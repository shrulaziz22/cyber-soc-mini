#!/usr/bin/env python3
"""
SIEM MINI Hari 6-7 (Termux, ringan, defensif)
- Baca ~/cyber-lab/logs/auth-sample.log
- Deteksi brute-force: >=5 gagal dari 1 IP
- Output: alerts.json + dashboard.txt + dashboard.html
Pakai: python3 ~/cyber-lab/scripts/siem_mini.py
"""
import re, json
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "cyber-lab" / "logs"
LOG = BASE / "auth-sample.log"
ALERT = BASE / "alerts.json"
DASH = BASE / "dashboard.txt"
HTML = BASE / "dashboard.html"

pola_gagal = re.compile(r"(\w+\s+\d+ \S+) .* Failed password for (\S+) from (\S+)")
pola_sukses = re.compile(r"Accepted password for (\S+) from (\S+)")

gagal_ip = []
sukses = 0
gagal = 0
detail = defaultdict(list)

for baris in open(LOG):
    if "Failed password" in baris:
        gagal += 1
        m = pola_gagal.search(baris)
        ip = m.group(3) if m else "unknown"
        gagal_ip.append(ip)
        detail[ip].append(baris.strip()[:120])
    elif "Accepted password" in baris:
        sukses += 1

hitung = Counter(gagal_ip)
alerts = []
for ip, jml in hitung.items():
    level = "CRITICAL" if jml >= 5 else "LOW"
    if jml >= 5:
        alerts.append({
            "waktu": datetime.now().isoformat(timespec="seconds"),
            "rule": "BRUTE_FORCE_SSH",
            "ip": ip,
            "count": jml,
            "level": level,
            "aksi": "Blok di firewall sendiri + ganti password + cek authorized_keys. Jangan balas menyerang."
        })

ALERT.write_text(json.dumps(alerts, indent=2))
print(f"[SIEM] sukses={sukses} gagal={gagal} alert={len(alerts)} -> {ALERT.name}")

# dashboard txt
with open(DASH, "w") as f:
    f.write(f"=== MINI SIEM {datetime.now():%Y-%m-%d %H:%M} ===\n")
    f.write(f"Sukses: {sukses} | Gagal: {gagal} | Aturan: >=5 gagal = CRITICAL\n\n")
    f.write("Top IP gagal:\n")
    for ip, jml in hitung.most_common():
        f.write(f"  {ip}: {jml}x {'[CRITICAL]' if jml>=5 else '[LOW]'}\n")
    f.write(f"\nAlert tersimpan: {len(alerts)}\n")
    for a in alerts:
        f.write(f"- {a['level']} {a['rule']} {a['ip']} {a['count']}x\n")

# dashboard html ringan
rows = "".join(f"<tr><td>{ip}</td><td>{j}</td><td>{'CRITICAL' if j>=5 else 'LOW'}</td></tr>" for ip,j in hitung.most_common())
HTML.write_text(f"<html><head><meta charset=utf-8><title>Mini SIEM</title></head><body><h2>Mini SIEM {datetime.now():%H:%M}</h2><p>Sukses:{sukses} Gagal:{gagal}</p><table border=1><tr><th>IP</th><th>Gagal</th><th>Level</th></tr>{rows}</table><p>Aturan: >=5 = CRITICAL. Hanya untuk log sendiri.</p></body></html>")

print(open(DASH).read())
print(f"[SIEM] buka dashboard: {HTML}")
