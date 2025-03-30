#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar dependencias de DCS-Clipper

Este script verifica si las dependencias requeridas están instaladas
y muestra los resultados directamente en la consola.
"""

import sys
import os
import importlib
from datetime import datetime

# Colores para la salida en consola (compatible con Windows)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def verificar_dependencias():
    # Lista de dependencias a verificar (nombre del módulo, nombre del paquete pip)
    deps = [
        ("PyQt6", "PyQt6"),
        ("yaml", "pyyaml"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("requests", "requests"),
        ("PIL", "pillow"),  # Pillow se importa como PIL
        ("moviepy", "moviepy"),
        ("tensorflow", "tensorflow"),
        ("torch", "torch")
    ]
    
    print(f"{Colors.BOLD}=== Verificación de Dependencias de DCS-Clipper ==={Colors.RESET}\n")
    print(f"Python version: {sys.version}\n")
    print(f"{Colors.BOLD}Verificación de dependencias:{Colors.RESET}")
    
    faltantes = []
    
    for module_name, package_name in deps:
        try:
            # Intentar importar el módulo
            importlib.import_module(module_name.lower())
            print(f"{module_name}: {Colors.GREEN}OK{Colors.RESET}")
        except ImportError as e:
            error_msg = str(e)
            print(f"{module_name}: {Colors.RED}ERROR{Colors.RESET} - {error_msg}")
            faltantes.append((module_name, package_name))
    
    # Si hay dependencias faltantes, mostrar instrucciones
    if faltantes:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Dependencias faltantes:{Colors.RESET}")
        for module_name, package_name in faltantes:
            print(f"  - {module_name}")
        
        print(f"\n{Colors.BOLD}Para instalar las dependencias faltantes, ejecute:{Colors.RESET}")
        comando_pip = "pip install " + " ".join([package for _, package in faltantes])
        print(f"  {comando_pip}")
        
        print(f"\n{Colors.YELLOW}Nota: Después de instalar las dependencias, ejecute nuevamente este script para verificar.{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Todas las dependencias están instaladas correctamente.{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Para ejecutar la aplicación, use el comando:{Colors.RESET}")
    print("  python run_app.py")

if __name__ == "__main__":
    verificar_dependencias()