"""
Módulo de subida de videos a plataformas sociales
"""

import os
from typing import Dict, List, Optional
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

class SocialMediaUploader:
    def __init__(self, credentials_path: str):
        """
        Inicializa el uploader de redes sociales.
        
        Args:
            credentials_path: Ruta al archivo de credenciales
        """
        self.credentials_path = credentials_path
        self.logger = logging.getLogger("SocialMediaUploader")
        self.youtube = None
        self.initialize_youtube()
        
    def initialize_youtube(self):
        """Inicializa la conexión con YouTube."""
        try:
            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
            
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
            
            self.youtube = build('youtube', 'v3', credentials=credentials)
            self.logger.info("Conexión con YouTube establecida")
            
        except Exception as e:
            self.logger.error(f"Error inicializando YouTube: {e}")
            
    def upload_to_youtube(self,
                         video_path: str,
                         title: str,
                         description: str,
                         tags: List[str] = None,
                         privacy_status: str = "private",
                         schedule_time: Optional[datetime] = None) -> Optional[str]:
        """
        Sube un video a YouTube con programación opcional.
        
        Args:
            video_path: Ruta al archivo de video
            title: Título del video
            description: Descripción del video
            tags: Lista de tags
            privacy_status: Estado de privacidad
            schedule_time: Fecha y hora programada para publicación
            
        Returns:
            ID del video subido o None si hay error
        """
        if not self.youtube:
            self.logger.error("YouTube no está inicializado")
            return None
            
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': '22'  # People & Blogs
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False,
                    'publishAt': schedule_time.isoformat() if schedule_time else None
                }
            }
            
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=MediaFileUpload(
                    video_path, 
                    chunksize=-1, 
                    resumable=True
                )
            )
            
            self.logger.info(f"Subiendo video: {title}")
            response = insert_request.execute()
            video_id = response.get('id')
            
            if video_id:
                self.logger.info(f"Video subido exitosamente: {video_id}")
                return video_id
            else:
                self.logger.error("Error: No se recibió ID del video")
                return None
                
        except Exception as e:
            self.logger.error(f"Error subiendo video: {e}")
            return None
            
    def update_video_metadata(self,
                            video_id: str,
                            title: str = None,
                            description: str = None,
                            tags: List[str] = None) -> bool:
        """
        Actualiza los metadatos de un video.
        
        Args:
            video_id: ID del video
            title: Nuevo título
            description: Nueva descripción
            tags: Nuevos tags
            
        Returns:
            True si la actualización fue exitosa
        """
        if not self.youtube:
            return False
            
        try:
            body = {
                'id': video_id,
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags
                }
            }
            
            self.youtube.videos().update(
                part='snippet',
                body=body
            ).execute()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error actualizando metadatos: {e}")
            return False
            
    def get_video_statistics(self, video_id: str) -> Optional[Dict]:
        """
        Obtiene estadísticas de un video.
        
        Args:
            video_id: ID del video
            
        Returns:
            Dict con estadísticas o None si hay error
        """
        if not self.youtube:
            return None
            
        try:
            response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            
            if response['items']:
                return response['items'][0]['statistics']
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return None
