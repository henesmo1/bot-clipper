"""Módulo de descarga y análisis de videos virales"""

import os
import yt_dlp
import numpy as np
from typing import Dict, Optional, List, Tuple
import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self, output_path: str = "data/downloads", max_workers: int = 4):
        """
        Inicializa el sistema de descarga y análisis de videos virales.
        
        Args:
            output_path: Directorio para guardar los videos
            max_workers: Número máximo de workers para descargas paralelas
        """
        self.output_path = output_path
        self.logger = logging.getLogger("VideoDownloader")
        self.max_workers = max_workers
        
        # Crear directorios necesarios
        for dir_name in ['downloads', 'clips', 'trending']:
            path = os.path.join(output_path, dir_name)
            if not os.path.exists(path):
                os.makedirs(path)
            
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, 'downloads', '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'writesubtitles': True,
            'writeautomaticsub': True
        }
        
        # Métricas de rendimiento
        self.stats = {
            'downloads_total': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'viral_clips_found': 0,
            'last_update': datetime.now()
        }
    
    def download_video(self, url: str) -> Optional[Dict]:
        """Descarga un video y extrae información relevante."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                self.logger.info(f"Descargando video: {url}")
                info = ydl.extract_info(url, download=True)
                
                self.stats['downloads_total'] += 1
                self.stats['successful_downloads'] += 1
                
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'comment_count': info.get('comment_count'),
                    'upload_date': info.get('upload_date'),
                    'filename': ydl.prepare_filename(info),
                    'engagement_metrics': self._calculate_engagement_metrics(info)
                }
        except Exception as e:
            self.logger.error(f"Error descargando video {url}: {e}")
            self.stats['failed_downloads'] += 1
            return None
    
    def _calculate_engagement_metrics(self, video_info: Dict) -> Dict:
        """Calcula métricas de engagement para un video."""
        views = video_info.get('view_count', 0)
        likes = video_info.get('like_count', 0)
        comments = video_info.get('comment_count', 0)
        
        return {
            'engagement_rate': (likes + comments) / views if views > 0 else 0,
            'like_ratio': likes / views if views > 0 else 0,
            'comment_ratio': comments / views if views > 0 else 0,
            'viral_score': self._calculate_viral_score(video_info)
        }
    
    def _calculate_viral_score(self, video_info: Dict) -> float:
        """Calcula un score de viralidad basado en múltiples factores."""
        try:
            # Obtener métricas básicas
            views = video_info.get('view_count', 0)
            likes = video_info.get('like_count', 0)
            comments = video_info.get('comment_count', 0)
            duration = video_info.get('duration', 0)
            
            # Calcular velocidad de crecimiento
            upload_date = datetime.strptime(video_info.get('upload_date', '20200101'), '%Y%m%d')
            days_since_upload = (datetime.now() - upload_date).days or 1
            
            views_per_day = views / days_since_upload
            engagement_per_day = (likes + comments) / days_since_upload
            
            # Factores de viralidad
            view_factor = np.log10(views_per_day + 1) / 10
            engagement_factor = (likes + comments) / (views + 1)
            duration_factor = 1 - (duration / 3600)  # Favorece videos más cortos
            
            # Calcular score final (0-1)
            viral_score = (view_factor * 0.4 + 
                          engagement_factor * 0.4 + 
                          duration_factor * 0.2)
            
            return min(max(viral_score, 0), 1)
            
        except Exception as e:
            self.logger.error(f"Error calculando score viral: {e}")
            return 0.0
    
    def analyze_channel_performance(self, channel_url: str) -> Dict:
        """Analiza el rendimiento general de un canal."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                channel_info = ydl.extract_info(channel_url, download=False)
                
                # Calcular métricas clave
                videos = channel_info.get('entries', [])
                total_views = sum(video.get('view_count', 0) for video in videos)
                total_likes = sum(video.get('like_count', 0) for video in videos)
                
                return {
                    'subscriber_count': channel_info.get('subscriber_count', 0),
                    'total_views': total_views,
                    'total_likes': total_likes,
                    'engagement_rate': (total_likes / total_views) if total_views > 0 else 0,
                    'upload_frequency': self._calculate_upload_frequency(videos),
                    'best_performing_categories': self._analyze_top_categories(videos),
                    'viral_potential': self._analyze_viral_potential(videos)
                }
        except Exception as e:
            self.logger.error(f"Error analizando canal {channel_url}: {e}")
            return {}
    
    def _calculate_upload_frequency(self, videos: List[Dict]) -> str:
        """Calcula la frecuencia promedio de subida de videos."""
        if not videos or len(videos) < 2:
            return "Unknown"
            
        upload_dates = [datetime.strptime(v['upload_date'], '%Y%m%d') 
                       for v in videos if 'upload_date' in v]
        if len(upload_dates) < 2:
            return "Unknown"
            
        upload_dates.sort()
        total_days = (upload_dates[-1] - upload_dates[0]).days
        avg_days_between = total_days / (len(upload_dates) - 1)
        
        if avg_days_between <= 1:
            return "Daily"
        elif avg_days_between <= 7:
            return "Weekly"
        elif avg_days_between <= 30:
            return "Monthly"
        else:
            return "Irregular"
    
    def _analyze_top_categories(self, videos: List[Dict]) -> List[Dict]:
        """Identifica las categorías más exitosas del canal."""
        categories = {}
        for video in videos:
            category = video.get('categories', ['Unknown'])[0]
            if category not in categories:
                categories[category] = {
                    'views': 0,
                    'likes': 0,
                    'videos': 0,
                    'viral_videos': 0
                }
            
            stats = categories[category]
            stats['views'] += video.get('view_count', 0)
            stats['likes'] += video.get('like_count', 0)
            stats['videos'] += 1
            
            # Contar videos virales
            if self._calculate_viral_score(video) > 0.7:
                stats['viral_videos'] += 1
        
        # Calcular métricas por categoría
        for cat_stats in categories.values():
            cat_stats['engagement'] = (cat_stats['likes'] / cat_stats['views']) 
                                     if cat_stats['views'] > 0 else 0
            cat_stats['viral_rate'] = (cat_stats['viral_videos'] / cat_stats['videos']) 
                                     if cat_stats['videos'] > 0 else 0
        
        # Ordenar por potencial viral
        sorted_categories = sorted(
            categories.items(), 
            key=lambda x: (x[1]['viral_rate'], x[1]['engagement']), 
            reverse=True
        )
        
        return [{'category': k, **v} for k, v in sorted_categories]
    
    def _analyze_viral_potential(self, videos: List[Dict]) -> Dict:
        """Analiza el potencial viral general del canal."""
        if not videos:
            return {}
            
        viral_scores = [self._calculate_viral_score(v) for v in videos]
        viral_videos = sum(1 for score in viral_scores if score > 0.7)
        
        return {
            'average_viral_score': sum(viral_scores) / len(viral_scores),
            'viral_video_rate': viral_videos / len(videos),
            'viral_consistency': np.std(viral_scores),  # Menor = más consistente
            'trending_topics': self._extract_trending_topics(videos)
        }
    
    def _extract_trending_topics(self, videos: List[Dict]) -> List[Dict]:
        """Extrae y analiza temas tendencia del canal."""
        topics = {}
        for video in videos:
            # Analizar tags y títulos
            tags = video.get('tags', [])
            title_words = video.get('title', '').lower().split()
            
            for topic in tags + title_words:
                if topic not in topics:
                    topics[topic] = {
                        'count': 0,
                        'views': 0,
                        'viral_score': 0
                    }
                
                topics[topic]['count'] += 1
                topics[topic]['views'] += video.get('view_count', 0)
                topics[topic]['viral_score'] += self._calculate_viral_score(video)
        
        # Calcular relevancia de temas
        for topic_stats in topics.values():
            topic_stats['average_viral_score'] = (
                topic_stats['viral_score'] / topic_stats['count']
            )
        
        # Ordenar por relevancia
        sorted_topics = sorted(
            topics.items(),
            key=lambda x: (x[1]['average_viral_score'], x[1]['views']),
            reverse=True
        )
        
        return [{'topic': k, **v} for k, v in sorted_topics[:10]]  # Top 10 temas
    
    def download_channel_videos(self, 
                              channel_url: str,
                              limit: int = 10,
                              min_engagement: float = 0.1) -> list:
        """Descarga videos de un canal con potencial viral."""
        videos = []
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Analizar canal primero
                channel_analysis = self.analyze_channel_performance(channel_url)
                if not channel_analysis:
                    return []
                
                # Obtener videos del canal
                with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                    channel_info = ydl.extract_info(channel_url, download=False)
                    entries = channel_info.get('entries', [])
                
                # Analizar y filtrar videos en paralelo
                future_to_video = {}
                for entry in entries:
                    future = executor.submit(self.get_video_info, entry['url'])
                    future_to_video[future] = entry['url']
                
                # Recolectar resultados
                analyzed_videos = []
                for future in future_to_video:
                    video_info = future.result()
                    if video_info:
                        viral_score = self._calculate_viral_score(video_info)
                        engagement = video_info.get('like_count', 0) / \
                                    video_info.get('view_count', 1)
                        
                        if engagement >= min_engagement:
                            analyzed_videos.append({
                                'url': future_to_video[future],
                                'info': video_info,
                                'viral_score': viral_score,
                                'engagement': engagement
                            })
                
                # Ordenar por potencial viral y descargar los mejores
                analyzed_videos.sort(key=lambda x: x['viral_score'], reverse=True)
                for video in analyzed_videos[:limit]:
                    self.logger.info(
                        f"Descargando video viral (score: {video['viral_score']:.2f})"
                    )
                    video_data = self.download_video(video['url'])
                    if video_data:
                        videos.append(video_data)
                
        except Exception as e:
            self.logger.error(f"Error descargando canal {channel_url}: {e}")
            
        return videos
