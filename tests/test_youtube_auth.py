"""
Script de prueba para verificar la autenticación de YouTube
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def test_youtube_auth():
    # Ruta al archivo de credenciales
    client_secrets_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                     "config", "credentials", "client_secrets.json")
    
    # Verificar que el archivo existe
    if not os.path.exists(client_secrets_file):
        print(f"Error: No se encuentra el archivo de credenciales en {client_secrets_file}")
        return False
    
    # Scopes necesarios
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.force-ssl'
    ]
    
    try:
        # Iniciar el flujo de autenticación
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, SCOPES)
        
        # Esto abrirá tu navegador para autenticar
        credentials = flow.run_local_server(port=0)
        
        # Crear el servicio de YouTube
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Intentar obtener información del canal
        request = youtube.channels().list(
            part="snippet",
            mine=True
        )
        response = request.execute()
        
        if response['items']:
            channel = response['items'][0]['snippet']
            print(f"\n¡Autenticación exitosa!")
            print(f"Canal: {channel['title']}")
            print(f"Descripción: {channel['description']}")
            return True
            
    except HttpError as e:
        print(f"Error de HTTP: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Permitir OAuth en entorno de desarrollo
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    test_youtube_auth()
