#!/usr/bin/env python3
"""
Tier-2 Hari 1-14: uji SOC-003 + SOC-004 ke tier2-sample.log (lab sendiri)
Pakai: python3 ~/cyber-lab/scripts/tier2_hari1.py
"""
from pathlib import Path
from collections import Counter
import re

BASE = Path.home() / "cyber-lab" / "logs"
txt = (BASE/"tier2-sample.log").read_text()

print("=== TIER-2 HARI 1-14 ===")
# SOC-003
gagal = re.findall(r"(401|404).*dari (\S+)", txt)
c = Counter(ip for _,ip in gagal)
for ip,j in c.items():
    print(f"SOC-003 web {ip}: {j}x {'ALERT T1110' if j>=3 else 'OK'}")
print("KQL: WebLog | summarize gagal=count() by SrcIp, bin(TimeGenerated,5m) | where gagal>=3")

# SOC-004
print("")
for baris in txt.splitlines():
    if "sudo" in baris and ("shadow" in baris or "tidak ada di sudoers" in baris):
        print(f"SOC-004 sudo ALERT T1548: {baris[:80]}")
print("KQL: SudoLog | where Command contains 'shadow' or User !in (allowlist)")

# DNS panjang (bonus hari 8)
for baris in txt.splitlines():
    if "dns:" in baris:
        dom = re.search(r"query (\S+)", baris)
        if dom and len(dom.group(1))>40:
            print(f"SOC-005 dns ALERT T1071: {dom.group(1)[:30]}... {len(dom.group(1))} char")
print("\nTugas 14 hari: salin pola ini jadi SOC-003/004/005 asli + tune FP + commit tiap ubah.")
