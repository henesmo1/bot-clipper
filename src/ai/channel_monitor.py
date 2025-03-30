"""Módulo para monitoreo en tiempo real de canales de YouTube y Twitch"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
from googleapiclient.discovery import build
from twitchAPI.twitch import Twitch
from .analyzer import ContentAnalyzer

# Importación de librerías adicionales para análisis de tendencias
import pandas as pd
import numpy as np
from transformers import pipeline

class ChannelMonitor:
    def __init__(self, youtube_api_key: str, twitch_client_id: str, twitch_secret: str, kick_api_key: str = None):
        """Inicializa el monitor de canales."""
        try:
            # Validación detallada de credenciales
            if not youtube_api_key:
                logging.error("Credencial faltante: YouTube API Key no proporcionada")
                raise ValueError("YouTube API Key no proporcionada o inválida")
            if not twitch_client_id:
                logging.error("Credencial faltante: Twitch Client ID no proporcionado")
                raise ValueError("Twitch Client ID no proporcionado o inválido")
            if not twitch_secret:
                logging.error("Credencial faltante: Twitch Client Secret no proporcionado")
                raise ValueError("Twitch Client Secret no proporcionado o inválido")
            if not kick_api_key:
                logging.warning("Credencial faltante: Kick API Key no proporcionada, algunas funciones estarán limitadas")
            
            # Inicialización de servicios con manejo de errores específicos
            try:
                self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
                logging.info("Servicio de YouTube inicializado correctamente")
            except Exception as yt_error:
                logging.error(f"Error al inicializar YouTube API: {str(yt_error)}")
                raise ValueError(f"Error de autenticación de YouTube: {str(yt_error)}")
            
            try:
                self.twitch = Twitch(twitch_client_id, twitch_secret)
                logging.info("Servicio de Twitch inicializado correctamente")
            except Exception as tw_error:
                logging.error(f"Error al inicializar Twitch API: {str(tw_error)}")
                raise ValueError(f"Error de autenticación de Twitch: {str(tw_error)}")
            
            self.analyzer = ContentAnalyzer()
            logging.info("Monitor de canales inicializado correctamente")
            
        except ValueError as ve:
            logging.error(f"Error de validación: {str(ve)}")
            raise
        except Exception as e:
            logging.error(f"Error inesperado al inicializar el monitor de canales: {str(e)}")
            raise ValueError(f"Error de inicialización: {str(e)}")
        self.monitored_channels = {
            'youtube': {'en': [], 'es': []},
            'twitch': {'en': [], 'es': []},
            'kick': {'en': [], 'es': []}
        }
        self.top_channels = {
            'youtube': {'en': [], 'es': []},
            'twitch': {'en': [], 'es': []},
            'kick': {'en': [], 'es': []}
        }
        self.kick_api_key = kick_api_key
        
        # Inicializar con datos de ejemplo para evitar tablas vacías
        self._initialize_sample_data()
        
    async def start_monitoring(self):
        """Inicia el monitoreo en tiempo real."""
        while True:
            try:
                await asyncio.gather(
                    self.update_youtube_rankings(),
                    self.update_twitch_rankings(),
                    self.analyze_top_channels()
                )
                await asyncio.sleep(300)  # Actualizar cada 5 minutos
            except Exception as e:
                logging.error(f"Error en monitoreo: {e}")
                await asyncio.sleep(60)
    
    async def update_youtube_rankings(self):
        """Actualiza el ranking de canales de YouTube."""
        try:
            for language in ['en', 'es']:
                # Buscar canales más populares por idioma
                request = self.youtube.search().list(
                    part='snippet',
                    type='channel',
                    regionCode='US' if language == 'en' else 'ES',
                    maxResults=10,
                    order='viewCount'
                )
                response = request.execute()
                
                channels = []
                for item in response['items']:
                    channel_id = item['snippet']['channelId']
                    stats = self.youtube.channels().list(
                        part='statistics',
                        id=channel_id
                    ).execute()
                    
                    channels.append({
                        'id': channel_id,
                        'title': item['snippet']['title'],
                        'subscribers': int(stats['items'][0]['statistics']['subscriberCount']),
                        'views': int(stats['items'][0]['statistics']['viewCount']),
                        'videos': int(stats['items'][0]['statistics']['videoCount']),
                        'last_updated': datetime.now().isoformat()
                    })
                
                self.top_channels['youtube'][language] = sorted(
                    channels,
                    key=lambda x: x['views'],
                    reverse=True
                )[:10]
                
        except Exception as e:
            logging.error(f"Error actualizando rankings de YouTube: {e}")
    
    async def update_twitch_rankings(self):
        """Actualiza el ranking de streamers de Twitch."""
        try:
            for language in ['en', 'es']:
                streams = await self.twitch.get_streams(
                    first=10,
                    language=[language]
                )
                
                channels = []
                for stream in streams:
                    channel = await self.twitch.get_users(user_ids=[stream.user_id])
                    channel_info = channel[0]
                    
                    channels.append({
                        'id': stream.user_id,
                        'title': channel_info.display_name,
                        'followers': await self.twitch.get_channel_followers(channel_info.id),
                        'views': stream.viewer_count,
                        'language': language,
                        'last_updated': datetime.now().isoformat()
                    })
                
                self.top_channels['twitch'][language] = sorted(
                    channels,
                    key=lambda x: x['views'],
                    reverse=True
                )[:10]
                
        except Exception as e:
            logging.error(f"Error actualizando rankings de Twitch: {e}")
    
    async def analyze_top_channels(self):
        """Analiza los 10 canales más vistos para generar clips."""
        try:
            # Combinar todos los canales y ordenar por vistas
            all_channels = []
            for platform in ['youtube', 'twitch']:
                for language in ['en', 'es']:
                    all_channels.extend(self.top_channels[platform][language])
            
            top_10 = sorted(all_channels, key=lambda x: x['views'], reverse=True)[:10]
            self.stats['total_monitored'] = len(top_10)
            
            for channel in top_10:
                if channel['id'] in self.monitored_channels:
                    continue
                    
                # Analizar último contenido del canal
                if platform == 'youtube':
                    videos = self.youtube.search().list(
                        part='snippet,statistics',
                        channelId=channel['id'],
                        order='date',
                        maxResults=5
                    ).execute()
                    
                    for video in videos['items']:
                        moments = self.analyzer.detect_key_moments(
                            f"https://youtube.com/watch?v={video['id']['videoId']}"
                        )
                        if moments:
                            self.viral_clips.extend(moments)
                            self.stats['viral_moments_detected'] += len(moments)
                            
                            # Actualizar estadísticas de YouTube
                            stats = video.get('statistics', {})
                            views = int(stats.get('viewCount', 0))
                            likes = int(stats.get('likeCount', 0))
                            self.stats['platform_stats']['youtube']['engagement_rate'] = \
                                (likes / views if views > 0 else 0)
                            self.stats['platform_stats']['youtube']['viral_rate'] = \
                                len([m for m in moments if m['viral_probability'] > 0.8]) / len(moments)
                            
                elif platform == 'twitch':
                    clips = await self.twitch.get_clips(
                        broadcaster_id=channel['id'],
                        first=5
                    )
                    
                    for clip in clips:
                        moments = self.analyzer.detect_key_moments(clip.url)
                        if moments:
                            self.viral_clips.extend(moments)
                            self.stats['viral_moments_detected'] += len(moments)
                            
                            # Actualizar estadísticas de Twitch
                            self.stats['platform_stats']['twitch']['engagement_rate'] = \
                                clip.view_count / (await self.twitch.get_channel_followers(channel['id']))
                            self.stats['platform_stats']['twitch']['viral_rate'] = \
                                len([m for m in moments if m['viral_probability'] > 0.8]) / len(moments)
                            
                self.monitored_channels[platform][language].append(channel['id'])
                
            # Actualizar timestamp
            self.stats['last_update'] = datetime.now().isoformat()
                
        except Exception as e:
            logging.error(f"Error analizando canales top: {e}")
    
    def _initialize_sample_data(self):
        """Inicializa datos de ejemplo para mostrar en las tablas antes de las llamadas a APIs."""
        # Datos de ejemplo para YouTube en inglés
        self.top_channels['youtube']['en'] = [
            {
                'id': 'UC-lHJZR3Gqxm24_Vd_AJ5Yw',
                'title': 'PewDiePie',
                'subscribers': 111000000,
                'views': 28000000000,
                'videos': 4200,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCX6OQ3DkcsbYNE6H8uQQuVA',
                'title': 'MrBeast',
                'subscribers': 97000000,
                'views': 16000000000,
                'videos': 700,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCiGm_E4ZwYSHV3bcW1pnSeQ',
                'title': 'Markiplier',
                'subscribers': 34000000,
                'views': 19000000000,
                'videos': 5500,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCYzPXprvl5Y-Sf0g4vX-m6g',
                'title': 'jacksepticeye',
                'subscribers': 29000000,
                'views': 15000000000,
                'videos': 4800,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCj5i58mCkAREDqFWlhaQbOw',
                'title': 'Dude Perfect',
                'subscribers': 58000000,
                'views': 14500000000,
                'videos': 350,
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        # Datos de ejemplo para YouTube en español
        self.top_channels['youtube']['es'] = [
            {
                'id': 'UCbW18JZRgko_mOGm5er8Yzg',
                'title': 'El Rubius OMG',
                'subscribers': 40000000,
                'views': 10000000000,
                'videos': 950,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCam8T03EOFBsNdR0thrFHdQ',
                'title': 'AuronPlay',
                'subscribers': 29000000,
                'views': 6500000000,
                'videos': 800,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCaHT88aobpcvRFEuy4v5Clg',
                'title': 'Fernanfloo',
                'subscribers': 45000000,
                'views': 9800000000,
                'videos': 750,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCrWvhVmt0Qac3HgsjQK62FQ',
                'title': 'TheGrefg',
                'subscribers': 17000000,
                'views': 3500000000,
                'videos': 1200,
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': 'UCXazgXDIYyWH-yXLAkcrFxw',
                'title': 'Vegetta777',
                'subscribers': 32000000,
                'views': 14000000000,
                'videos': 6500,
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        # Datos de ejemplo para Twitch en inglés
        self.top_channels['twitch']['en'] = [
            {
                'id': '141981764',
                'title': 'xQc',
                'followers': 11000000,
                'views': 250000,
                'language': 'en',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '26301881',
                'title': 'sodapoppin',
                'followers': 8500000,
                'views': 180000,
                'language': 'en',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '71092938',
                'title': 'pokimane',
                'followers': 9200000,
                'views': 165000,
                'language': 'en',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '19571641',
                'title': 'Ninja',
                'followers': 18500000,
                'views': 145000,
                'language': 'en',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '39276140',
                'title': 'shroud',
                'followers': 10200000,
                'views': 135000,
                'language': 'en',
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        # Datos de ejemplo para Twitch en español
        self.top_channels['twitch']['es'] = [
            {
                'id': '52551192',
                'title': 'Ibai',
                'followers': 11500000,
                'views': 220000,
                'language': 'es',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '41314141',
                'title': 'auronplay',
                'followers': 13800000,
                'views': 195000,
                'language': 'es',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '24147592',
                'title': 'TheGrefg',
                'followers': 9800000,
                'views': 175000,
                'language': 'es',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '120577122',
                'title': 'ElXokas',
                'followers': 3500000,
                'views': 120000,
                'language': 'es',
                'last_updated': datetime.now().isoformat()
            },
            {
                'id': '30486650',
                'title': 'Rubius',
                'followers': 12500000,
                'views': 110000,
                'language': 'es',
                'last_updated': datetime.now().isoformat()
            }
        ]
        
        # Inicializar algunos clips virales de ejemplo
        self.viral_clips = [
            {
                'id': 'sample_clip_1',
                'title': 'Momento épico en directo',
                'channel': 'Ibai',
                'platform': 'twitch',
                'url': 'https://clips.twitch.tv/example1',
                'timestamp': '00:15:30',
                'duration': 45,
                'views': 1250000,
                'viral_probability': 0.92,
                'detected_at': datetime.now().isoformat()
            },
            {
                'id': 'sample_clip_2',
                'title': 'Reacción increíble',
                'channel': 'AuronPlay',
                'platform': 'youtube',
                'url': 'https://youtube.com/watch?v=example2',
                'timestamp': '00:08:15',
                'duration': 30,
                'views': 980000,
                'viral_probability': 0.88,
                'detected_at': datetime.now().isoformat()
            },
            {
                'id': 'sample_clip_3',
                'title': 'Unexpected gaming moment',
                'channel': 'MrBeast',
                'platform': 'youtube',
                'url': 'https://youtube.com/watch?v=example3',
                'timestamp': '00:22:45',
                'duration': 60,
                'views': 2500000,
                'viral_probability': 0.95,
                'detected_at': datetime.now().isoformat()
            }
        ]
        
        # Inicializar estadísticas de ejemplo
        self.stats = {
            'total_monitored': 20,
            'viral_moments_detected': 3,
            'last_update': datetime.now().isoformat(),
            'platform_stats': {
                'youtube': {'viral_rate': 0.15, 'engagement_rate': 0.08},
                'twitch': {'viral_rate': 0.12, 'engagement_rate': 0.06}
            }
        }
        
        logging.info("Datos de ejemplo inicializados correctamente")
    
    def get_current_rankings(self) -> Dict:
        """Obtiene los rankings actuales de todos los canales."""
        return {
            'youtube': self.top_channels['youtube'],
            'twitch': self.top_channels['twitch'],
            'viral_clips': sorted(self.viral_clips, key=lambda x: x['viral_probability'], reverse=True),
            'stats': self.stats,
            'last_updated': datetime.now().isoformat()
        }