#!/usr/bin/env python3
"""
SOC-002 terbaik: uji CreateUser jam aneh (T1136) ke cloud-sample.json + convert
Pakai: python3 ~/cyber-lab/scripts/detection_best.py
"""
import json
from pathlib import Path

BASE = Path.home() / "cyber-lab"
print("=== RULE TERBAIK SOC-002 (T1136) ===")

tp = fp = 0
for baris in open(BASE/"logs/cloud-sample.json"):
    e = json.loads(baris)
    if e.get("event") != "CreateUser": continue
    jam = int(e["jam"].split(":")[0])
    asing = e["ip"] != "203.0.113.10"
    aneh = 0 <= jam <= 5
    if asing and aneh:
        print(f"  ALERT {e['jam']} {e['user']} dari {e['ip']} -> T1136 persistence!")
        tp += 1
    else:
        fp += 1

print(f"Hasil: TP={tp} FP={fp} (target pro: TP>=1 FP=0)")
print("\nKQL:")
print('CloudLog | where Event=="CreateUser" and TimeGenerated.hour in (0,1,2,3,4,5) and SrcIp != "203.0.113.10"')
print("SPL:")
print('index=cloud Event=CreateUser date_hour<=5 NOT src_ip=203.0.113.10')
print("\nBest practice: tiap rule wajib ada id, mitre, FP, action + test TP/FP + git version. Duet SOC-001+002 ini sudah layak demo interview.")
