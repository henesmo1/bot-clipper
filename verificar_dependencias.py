#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar dependencias de DCS-Clipper

Este script verifica si las dependencias requeridas están instaladas
y genera un archivo de texto con los resultados.
"""

import sys
import os
import importlib

def verificar_dependencias():
    # Lista de dependencias a verificar
    deps = [
        "PyQt6",
        "yaml",
        "numpy",
        "pandas",
        "requests",
        "pillow",
        "moviepy",
        "tensorflow",
        "torch"
    ]
    
    # Crear archivo de salida
    with open('verificacion_deps.txt', 'w', encoding='utf-8') as f:
        # Escribir versión de Python
        f.write(f'Python version: {sys.version}\n\n')
        
        # Verificar dependencias
        f.write('Verificación de dependencias:\n')
        for dep in deps:
            try:
                # Intentar importar el módulo
                importlib.import_module(dep.lower())
                f.write(f'{dep}: OK\n')
            except ImportError as e:
                f.write(f'{dep}: ERROR - {str(e)}\n')

if __name__ == "__main__":
    verificar_dependencias()
    print("Verificación completada. Resultados guardados en 'verificacion_deps.txt'")