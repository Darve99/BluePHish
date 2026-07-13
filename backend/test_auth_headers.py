import urllib.request
import urllib.error
import json

# Get fresh token from login
login_data = json.dumps({"email": "test@example.com", "password": "pass123"}).encode()
login_req = urllib.request.Request(
    "http://localhost:8000/auth/login",
    data=login_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
resp = urllib.request.urlopen(login_req, timeout=10)
token = json.loads(resp.read().decode())["access_token"]

print("Token:", token[:50] + "...")

# Try /auth/me first to verify token works
auth_me_req = urllib.request.Request(
    "http://localhost:8000/auth/me",
    headers={"Authorization": f"Bearer {token}"},
    method="GET"
)

try:
    resp_me = urllib.request.urlopen(auth_me_req, timeout=10)
    print("AUTH/ME STATUS", resp_me.status)
    print("User:", json.loads(resp_me.read().decode()))
except urllib.error.HTTPError as e:
    print("AUTH/ME ERROR", e.code)
    print(e.read().decode())

# Now try /analysis with that same token
analysis_data = json.dumps({"raw_email": "From: test@test.com\nTo: user@test.com\nSubject: Hola\n\nTest body"}).encode()
analysis_req = urllib.request.Request(
    "http://localhost:8000/analysis",
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
except urllib.error.HTTPError as e:
    print("ANALYSIS ERROR", e.code)
    print(e.read().decode())
