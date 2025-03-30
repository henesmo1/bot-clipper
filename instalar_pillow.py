#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para instalar y verificar Pillow (PIL)

Este script explica la diferencia entre PIL y Pillow,
verifica si Pillow está instalado correctamente y lo instala si es necesario.
"""

import sys
import subprocess
import importlib

# Colores para la salida en consola
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{text}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}{Colors.BOLD}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}{Colors.BOLD}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}{text}{Colors.RESET}")

def instalar_pillow():
    print_header("=== Información sobre PIL y Pillow ===")
    
    print("PIL (Python Imaging Library) es una biblioteca para procesamiento de imágenes en Python.")
    print("Sin embargo, el proyecto original PIL está obsoleto y ha sido reemplazado por Pillow.")
    print("\nCuando intentas instalar con 'pip install pil', no funciona porque:")
    print_info("  - El nombre correcto del paquete es 'pillow', no 'pil'")
    print_info("  - En Python, se sigue importando como 'PIL', pero se instala como 'pillow'")
    
    print("\nPara instalar Pillow correctamente, usa:")
    print_info("  pip install pillow")
    
    print("\nEn los scripts de Python, se sigue importando como:")
    print_info("  import PIL")
    print_info("  from PIL import Image")
    
    print_header("Verificando si Pillow está instalado en tu sistema...")
    
    try:
        # Intentar importar PIL
        PIL = importlib.import_module("PIL")
        version = getattr(PIL, "__version__", "desconocida")
        print_success(f"Pillow está instalado correctamente (versión {version})")
    except ImportError:
        print_error("Pillow no está instalado.")
        
        respuesta = input("\n¿Deseas instalar Pillow ahora? (s/n): ").lower()
        if respuesta in ["s", "si", "sí", "y", "yes"]:
            print("\nInstalando Pillow...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pillow"], check=True)
                
                try:
                    # Verificar si la instalación fue exitosa
                    PIL = importlib.import_module("PIL")
                    version = getattr(PIL, "__version__", "desconocida")
                    print_success(f"Pillow ha sido instalado correctamente (versión {version})")
                except ImportError:
                    print_error("Hubo un problema al instalar Pillow.")
                    print_info("\nPor favor, intenta manualmente:\n  pip install pillow")
            except subprocess.CalledProcessError:
                print_error("Error durante la instalación de Pillow.")
                print_info("\nPuedes intentar con opciones adicionales:\n  pip install pillow --no-cache-dir")
        else:
            print("\nInstalación cancelada.")
    
    print("\nRecuerda: En requirements.txt ya está incluido 'pillow~=10.1.0', así que")
    print("al instalar todas las dependencias con 'pip install -r config/requirements.txt'")
    print("también se instalará Pillow automáticamente.")

if __name__ == "__main__":
    instalar_pillow()