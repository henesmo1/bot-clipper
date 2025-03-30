"""
Módulo de edición automática de clips virales
"""

import os
import random
from typing import List, Dict, Optional, Tuple
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, vfx
from moviepy.video.tools.subtitles import SubtitlesClip
import numpy as np
import cv2

# Importación de librerías adicionales para edición avanzada
import ffmpeg

class VideoEditor:
    def __init__(self, config: Dict):
        """
        Inicializa el editor de videos.
        
        Args:
            config: Configuración del editor
        """
        self.config = config
        self.effects = {
            'fade_in': self._apply_fade_in,
            'fade_out': self._apply_fade_out,
            'zoom': self._apply_zoom,
            'text_overlay': self._apply_text_overlay
        }
        
    def create_clip(self, 
                   video_path: str,
                   start_time: float,
                   end_time: float,
                   effects: List[Dict] = None) -> Optional[VideoFileClip]:
        """
        Crea un clip a partir de un video.
        
        Args:
            video_path: Ruta al video original
            start_time: Tiempo de inicio del clip
            end_time: Tiempo final del clip
            effects: Lista de efectos a aplicar
            
        Returns:
            VideoFileClip editado o None si hay error
        """
        try:
            video = VideoFileClip(video_path)
            clip = video.subclip(start_time, end_time)
            
            if effects:
                for effect in effects:
                    effect_name = effect.get('name')
                    effect_params = effect.get('params', {})
                    if effect_name in self.effects:
                        clip = self.effects[effect_name](clip, **effect_params)
                        
            return clip
            
        except Exception as e:
            print(f"Error creando clip: {e}")
            return None
            
    def _apply_fade_in(self, clip: VideoFileClip, duration: float = 1.0) -> VideoFileClip:
        """Aplica efecto de fade in."""
        return clip.fadein(duration)
        
    def _apply_fade_out(self, clip: VideoFileClip, duration: float = 1.0) -> VideoFileClip:
        """Aplica efecto de fade out."""
        return clip.fadeout(duration)
        
    def _apply_zoom(self, 
                   clip: VideoFileClip,
                   start_scale: float = 1.0,
                   end_scale: float = 1.5) -> VideoFileClip:
        """Aplica efecto de zoom."""
        def zoom(get_frame, t):
            scale = start_scale + (end_scale - start_scale) * t / clip.duration
            frame = get_frame(t)
            height, width = frame.shape[:2]
            center = (width/2, height/2)
            M = cv2.getRotationMatrix2D(center, 0, scale)
            return cv2.warpAffine(frame, M, (width, height))
            
        return clip.fl(zoom)
        
    def _apply_text_overlay(self,
                          clip: VideoFileClip,
                          text: str,
                          position: str = 'bottom',
                          fontsize: int = 30) -> VideoFileClip:
        """Aplica texto sobre el video."""
        txt_clip = TextClip(text, fontsize=fontsize, color='white')
        
        if position == 'bottom':
            txt_clip = txt_clip.set_position(('center', 'bottom'))
        elif position == 'top':
            txt_clip = txt_clip.set_position(('center', 'top'))
            
        return concatenate_videoclips([clip, txt_clip.set_duration(clip.duration)])
        
    def add_watermark(self,
                     clip: VideoFileClip,
                     watermark_path: str,
                     position: str = 'bottom-right',
                     opacity: float = 0.7) -> VideoFileClip:
        """
        Añade una marca de agua al video.
        
        Args:
            clip: Video clip
            watermark_path: Ruta a la imagen de marca de agua
            position: Posición de la marca de agua
            opacity: Opacidad de la marca de agua (0-1)
            
        Returns:
            Video con marca de agua
        """
        try:
            # Cargar y redimensionar marca de agua
            watermark = (VideoFileClip(watermark_path)
                        .resize(width=clip.w//4)  # Tamaño relativo al video
                        .set_opacity(opacity))
            
            # Calcular posición
            margin = 20  # píxeles desde el borde
            if position == 'bottom-right':
                pos = ('right', 'bottom')
            elif position == 'bottom-left':
                pos = ('left', 'bottom')
            elif position == 'top-right':
                pos = ('right', 'top')
            elif position == 'top-left':
                pos = ('left', 'top')
            else:
                pos = ('center', 'center')
                
            # Aplicar marca de agua
            watermark = watermark.set_position(pos).set_duration(clip.duration)
            return CompositeVideoClip([clip, watermark])
            
        except Exception as e:
            logging.error(f"Error añadiendo marca de agua: {e}")
            return clip
        
    def compile_video(self,
                     clips: List[VideoFileClip],
                     output_path: str,
                     add_transitions: bool = True) -> bool:
        """
        Compila múltiples clips en un solo video.
        
        Args:
            clips: Lista de clips a compilar
            output_path: Ruta donde guardar el video final
            add_transitions: Si se deben añadir transiciones
            
        Returns:
            True si la compilación fue exitosa
        """
        try:
            if not clips:
                logging.error("No hay clips para compilar")
                return False
                
            if add_transitions:
                final_clips = []
                transition_duration = 0.5
                
                for i, clip in enumerate(clips):
                    # Añadir fade in al primer clip
                    if i == 0:
                        clip = clip.fadein(transition_duration)
                    
                    # Añadir fade out al último clip
                    if i == len(clips) - 1:
                        clip = clip.fadeout(transition_duration)
                    
                    # Añadir crossfade entre clips
                    if i > 0:
                        clip = clip.crossfadein(transition_duration)
                    
                    final_clips.append(clip)
                
                final_clip = concatenate_videoclips(final_clips, 
                                                   method="compose")
            else:
                final_clip = concatenate_videoclips(clips)
            
            # Configurar codec y bitrate para mejor calidad
            final_clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                bitrate='8000k',
                threads=4,
                logger=None
            )
            return True
            
        except Exception as e:
            logging.error(f"Error compilando video: {e}")
            return False
