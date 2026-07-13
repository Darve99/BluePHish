import urllib.request
import urllib.error
import json

# Usar el token del test_register.py anterior
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzgzOTEyOTkyLCJ0eXBlIjoiYWNjZXNzIn0.PWm_-0mFwr9eAM_8UeVJiujgBAUODLl0bt30f1HS160"

data = json.dumps({"raw_email": "From: attacker@test.com\nTo: user@test.com\nSubject: Test\n\nTest body"}).encode()
req = urllib.request.Request(
    "http://localhost:8000/analysis",
    data=data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    },
    method="POST"
)

try:
    resp = urllib.request.urlopen(req, timeout=10)
    print("STATUS", resp.status)
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print("ERROR", e.code)
    print(e.read().decode())
except Exception as e:
    print("EXCEPTION", type(e).__name__, e)
