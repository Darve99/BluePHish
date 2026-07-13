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

# Tu email de phishing
phishing_email = """From: seguridad@banconacional.com
To: cliente@example.com
Subject: ⚠️ Acción requerida: Su cuenta será suspendida en las próximas 24 horas
Content-Type: text/plain; charset="UTF-8"

Estimado cliente,

Hemos detectado actividad inusual en su cuenta durante las últimas horas. Por motivos de seguridad, el acceso ha sido restringido temporalmente.

Para evitar la suspensión permanente de su cuenta, debe verificar su identidad de inmediato haciendo clic en el siguiente enlace:

https://seguridad-banc0-verificacion.com/login

Una vez complete la verificación, su cuenta será reactivada automáticamente.

Si no realiza este proceso dentro de las próximas 24 horas, su cuenta será bloqueada y todos los servicios asociados quedarán suspendidos.

Como parte del proceso de validación, tenga a la mano:
- Documento de identidad
- Usuario
- Contraseña
- Código de autenticación enviado por SMS

Si necesita ayuda, responda directamente a este correo.

Atentamente,

Departamento de Seguridad Digital
Banco Nacional de Colombia

Este es un mensaje automático. No responda a este correo.
"""

analysis_data = json.dumps({"raw_email": phishing_email}).encode()

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
    
    print("=== ANALYSIS RESULT ===")
    print(f"Subject: {result.get('subject')}")
    print(f"From: {result.get('from')}")
    print(f"Score: {result.get('score')}/100")
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"Summary: {result.get('summary')}")
    print(f"\nURLs detected: {result.get('urls')}")
    print(f"\nIndicators:")
    for ind in result.get('indicators', [])[:5]:
        print(f"  - {ind}")
    
except urllib.error.HTTPError as e:
    print("ERROR", e.code)
    print(e.read().decode())
