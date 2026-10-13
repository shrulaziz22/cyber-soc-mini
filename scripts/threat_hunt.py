#!/usr/bin/env python3
"""
Minggu 5: threat_hunt.py - berburu anomali di log sendiri (defensif)
- Aturan Sigma-mini: login jam aneh (00-05) + user baru dari IP asing + gagal 3x
- + cek pola YARA-mini: nama file .exe di log
Pakai: python3 ~/cyber-lab/scripts/threat_hunt.py
"""
import json
from pathlib import Path
from collections import Counter

BASE = Path.home() / "cyber-lab" / "logs"

print("=== MINGGU 5: THREAT HUNT ===")

# 1. Cloud hunt
print("\n[1] Cloud log (jam aneh + user baru):")
jalur = BASE/"cloud-sample.json"
gagal_ip = Counter()
for baris in open(jalur):
    e = json.loads(baris)
    jam = int(e["jam"].split(":")[0])
    aneh = 0 <= jam <= 5
    if e["status"]=="gagal":
        gagal_ip[e["ip"]]+=1
    if aneh:
        print(f"  ANEH {e['jam']} {e['user']} dari {e['ip']} [{e['event']}] -> cek: kerja jam 2 pagi?")
    if e["event"]=="CreateUser" and e["ip"]!="203.0.113.10":
        print(f"  KRITIS CreateUser oleh {e['ip']} -> T1136 (buat akun persistence), isolasi!")

for ip,j in gagal_ip.items():
    if j>=3: print(f"  BRUTE {ip} {j}x gagal -> T1110")

# 2. YARA-mini: pola file berbahaya di log sendiri
print("\n[2] YARA-mini (pola di log sendiri):")
pola = [".exe", "mimikatz", "powershell -enc", "4444"]
for logf in [BASE/"malware-sample.log", BASE/"auth-sample.log"]:
    txt = logf.read_text() if logf.exists() else ""
    for p in pola:
        if p in txt: print(f"  HIT {logf.name}: pola '{p}' -> selidiki, jangan jalankan file-nya")

print("\nHunt selesai. Hipotesis -> buktikan dengan log -> catat. Jangan kejar di luar sistem sendiri.")
