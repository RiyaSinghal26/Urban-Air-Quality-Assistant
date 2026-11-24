"""
AuraShield AI: Winter Smog & Urban Air Pollution Navigator
Application Runner Script
"""

import os
import sys
import socket
import webbrowser
import uvicorn

def is_port_free(port: int, host: str = "127.0.0.1") -> bool:
    """Checks if a network port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) != 0

def find_available_port(start_port: int = 8000, max_attempts: int = 20) -> int:
    """Finds the first available port starting from start_port."""
    for p in range(start_port, start_port + max_attempts):
        if is_port_free(p):
            return p
    return start_port

if __name__ == "__main__":
    env_port = os.environ.get("PORT")
    if env_port:
        port = int(env_port)
        host = "0.0.0.0"
    else:
        port = find_available_port(8000)
        host = "127.0.0.1"

    url = f"http://{host}:{port}"

    print("=" * 70)
    print("🛡️  AuraShield AI: Winter Smog & Urban Air Pollution Navigator")
    print("=" * 70)
    print(f"🚀 Starting server on: {url} (host: {host}, port: {port})")
    print(f"📡 Access the web dashboard at: {url}")
    print("💡 Press Ctrl+C to stop the server.")
    print("=" * 70)

    # Optional: open browser automatically if local interactive session
    if not env_port and "--no-browser" not in sys.argv:
        try:
            webbrowser.open(f"http://127.0.0.1:{port}")
        except Exception:
            pass

    uvicorn.run("app.main:app", host=host, port=port, reload=False, log_level="info")
