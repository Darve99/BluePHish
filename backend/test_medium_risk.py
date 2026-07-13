import urllib.request
import urllib.error
import json

# Get fresh token
login_data = json.dumps({"email": "test@example.com", "password": "pass123"}).encode()
login_req = urllib.request.Request(
    "http://127.0.0.1:8000/auth/login",
    data=login_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
resp = urllib.request.urlopen(login_req, timeout=10)
token = json.loads(resp.read().decode())["access_token"]

# Correo de riesgo MEDIO: lenguaje urgente + URL sospechosa + verificación, pero sin solicitar credenciales explícitamente
medium_risk_email = """From: noreply@confirm-account.com
To: usuario@gmail.com
Subject: Acción requerida: Verifica tu cuenta
Content-Type: text/plain; charset="UTF-8"

Hola,

Hemos detectado un cambio en la configuración de tu cuenta. 
Por favor verifica tu identidad haciendo clic en el enlace a continuación:

https://confirm-account.com/verify?user=abc123

Este enlace expirará en 48 horas.

Gracias,
Equipo de Seguridad
"""

analysis_data = json.dumps({"raw_email": medium_risk_email}).encode()

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
    result = json.loads(resp_analysis.read().decode())
    
    print("=== MEDIUM RISK EMAIL ANALYSIS ===")
    print(f"Subject: {result.get('subject')}")
    print(f"Score: {result.get('score')}/100")
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"\nIndicators detected:")
    for ind in result.get('indicators', []):
        print(f"  - {ind.get('detail')} (weight: {ind.get('weight')})")
    
except urllib.error.HTTPError as e:
    print("ERROR", e.code)
    print(e.read().decode())
