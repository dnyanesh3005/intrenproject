"""
FastAPI Tracking Server
-----------------------
Runs on port 8000. Handles:
  GET /track/open?tid=<uuid>   → records email open, returns 1x1 GIF
  GET /track/click?tid=<uuid>&url=<url> → records click, redirects to url
  GET /health                  → health check
"""

import base64
import sys
import os

# Allow importing from parent directory
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.responses import Response, RedirectResponse, JSONResponse

from services.db import init_db, mark_email_opened, insert_link_click

# Bootstrap DB on startup
init_db()

app = FastAPI(
    title="LeadTrack Email Tracking Server",
    description="Handles email open & click tracking",
    version="1.0.0",
)

# 1×1 transparent GIF (base64 encoded)
TRANSPARENT_GIF_B64 = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
TRANSPARENT_GIF = base64.b64decode(TRANSPARENT_GIF_B64)


@app.get("/track/open")
async def track_open(tid: str):
    """
    Email open tracking endpoint.
    Called when the email client loads the 1x1 tracking pixel.
    """
    try:
        mark_email_opened(tid)
    except Exception as e:
        # Silently fail — never break the user experience
        print(f"[TRACKING] Open tracking error for {tid}: {e}")

    return Response(
        content=TRANSPARENT_GIF,
        media_type="image/gif",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, private",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/track/click")
async def track_click(tid: str, url: str):
    """
    Link click tracking endpoint.
    Logs the click and redirects the user to the real URL.
    """
    try:
        insert_link_click(tid, url)
    except Exception as e:
        print(f"[TRACKING] Click tracking error for {tid}: {e}")

    # Ensure the URL is safe to redirect to
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return RedirectResponse(url=url, status_code=302)


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "service": "LeadTrack Tracking Server"})


@app.get("/")
async def root():
    return JSONResponse({
        "service": "LeadTrack Email Tracking Server",
        "endpoints": ["/track/open", "/track/click", "/health"]
    })
