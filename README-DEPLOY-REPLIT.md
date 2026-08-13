Despliegue rápido en Replit

1. Importar desde GitHub
- En Replit, selecciona "Create" → "Import from GitHub" y elige el repo `Darve99/BluePHish`.

2. Configuración de ejecución
- El proyecto ya incluye un archivo `.replit` que instala dependencias y arranca el backend:

```
cd backend && pip install -r requirements.txt && uvicorn main:app --host=0.0.0.0 --port $PORT
```

3. Variables y CORS
- Si vas a usar el frontend en Vercel, copia la URL pública de Replit y crea la variable `VITE_API_BASE_URL` en Vercel.
- Asegúrate de que `backend/main.py` permita CORS desde el dominio de Vercel o usa `*` para pruebas.

Limitaciones:
- Replit free puede hibernar por inactividad y tiene recursos limitados.
