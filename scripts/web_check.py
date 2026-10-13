#!/usr/bin/env python3
"""
web_check.py - cek header keamanan situs SENDIRI (defensif)
Pakai: python3 ~/cyber-lab/scripts/web_check.py http://127.0.0.1:8000
Jangan scan situs orang tanpa izin. Untuk belajar pakai localhost + example.com saja.
"""
import sys
import requests

WAJIB = ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Strict-Transport-Security"]

def cek(url):
    print(f"=== CEK {url} ===")
    try:
        r = requests.get(url, timeout=10)
        print(f"Status: {r.status_code}")
        skor = 0
        for h in WAJIB:
            ada = h in r.headers
            print(f"  {h}: {'ADA' if ada else 'HILANG -> tambah di server sendiri'}")
            if ada: skor += 1
        print(f"Skor: {skor}/{len(WAJIB)}")
        if skor < 3:
            print("Saran: tambah header di app.py milikmu, jangan ubah situs orang.")
    except Exception as e:
        print(f"Gagal (server belum jalan?): {e}")
        print("Jalankan dulu: python3 ~/cyber-lab/web-lab/app.py")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    cek(url)
