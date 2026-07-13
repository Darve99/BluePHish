import urllib.request
import urllib.error
import json

# Step 1: Register/Login
login_data = json.dumps({"email": "test@example.com", "password": "pass123"}).encode()
login_req = urllib.request.Request(
    "http://localhost:8000/auth/login",
    data=login_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    resp = urllib.request.urlopen(login_req, timeout=10)
    login_result = json.loads(resp.read().decode())
    token = login_result.get("access_token")
    print("LOGIN OK, TOKEN:", token[:50] + "...")
    
    # Step 2: Analyze email
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
    
    resp2 = urllib.request.urlopen(analysis_req, timeout=10)
    print("ANALYSIS STATUS", resp2.status)
    result = json.loads(resp2.read().decode())
    print("Score:", result.get("score"))
    print("Risk level:", result.get("risk_level"))
    
except urllib.error.HTTPError as e:
    print("ERROR", e.code)
    print(e.read().decode())
except Exception as e:
    print("EXCEPTION", type(e).__name__, e)
