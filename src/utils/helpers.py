"""
Funciones auxiliares para el sistema
"""

import os
import shutil
from typing import List, Dict, Optional
import yaml
from datetime import datetime, timedelta
import json

def load_yaml_config(file_path: str) -> Dict:
    """
    Carga un archivo de configuración YAML.
    
    Args:
        file_path: Ruta al archivo YAML
        
    Returns:
        Dict con la configuración
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Error cargando configuración: {e}")

def ensure_dir(directory: str):
    """
    Asegura que un directorio existe, lo crea si no.
    
    Args:
        directory: Ruta del directorio
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_directory(directory: str, max_age_days: int = 7):
    """
    Limpia archivos antiguos de un directorio.
    
    Args:
        directory: Directorio a limpiar
        max_age_days: Edad máxima de archivos en días
    """
    if not os.path.exists(directory):
        return
        
    now = datetime.now()
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_time = datetime.fromtimestamp(os.path.getctime(item_path))
            if now - file_time > timedelta(days=max_age_days):
                os.remove(item_path)

def get_file_size(file_path: str) -> int:
    """
    Obtiene el tamaño de un archivo en bytes.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Tamaño en bytes
    """
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def format_time(seconds: float) -> str:
    """
    Formatea segundos en formato HH:MM:SS.
    
    Args:
        seconds: Segundos a formatear
        
    Returns:
        String formateado
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def save_metadata(data: Dict, file_path: str):
    """
    Guarda metadatos en formato JSON.
    
    Args:
        data: Datos a guardar
        file_path: Ruta donde guardar
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error guardando metadatos: {e}")

def load_metadata(file_path: str) -> Optional[Dict]:
    """
    Carga metadatos desde un archivo JSON.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Dict con metadatos o None si hay error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def get_video_files(directory: str) -> List[str]:
    """
    Obtiene lista de archivos de video en un directorio.
    
    Args:
        directory: Directorio a buscar
        
    Returns:
        Lista de rutas a archivos de video
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    videos = []
    
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            videos.append(os.path.join(directory, file))
            
    return videos

def calculate_directory_size(directory: str) -> int:
    """
    Calcula el tamaño total de un directorio en bytes.
    
    Args:
        directory: Directorio a calcular
        
    Returns:
        Tamaño total en bytes
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def format_bytes(bytes: int) -> str:
    """
    Formatea bytes en formato legible.
    
    Args:
        bytes: Cantidad de bytes
        
    Returns:
        String formateado (e.g., "1.23 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"
