#!/usr/bin/env python3
"""
Minggu 8-9: laporan_otomatis.py + backup bukti (capstone final)
- Gabung semua tool jadi 1 laporan + zip bukti + hash
Pakai: python3 ~/cyber-lab/scripts/laporan_otomatis.py
"""
import subprocess, hashlib, zipfile
from pathlib import Path
from datetime import datetime

HOME = Path.home()
BASE = HOME / "cyber-lab"
LOGS = BASE / "logs"

print("=== MINGGU 8-9: LAPORAN OTOMATIS ===")
out = [f"# Laporan Harian SOC Mini - {datetime.now():%Y-%m-%d %H:%M}", ""]
for s in ["siem_mini.py","soc_triage.py","threat_hunt.py","dfir_timeline.py"]:
    try:
        r = subprocess.run(["python3", str(BASE/"scripts"/s)], capture_output=True, text=True, timeout=15)
        out.append(f"## {s}\n```\n{r.stdout[:1500]}\n```\n")
        print(f"  OK {s}")
    except Exception as e:
        print(f"  GAGAL {s}: {e}")

lap = LOGS / "LAPORAN_FINAL.md"
lap.write_text("\n".join(out))
print(f"[OK] laporan: {lap} ({lap.stat().st_size}B)")

# backup bukti + hash
zb = LOGS / "bukti.zip"
with zipfile.ZipFile(zb, "w") as z:
    for f in LOGS.glob("*.log"):
        z.write(f, f.name)
    for f in LOGS.glob("*.json"):
        z.write(f, f.name)
h = hashlib.sha256(zb.read_bytes()).hexdigest()[:16]
print(f"[OK] backup: {zb.name} sha256:{h}... - simpan hash ini sebagai chain-of-custody")
print("\nNext: push LAPORAN_FINAL.md + scripts ke GitHub. Jangan upload log asli berisi IP/data pribadi.")
