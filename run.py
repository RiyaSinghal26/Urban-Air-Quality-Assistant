"""
AuraShield AI: Winter Smog & Urban Air Pollution Navigator
Application Runner Script
"""

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
    port = find_available_port(8000)
    url = f"http://127.0.0.1:{port}"

    print("=" * 70)
    print("🛡️  AuraShield AI: Winter Smog & Urban Air Pollution Navigator")
    print("=" * 70)
    print(f"🚀 Starting server on: {url}")
    print(f"📡 Access the web dashboard at: {url}")
    print("💡 Press Ctrl+C to stop the server.")
    print("=" * 70)

    # Optional: open browser automatically if interactive
    if "--no-browser" not in sys.argv:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False, log_level="info")
