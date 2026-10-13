#!/usr/bin/env python3
"""
Minggu 7: dfir_timeline.py - forensik mini (defensif, barang bukti lab sendiri)
- Bikin timeline dari 3 log + hash SHA256 tiap file (chain-of-custody mini)
- Jangan sentuh barang bukti asli orang lain.
Pakai: python3 ~/cyber-lab/scripts/dfir_timeline.py
"""
from pathlib import Path
import hashlib, re

BASE = Path.home() / "cyber-lab" / "logs"
print("=== MINGGU 7: DFIR TIMELINE ===")

# 1. Hash bukti (integritas)
print("\n[1] Hash bukti:")
for f in ["auth-sample.log","malware-sample.log","cloud-sample.json","phishing-sample.txt"]:
    p = BASE/f
    if p.exists():
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        print(f"  {f}: sha256:{h}... size:{p.stat().st_size}B")

# 2. Timeline gabungan (Urut manual mini)
print("\n[2] Timeline insiden (gabungan lab):")
events = []
for baris in open(BASE/"malware-sample.log"):
    if "11:00:01" in baris: events.append(("11:00:01","EXEC invoice.exe","T1204"))
    if "4444" in baris: events.append(("11:00:10","C2 ke 192.0.2.99:4444","T1071"))
events += [("02:11-02:13","3x gagal admin","T1110"), ("02:15","CreateUser root","T1136"), ("10:02","6x gagal SSH","T1110")]
for jam, apa, tid in sorted(events):
    print(f"  {jam} | {apa} | {tid}")

print("\nKesimpulan DFIR: simpan hash + jangan ubah file asli + tulis siapa pegang bukti. Ini yang ditanya saat interview SOC.")
