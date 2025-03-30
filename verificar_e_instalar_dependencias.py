#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar e instalar dependencias de DCS-Clipper

Este script verifica si las dependencias requeridas están instaladas,
genera un archivo de texto con los resultados y ofrece instrucciones
para instalar las dependencias faltantes.
"""

import sys
import os
import importlib
import subprocess
from datetime import datetime

def verificar_dependencias(instalar=False):
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
    
    # Crear archivo de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'verificacion_deps_{timestamp}.txt'
    
    faltantes = []
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Escribir versión de Python
        f.write(f'Python version: {sys.version}\n\n')
        
        # Verificar dependencias
        f.write('Verificación de dependencias:\n')
        for module_name, package_name in deps:
            try:
                # Intentar importar el módulo
                importlib.import_module(module_name.lower())
                f.write(f'{module_name}: OK\n')
            except ImportError as e:
                error_msg = str(e)
                f.write(f'{module_name}: ERROR - {error_msg}\n')
                faltantes.append((module_name, package_name))
    
    print(f"Verificación completada. Resultados guardados en '{output_file}'")
    
    # Si hay dependencias faltantes, mostrar instrucciones
    if faltantes:
        print("\nDependencias faltantes:")
        for module_name, package_name in faltantes:
            print(f"  - {module_name}")
        
        print("\nPara instalar las dependencias faltantes, ejecute:")
        comando_pip = "pip install " + " ".join([package for _, package in faltantes])
        print(f"  {comando_pip}")
        
        # Opción para instalar automáticamente
        if instalar:
            print("\nInstalando dependencias faltantes...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install"] + 
                              [package for _, package in faltantes],
                              check=True)
                print("Instalación completada.")
            except subprocess.CalledProcessError as e:
                print(f"Error durante la instalación: {e}")
    else:
        print("\nTodas las dependencias están instaladas correctamente.")

def main():
    # Verificar si se solicita instalación automática
    instalar = False
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["-i", "--install"]:
        instalar = True
        print("Modo de instalación automática activado.")
    
    verificar_dependencias(instalar)
    
    print("\nPara ejecutar la aplicación, use el comando:")
    print("  python run_app.py")

if __name__ == "__main__":
    main()