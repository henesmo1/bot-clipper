"""
Sistema de logging personalizado
"""

import logging
import os
from datetime import datetime
from typing import Optional

class DCSLogger:
    def __init__(self, 
                 name: str,
                 log_dir: str = "logs",
                 level: int = logging.INFO):
        """
        Inicializa el logger.
        
        Args:
            name: Nombre del logger
            log_dir: Directorio para los logs
            level: Nivel de logging
        """
        self.name = name
        self.log_dir = log_dir
        self.level = level
        self.logger = None
        self.setup_logger()
        
    def setup_logger(self):
        """Configura el logger."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        log_file = os.path.join(
            self.log_dir,
            f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            # Handler para archivo
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.level)
            console_formatter = logging.Formatter(
                '%(levelname)s: %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
    def info(self, message: str):
        """Registra un mensaje de nivel INFO."""
        self.logger.info(message)
        
    def warning(self, message: str):
        """Registra un mensaje de nivel WARNING."""
        self.logger.warning(message)
        
    def error(self, message: str):
        """Registra un mensaje de nivel ERROR."""
        self.logger.error(message)
        
    def debug(self, message: str):
        """Registra un mensaje de nivel DEBUG."""
        self.logger.debug(message)
        
    def critical(self, message: str):
        """Registra un mensaje de nivel CRITICAL."""
        self.logger.critical(message)
        
    def log_exception(self, e: Exception, context: Optional[str] = None):
        """
        Registra una excepción con contexto opcional.
        
        Args:
            e: Excepción a registrar
            context: Contexto adicional
        """
        if context:
            self.error(f"{context}: {str(e)}")
        else:
            self.error(str(e))
        self.debug(f"Detalles de la excepción: {repr(e)}")
        
    def get_logger(self) -> logging.Logger:
        """Obtiene el objeto logger."""
        return self.logger
