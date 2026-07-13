import urllib.request
import urllib.error
import json
import sys

# Get fresh token from login
login_data = json.dumps({"email": "test@example.com", "password": "pass123"}).encode()
login_req = urllib.request.Request(
    "http://127.0.0.1:8000/auth/login",
    data=login_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
resp = urllib.request.urlopen(login_req, timeout=10)
token = json.loads(resp.read().decode())["access_token"]

print("Token obtained:", token[:50] + "...", file=sys.stderr)

# Email con caracteres reales que podrían causar problemas
test_email = """From: sender@example.com
To: recipient@test.com
Subject: Test Email
Date: Mon, 12 Jul 2026 12:00:00 +0000
Content-Type: text/plain; charset="UTF-8"

This is a test email with special chars: áéíóú ñ

Click here: https://malicious-link.com
"""

analysis_data = json.dumps({"raw_email": test_email}).encode()
print("Payload size:", len(analysis_data), file=sys.stderr)

analysis_req = urllib.request.Request(
    "http://127.0.0.1:8000/analysis",
    data=analysis_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    },
    method="POST"
)

try:
    resp_analysis = urllib.request.urlopen(analysis_req, timeout=10)
    print("ANALYSIS STATUS", resp_analysis.status)
    result = json.loads(resp_analysis.read().decode())
    print("SCORE:", result.get("score"))
except urllib.error.HTTPError as e:
    print("ANALYSIS ERROR", e.code, file=sys.stderr)
    error_body = e.read().decode()
    print("Error response:", error_body, file=sys.stderr)
    try:
        error_json = json.loads(error_body)
        print("Detail:", error_json.get("detail"), file=sys.stderr)
    except:
        pass
except Exception as e:
    print("EXCEPTION", type(e).__name__, e, file=sys.stderr)
