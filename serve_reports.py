import os
import sys
import time
import json
import re
import subprocess
import http.server
import threading
from pathlib import Path
from urllib.parse import unquote

BASE_DIR = Path(__file__).parent.resolve()
PORT = int(os.environ.get("REPORTS_PORT", 8080))
API_MARKET_SNAPSHOT = "/api/market-snapshot"
# The server is public through the Cloudflare tunnel: only the portal pages and published tearsheets are served.
PUBLIC_FILES = {"/", "/index.html", "/news.html", "/favicon.ico"}
PUBLIC_DIRS = ("/published_reports/",)


def request_path(raw_path: str) -> str:
    return unquote(raw_path.split("?", 1)[0].split("#", 1)[0])


def is_public_path(raw_path: str) -> bool:
    path = request_path(raw_path)
    if ".." in path or any(c in path for c in ("\\", ":", "\x00")):
        return False
    if any(seg.startswith(".") for seg in path.split("/")):
        return False
    return path in PUBLIC_FILES or path.startswith(PUBLIC_DIRS)


class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if request_path(self.path) == API_MARKET_SNAPSHOT:
            self.send_market_snapshot()
        else:
            super().do_GET()

    def send_head(self):
        if not is_public_path(self.path):
            self.send_error(404, "File not found")
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, "File not found")
        return None

    def send_market_snapshot(self):
        try:
            from market_snapshot import fetch_market_snapshot
            body, status = json.dumps(fetch_market_snapshot(max_age_seconds=55)).encode("utf-8"), 200
        except Exception as exc:
            print(f"[serve_reports] market snapshot failed: {exc}", file=sys.stderr)
            body, status = json.dumps({"error": "market snapshot unavailable"}).encode("utf-8"), 503
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        # Prevent caching for live reports (also covers the market snapshot API)
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()


class ReportsHTTPServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def start_server(port=PORT):
    server = ReportsHTTPServer(("0.0.0.0", port), CustomHTTPHandler)
    print(f"Local HTTP server running on http://localhost:{port}")
    server.serve_forever()


def _drain(stream):
    try:
        for _ in iter(stream.readline, ""):
            pass
    except Exception:
        pass


def start_cloudflared():
    cloudflared_path = r"C:\Program Files (x86)\cloudflared\cloudflared.EXE"
    if not os.path.exists(cloudflared_path):
        print("cloudflared binary not found")
        return None

    proc = subprocess.Popen(
        [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    tunnel_url = None
    start_time = time.time()
    while time.time() - start_time < 20:
        line = proc.stderr.readline()
        if not line and proc.poll() is not None:
            break
        if "trycloudflare.com" in line:
            m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if m:
                tunnel_url = m.group(0)
                break

    # Keep both pipes drained so cloudflared never blocks on a full pipe buffer.
    for stream in (proc.stdout, proc.stderr):
        threading.Thread(target=_drain, args=(stream,), daemon=True).start()

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
