#!/usr/bin/env python3
"""
app.py - web lab AMAN milik sendiri (pengganti DVWA di HP)
Jalan: python3 ~/cyber-lab/web-lab/app.py
Buka di browser HP: http://127.0.0.1:8000
Demo bertahan: input di-escape + header aman. Tidak ada kode rentan.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import html
from urllib.parse import urlparse, parse_qs

class Aman(BaseHTTPRequestHandler):
    def _header(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Security-Policy", "default-src 'self'")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        nama = html.escape(q.get("nama", ["tamu"])[0][:50])  # bertahan: escape + batas panjang
        self._header()
        self.wfile.write(f"<h2>Lab sendiri</h2><p>Halo {nama} (sudah di-escape, aman dari XSS)</p><form>Nama:<input name=nama><button>Kirim</button></form>".encode())
    def log_message(self, *a): pass

print("Lab aman jalan di http://127.0.0.1:8000 (Ctrl+C untuk stop)")
HTTPServer(("127.0.0.1", 8000), Aman).serve_forever()
