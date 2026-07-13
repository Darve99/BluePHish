import urllib.request
import urllib.error
import json

data = json.dumps({"name":"Test","email":"test@example.com","password":"pass123"}).encode()
req = urllib.request.Request(
    "http://localhost:8000/auth/register",
    data=data,
    headers={"Content-Type":"application/json"},
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
