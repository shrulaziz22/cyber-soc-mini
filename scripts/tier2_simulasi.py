#!/usr/bin/env python3
"""
Tier-2 Hari 31: simulasi penuh web->sudo->dns (lab sendiri)
Pakai: python3 ~/cyber-lab/scripts/tier2_simulasi.py
"""
from pathlib import Path
print("=== HARI 31 SIMULASI PENUH ===")
print("11:00 web 4x gagal T1110 dari 198.51.100.23")
print("11:03 sudo shadow + admin liar T1548")
print("11:04 dns panjang 44 char T1071")
print("Rantai: brute gagal -> coba sudo -> coba C2. Korelasi 3 = insiden.")
print("Aksi Tier-1: isolasi host sendiri, blokir IP di firewall sendiri, amankan hash+log, eskalasi Tier-2 dengan timeline.")
out = Path.home()/"cyber-lab/logs/simulasi31.txt"
out.write_text("web T1110 -> sudo T1548 -> dns T1071 = incident chain. Action: isolate, block own, hash, escalate.\n")
print("Tersimpan: logs/simulasi31.txt. Tugas: tulis versi Inggris 5 baris di laporan.")
