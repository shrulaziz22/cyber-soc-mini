#!/usr/bin/env python3
"""
Tier-2 Hari 15: tuning 5 aturan (lab sendiri)
- Hitung TP FP semua log + saran naikkan threshold + tulis versi
Pakai: python3 ~/cyber-lab/scripts/tier2_tuning.py
"""
from pathlib import Path
from collections import Counter
import re, json

BASE = Path.home() / "cyber-lab" / "logs"
print("=== TIER-2 HARI 15 TUNING ===")

# kumpulkan semua gagal
semua = ""
for f in ["auth-sample.log","tier2-sample.log"]:
    p = BASE/f
    if p.exists(): semua += p.read_text() + "\n"

ips = re.findall(r"(?:Failed password|401|404).*?(?:from|dari) (\S+)", semua)
c = Counter(ips)
tp = sum(1 for v in c.values() if v>=5)
fp = sum(1 for v in c.values() if v<5)
print(f"Total IP: {dict(c)}")
print(f"TP >=5: {tp} | FP <5: {fp}")
if fp >= tp:
    print("Saran: naikkan SOC-001/003 ke >=8 atau tambah allowlist 203.0.113.10")
else:
    print("Saran: threshold pas, pertahankan + catat versi 1.1")

out = {"tanggal":"hari15","TP":tp,"FP":fp,"aturan":5,"versi":"1.1"}
(BASE/"tuning.json").write_text(json.dumps(out, indent=2))
print("Tersimpan: logs/tuning.json")
print("Tugas 16-65: ulang tiap minggu + simulasi penuh + Sentinel + laporan Inggris.")
