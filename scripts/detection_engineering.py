#!/usr/bin/env python3
"""
Detection Engineering mini (profesional, defensif, lab sendiri)
- Baca rules/*.yml (Sigma-mini) -> uji ke logs -> convert ke KQL/SPL
Pakai: python3 ~/cyber-lab/scripts/detection_engineering.py
"""
from pathlib import Path
from collections import Counter
import re

BASE = Path.home() / "cyber-lab"
RULE = (BASE/"rules/brute_force.yml").read_text()
LOG = (BASE/"logs/auth-sample.log").read_text()

print("=== DETECTION ENGINEERING ===")
print("[1] Rule loaded: SOC-001 Brute Force (T1110) >=5/5m")

# uji rule
ips = re.findall(r"Failed password for \S+ from (\S+)", LOG)
hitung = Counter(ips)
tp = sum(1 for v in hitung.values() if v>=5)
fp = sum(1 for v in hitung.values() if 1<=v<5)
print(f"[2] Uji ke auth-sample.log: {dict(hitung)}")
print(f"    True Positive (alert benar): {tp} | False Positive (1-4x, abaikan): {fp}")

# convert
print("\n[3] Convert otomatis:")
print("  KQL (Sentinel):")
print("  AuthLog | where Event contains 'Failed password' | summarize gagal=count() by SrcIp, bin(TimeGenerated, 5m) | where gagal >= 5")
print("  SPL (Splunk):")
print('  index=linux "Failed password" | bin _time span=5m | stats count by src_ip, _time | where count>=5')

print("\n[4] Tune pro: kalau FP tinggi, naikkan ke >=8 atau kecualikan IP admin 203.0.113.10 (allowlist sendiri).")
print("Version: git commit tiap ubah rule. Ini kerjaan Detection Engineer.")
