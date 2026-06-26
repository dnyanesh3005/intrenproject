import smtplib
import os
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
TRACKING_BASE_URL = os.getenv("TRACKING_BASE_URL", "http://localhost:8000")
REDIRECT_URL = os.getenv("REDIRECT_URL", "https://yourdomain.com")
USE_STREAMLIT_TRACKING = os.getenv("USE_STREAMLIT_TRACKING", "False").lower() in ("true", "1", "t", "yes")


def generate_tracking_id() -> str:
    return str(uuid.uuid4())


def build_email_html(name: str, requirement: str, tracking_id: str) -> str:
    if USE_STREAMLIT_TRACKING:
        trackable_link = f"{TRACKING_BASE_URL}/?track_click={tracking_id}&url={REDIRECT_URL}"
        pixel_url = f"{TRACKING_BASE_URL}/?track_open={tracking_id}"
    else:
        trackable_link = f"{TRACKING_BASE_URL}/track/click?tid={tracking_id}&url={REDIRECT_URL}"
        pixel_url = f"{TRACKING_BASE_URL}/track/open?tid={tracking_id}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thank You, {name}!</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; }}
  .wrapper {{ padding: 40px 20px; }}
  .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.12); }}
  .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 48px 40px; text-align: center; }}
  .header-icon {{ font-size: 48px; margin-bottom: 16px; }}
  .header h1 {{ color: #ffffff; font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }}
  .header p {{ color: rgba(255,255,255,0.8); font-size: 15px; margin-top: 8px; }}
  .body {{ padding: 44px 40px; }}
  .greeting {{ font-size: 20px; font-weight: 600; color: #1a1a2e; margin-bottom: 16px; }}
  .text {{ font-size: 15px; color: #6b7280; line-height: 1.75; margin-bottom: 16px; }}
  .req-card {{ background: linear-gradient(135deg, #f0f4ff, #faf0ff); border: 1px solid #e0e7ff; border-radius: 12px; padding: 20px 24px; margin: 24px 0; }}
  .req-label {{ font-size: 12px; font-weight: 600; color: #764ba2; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
  .req-text {{ font-size: 16px; color: #1a1a2e; font-weight: 500; font-style: italic; }}
  .divider {{ height: 1px; background: #f3f4f6; margin: 28px 0; }}
  .cta-section {{ text-align: center; margin: 32px 0; }}
  .cta-btn {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff !important; text-decoration: none; padding: 16px 40px; border-radius: 50px; font-size: 16px; font-weight: 600; letter-spacing: 0.3px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }}
  .cta-hint {{ font-size: 13px; color: #9ca3af; margin-top: 12px; }}
  .info-box {{ background: #f8fafc; border-radius: 10px; padding: 20px 24px; margin-bottom: 24px; }}
  .info-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
  .info-row:last-child {{ margin-bottom: 0; }}
  .info-icon {{ font-size: 16px; }}
  .info-text {{ font-size: 14px; color: #6b7280; }}
  .info-text strong {{ color: #374151; }}
  .signature {{ margin-top: 32px; }}
  .sig-name {{ font-size: 16px; font-weight: 700; color: #1a1a2e; }}
  .sig-title {{ font-size: 13px; color: #9ca3af; margin-top: 4px; }}
  .footer {{ background: #f8fafc; padding: 28px 40px; text-align: center; border-top: 1px solid #f3f4f6; }}
  .footer p {{ font-size: 12px; color: #9ca3af; line-height: 1.6; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="container">
    <div class="header">
      <div class="header-icon">🚀</div>
      <h1>We've Received Your Request!</h1>
      <p>Our team will review it and get back to you soon</p>
    </div>

    <div class="body">
      <p class="greeting">Hi {name},</p>
      <p class="text">
        Thank you for reaching out! We're excited to learn about your needs and explore how we can help you achieve your goals.
      </p>

      <div class="req-card">
        <p class="req-label">📋 Your Requirement</p>
        <p class="req-text">"{requirement}"</p>
      </div>

      <div class="info-box">
        <div class="info-row">
          <span class="info-icon">⏱️</span>
          <span class="info-text">We typically respond within <strong>24 hours</strong> on business days.</span>
        </div>
        <div class="info-row">
          <span class="info-icon">💼</span>
          <span class="info-text">Our team is reviewing your requirement and will prepare a tailored response.</span>
        </div>
        <div class="info-row">
          <span class="info-icon">📧</span>
          <span class="info-text">Keep an eye on your inbox — a detailed proposal is coming your way.</span>
        </div>
      </div>

      <div class="divider"></div>

      <div class="cta-section">
        <p class="text">Want to learn more about our solutions in the meantime?</p>
        <a href="{trackable_link}" class="cta-btn">Explore Our Services →</a>
        <p class="cta-hint">Clicking the button helps us understand your interests better</p>
      </div>

      <div class="divider"></div>

      <div class="signature">
        <p class="sig-name">Team LeadTrack</p>
        <p class="sig-title">Lead Management System</p>
      </div>
    </div>

    <div class="footer">
      <p>You received this email because you submitted an inquiry through our lead form.</p>
      <p style="margin-top: 8px;">© 2025 LeadTrack. All rights reserved.</p>
    </div>
  </div>
</div>
<!-- Email Open Tracking Pixel (do not remove) -->
<img src="{pixel_url}" width="1" height="1" style="display:none;border:0;outline:none;" alt="" />
</body>
</html>"""


def send_email(lead_id: int, name: str, email: str, requirement: str):
    """
    Send a personalized tracking email.
    Returns (tracking_id, error_message) — error_message is None on success.
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return None, "Email credentials not configured. Please update your .env file."

    tracking_id = generate_tracking_id()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Hi {name}, we received your request! 🎉"
    msg["From"] = f"LeadTrack <{GMAIL_ADDRESS}>"
    msg["To"] = email

    # Plain text fallback
    tracking_link = f"{TRACKING_BASE_URL}/?track_click={tracking_id}&url={REDIRECT_URL}" if USE_STREAMLIT_TRACKING else f"{TRACKING_BASE_URL}/track/click?tid={tracking_id}&url={REDIRECT_URL}"
    plain_text = f"""Hi {name},

Thank you for reaching out to us!

We received your requirement: "{requirement}"

Our team will get back to you within 24 hours.

Learn more about our services: {tracking_link}

Best regards,
Team LeadTrack
"""
    msg.attach(MIMEText(plain_text, "plain"))

    # HTML email
    html_content = build_email_html(name, requirement, tracking_id)
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, email, msg.as_string())
        return tracking_id, None
    except smtplib.SMTPAuthenticationError:
        return None, "Authentication failed. Check your Gmail address and App Password in .env"
    except Exception as e:
        return None, str(e)
