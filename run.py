"""
run.py — Start both servers with a single command:
    python run.py

- FastAPI tracking server → http://localhost:8000
- Streamlit app          → http://localhost:8501
"""

import subprocess
import sys
import time
import os
import signal
import io

# Fix Windows console Unicode encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    print("=" * 60)
    print("  LeadTrack -- Automated Lead Management System")
    print("=" * 60)
    print()
    print("  [*] Starting FastAPI tracking server on port 8000 ...")

    tracking_proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "tracking_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--log-level", "warning",
        ],
        cwd=BASE_DIR,
    )

    time.sleep(2)
    print("  [OK] Tracking server running at http://localhost:8000")
    print()
    print("  [*] Starting Streamlit dashboard on port 8501 ...")

    streamlit_proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit",
            "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false",
        ],
        cwd=BASE_DIR,
    )

    print("  [OK] Streamlit app running at http://localhost:8501")
    print()
    print("  Press Ctrl+C to stop both servers.")
    print("=" * 60)

    def shutdown(signum, frame):
        print("\n  Shutting down servers...")
        tracking_proc.terminate()
        streamlit_proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        streamlit_proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        tracking_proc.terminate()
        streamlit_proc.terminate()


if __name__ == "__main__":
    main()
