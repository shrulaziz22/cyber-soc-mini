#!/usr/bin/env python3
"""
Hari 5: Hardening audit defensif untuk Termux (milik sendiri saja)
Cek: permission 777, ssh key perm, sshd config, port terbuka
"""
import os, stat, subprocess
from pathlib import Path

HOME = Path.home()
LAB = HOME / "cyber-lab"

print("=== HARI 5: HARDENING CHECK (HP sendiri) ===")

# 1. Cek file 777 / world-writable di cyber-lab saja (aman, cepat)
print("\n[1] Cek permission longgar di ~/cyber-lab:")
buruk = []
for p in LAB.rglob("*"):
    try:
        mode = p.stat().st_mode
        if mode & stat.S_IWOTH:  # world-writable
            buruk.append(str(p))
    except: pass
if buruk:
    print(f"TEMUAN: {len(buruk)} file world-writable:")
    for b in buruk[:10]: print(f"  - {b} -> perbaiki: chmod o-w {b}")
else:
    print("OK: tidak ada file world-writable di cyber-lab (bagus, 600/700 semua)")

# 2. Cek .ssh
print("\n[2] Cek ~/.ssh:")
ssh = HOME / ".ssh"
print(f"  dir .ssh = {oct(ssh.stat().st_mode)[-3:]} (harus 700)")
for f in ssh.iterdir():
    m = oct(f.stat().st_mode)[-3:]
    print(f"  {f.name} = {m} {'OK' if m in ['600','644','700'] else 'CEK!'}")
ak = ssh / "authorized_keys"
if ak.exists() and ak.stat().st_size == 0:
    print("  authorized_keys kosong = OK (tidak ada akses luar)")

# 3. Cek sshd_config
print("\n[3] Cek sshd_config:")
conf = Path(os.environ.get("PREFIX","/data/data/com.termux/files/usr")) / "etc/ssh/sshd_config"
txt = conf.read_text() if conf.exists() else ""
for kunci in ["PasswordAuthentication", "PermitRootLogin", "PubkeyAuthentication"]:
    hit = [l for l in txt.splitlines() if kunci in l and not l.strip().startswith("#")]
    print(f"  {kunci}: {hit[0] if hit else '(default / tidak diset eksplisit)'}")
print("  Saran Termux: pakai key saja (kamu sudah punya security_lab_ed25519), jangan nyalakan sshd ke internet tanpa perlu")

# 4. Cek port (pakai nmap, bukan ss yang diblokir Android)
print("\n[4] Cek port terbuka (nmap localhost):")
try:
    out = subprocess.run(["nmap","-F","127.0.0.1"], capture_output=True, text=True, timeout=20).stdout
    if "0 hosts" in out or "All 100" in out and "closed" in out:
        print("  OK: 100 port closed, tidak ada service nganga")
    else:
        print(out[:500])
except Exception as e:
    print(f"  nmap gagal: {e}")

print("\n=== RINGKASAN HARI 5 ===")
print("Di HP non-root kamu TIDAK bisa: ufw, systemctl disable service, edit /etc/shadow.")
print("Yang BISA & WAJIB: chmod benar, ssh pakai key, matikan sshd kalau tidak dipakai (pkill sshd), pkg upgrade.")
