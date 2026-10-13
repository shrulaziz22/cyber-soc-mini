# Home SOC Mini (Termux / Android) — SOC Tier-1 Menuju Tier-2

Belajar 63 hari dari HP: monitoring, triage, hunting, DFIR, semua di lab sendiri dengan data sampel.

## Skill
- Log Analysis (Linux auth, CloudTrail-mini)
- SIEM mini: rule `>=5 gagal = CRITICAL`, alert JSON, dashboard HTML
- SOC Triage: phishing scoring, C2 detection, MITRE ATT&CK T1110/T1136/T1204/T1071/T1566
- Network: Nmap localhost, DNS, HTTP header check
- Hardening: permission audit, SSH key, port audit
- DFIR mini: timeline + SHA256 chain-of-custody

## Struktur
```
scripts/cek_log.py — analis log dasar
scripts/cek_log_hari3.py — CSV + alert
scripts/hari4_net.py — DNS/HTTP/TCP (pengganti Wireshark)
scripts/hari5_hardening.py — audit permission + SSH + port
scripts/siem_mini.py — SIEM: alerts.json + dashboard
scripts/web_check.py — cek header (CSP, X-Frame, dll)
scripts/soc_triage.py — phishing + malware triage
scripts/threat_hunt.py — jam aneh + CreateUser + YARA-mini
scripts/dfir_timeline.py — timeline + hash bukti
scripts/laporan_otomatis.py — gabung semua jadi LAPORAN_FINAL.md
scripts/detection_engineering.py — Sigma SOC-001 -> KQL/SPL + tune TP/FP
scripts/detection_best.py — Sigma SOC-002 T1136 jam aneh
rules/brute_force.yml — SOC-001 T1110 >=5/5m
rules/persistence_createuser.yml — SOC-002 T1136 jam 00-05
web-lab/app.py — server aman sendiri (escape + CSP)
logs/* — SEMUA SAMPEL, bukan data asli
```

## Cara jalan (Termux)
```
python3 scripts/siem_mini.py
python3 scripts/soc_triage.py
python3 scripts/threat_hunt.py
python3 scripts/dfir_timeline.py
python3 scripts/laporan_otomatis.py
# lihat: logs/LAPORAN_FINAL.md, logs/dashboard.html, logs/alerts.json
```

## Contoh hasil
- `198.51.100.23: 6x gagal = CRITICAL BRUTE_FORCE`
- Phishing skor 9 = BLOK (typo domain + IP mentah + exe)
- `CreateUser root jam 02:15 = T1136 persistence`
- XSS `<script>` jadi `&lt;script&gt;` = aman

## Etika
Hanya lab milik sendiri + situs latihan legal (TryHackMe, HackTheBox, PortSwigger Academy). Tidak menyerang sistem orang lain.

— Dibuat 63 hari, 12 script, 500+ baris, 2 Sigma rule TP 2 FP 0, full di Android.
