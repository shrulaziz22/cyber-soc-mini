# Laporan Harian SOC Mini - 2026-10-13 11:08

## siem_mini.py
```
[SIEM] sukses=3 gagal=7 alert=1 -> alerts.json
=== MINI SIEM 2026-10-13 11:08 ===
Sukses: 3 | Gagal: 7 | Aturan: >=5 gagal = CRITICAL

Top IP gagal:
  198.51.100.23: 6x [CRITICAL]
  192.0.2.5: 1x [LOW]

Alert tersimpan: 1
- CRITICAL BRUTE_FORCE_SSH 198.51.100.23 6x

[SIEM] buka dashboard: /data/data/com.termux/files/home/cyber-lab/logs/dashboard.html

```

## soc_triage.py
```
=== MINGGU 3: SOC TRIAGE ===

[1] PHISHING:
  URGENT: Verifikasi password anda da => skor 9 [PHISHING-BLOK] (tekanan waktu, typo domain, link IP mentah, attachment exe)
  Jadwal cuti bersama => skor 0 [BERSIH] (tidak ada sinyal)

[2] MALWARE/C2:
  EXEC: Oct 13 11:00:01 lab kernel: invoice.exe hash 5d41402abc4b2a76b9719d911017c592 dijalankan u -> T1566/T1204 (eksekusi user)
  C2: Oct 13 11:00:10 lab net: koneksi keluar ke 192.0.2.99:4444 (port non-standar) -> T1071 (port non-standar ke IP mentah)
  OK: login normal, abaikan

[3] MITRE MAP (Hari 20-21):
  T1566 Phishing -> waspada email 1
  T1204 User Execution (invoice.exe) -> blokir exe via email
  T1071 C2 192.0.2.99:4444 -> blokir IP di firewall sendiri + isolasi host

Aksi SOC: isolasi, blokir IoC sendiri, reset password, tulis laporan. Jangan balas menyerang.

```

## threat_hunt.py
```
=== MINGGU 5: THREAT HUNT ===

[1] Cloud log (jam aneh + user baru):
  ANEH 02:11 admin dari 198.51.100.23 [ConsoleLogin] -> cek: kerja jam 2 pagi?
  ANEH 02:12 admin dari 198.51.100.23 [ConsoleLogin] -> cek: kerja jam 2 pagi?
  ANEH 02:13 admin dari 198.51.100.23 [ConsoleLogin] -> cek: kerja jam 2 pagi?
  ANEH 02:15 root dari 198.51.100.23 [CreateUser] -> cek: kerja jam 2 pagi?
  KRITIS CreateUser oleh 198.51.100.23 -> T1136 (buat akun persistence), isolasi!
  BRUTE 198.51.100.23 3x gagal -> T1110

[2] YARA-mini (pola di log sendiri):
  HIT malware-sample.log: pola '.exe' -> selidiki, jangan jalankan file-nya
  HIT malware-sample.log: pola '4444' -> selidiki, jangan jalankan file-nya

Hunt selesai. Hipotesis -> buktikan dengan log -> catat. Jangan kejar di luar sistem sendiri.

```

## dfir_timeline.py
```
=== MINGGU 7: DFIR TIMELINE ===

[1] Hash bukti:
  auth-sample.log: sha256:1a524dfb1311285d... size:1084B
  malware-sample.log: sha256:a7c92d3724430da6... size:326B
  cloud-sample.json: sha256:f81cda13e6ab157b... size:546B
  phishing-sample.txt: sha256:aa1fb4297f619911... size:406B

[2] Timeline insiden (gabungan lab):
  02:11-02:13 | 3x gagal admin | T1110
  02:15 | CreateUser root | T1136
  10:02 | 6x gagal SSH | T1110
  11:00:01 | EXEC invoice.exe | T1204
  11:00:10 | C2 ke 192.0.2.99:4444 | T1071

Kesimpulan DFIR: simpan hash + jangan ubah file asli + tulis siapa pegang bukti. Ini yang ditanya saat interview SOC.

```
