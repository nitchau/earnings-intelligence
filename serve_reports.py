import os
import sys
import time
import json
import re
import subprocess
import http.server
import socketserver
import threading
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
PORT = 8080

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def end_headers(self):
        # Prevent caching for live reports
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def start_server():
    server = socketserver.TCPServer(("0.0.0.0", PORT), CustomHTTPHandler)
    server.allow_reuse_address = True
    print(f"Local HTTP server running on http://localhost:{PORT}")
    server.serve_forever()

def start_cloudflared():
    cloudflared_path = r"C:\Program Files (x86)\cloudflared\cloudflared.EXE"
    if not os.path.exists(cloudflared_path):
        print("cloudflared binary not found")
        return None

    proc = subprocess.Popen(
        [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    tunnel_url = None
    start_time = time.time()
    while time.time() - start_time < 20:
        line = proc.stderr.readline()
        if "trycloudflare.com" in line:
            m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if m:
                tunnel_url = m.group(0)
                break

    if tunnel_url:
        print(f"Public Cloudflare Tunnel URL: {tunnel_url}")
        (BASE_DIR / "tunnel_url.json").write_text(
            json.dumps({"tunnel_url": tunnel_url, "updated_at": time.time()}, indent=2),
            encoding="utf-8"
        )
    return proc

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    cf_proc = start_cloudflared()
    
    # Keep process alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if cf_proc:
            cf_proc.terminate()
