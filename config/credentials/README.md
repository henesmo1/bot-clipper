# Credenciales de YouTube

Este directorio debe contener los siguientes archivos:
- `client_secrets.json`: Credenciales de OAuth 2.0 para la API de YouTube
- `youtube_token.pickle`: Token de acceso (se generará automáticamente)

## Pasos para configurar:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de YouTube Data v3
4. En la sección de credenciales:
   - Crea credenciales OAuth 2.0
   - Tipo: Aplicación de escritorio
   - Descarga el archivo JSON
   - Renómbralo a `client_secrets.json` y colócalo en este directorio

IMPORTANTE: No subas estos archivos a control de versiones.
