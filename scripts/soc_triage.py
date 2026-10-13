#!/usr/bin/env python3
"""
soc_triage.py - Minggu 3 Blue Team mini (defensif, lab sendiri)
- Skor phishing dari logs/phishing-sample.txt
- Deteksi C2 dari logs/malware-sample.log
- Petakan ke MITRE ATT&CK (high-level saja)
Pakai: python3 ~/cyber-lab/scripts/soc_triage.py
"""
from pathlib import Path
import re

BASE = Path.home() / "cyber-lab" / "logs"

print("=== MINGGU 3: SOC TRIAGE ===")

# 1. Phishing
print("\n[1] PHISHING:")
txt = (BASE/"phishing-sample.txt").read_text()
for blok in txt.split("---"):
    if not blok.strip(): continue
    skor = 0
    alasan = []
    if re.search(r"URGENT|24 jam|dikunci", blok, re.I): skor+=2; alasan.append("tekanan waktu")
    if re.search(r"micorsoft|typo|update\.com", blok, re.I): skor+=2; alasan.append("typo domain")
    if re.search(r"http://\d+\.\d+", blok): skor+=2; alasan.append("link IP mentah")
    if re.search(r"\.exe", blok, re.I): skor+=3; alasan.append("attachment exe")
    vonis = "PHISHING-BLOK" if skor>=4 else "BERSIH"
    subj = re.search(r"Subject: (.*)", blok)
    print(f"  {subj.group(1)[:35] if subj else '?'} => skor {skor} [{vonis}] ({', '.join(alasan) if alasan else 'tidak ada sinyal'})")

# 2. Malware / C2
print("\n[2] MALWARE/C2:")
mlog = (BASE/"malware-sample.log").read_text()
for baris in mlog.splitlines():
    if ".exe" in baris: print(f"  EXEC: {baris[:90]} -> T1566/T1204 (eksekusi user)")
    if re.search(r"192\.0\.2\.\d+", baris) and "4444" in baris: print(f"  C2: {baris[:90]} -> T1071 (port non-standar ke IP mentah)")
    if "Accepted" in baris and "203.0.113" in baris: print(f"  OK: login normal, abaikan")

print("\n[3] MITRE MAP (Hari 20-21):")
print("  T1566 Phishing -> waspada email 1")
print("  T1204 User Execution (invoice.exe) -> blokir exe via email")
print("  T1071 C2 192.0.2.99:4444 -> blokir IP di firewall sendiri + isolasi host")
print("\nAksi SOC: isolasi, blokir IoC sendiri, reset password, tulis laporan. Jangan balas menyerang.")
