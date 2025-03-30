#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico para DCS-Clipper

Este script verifica las dependencias y la configuración necesaria
para ejecutar correctamente la aplicación DCS-Clipper.
"""

import sys
import os
import importlib
import platform
import subprocess
import traceback

# Colores para la salida en consola
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status, details=None):
    """Imprime un mensaje de estado con formato"""
    if status == "OK":
        status_color = Colors.GREEN
    elif status == "ADVERTENCIA":
        status_color = Colors.YELLOW
    else:  # ERROR
        status_color = Colors.RED
        
    print(f"{message}: {status_color}{status}{Colors.RESET}")
    if details:
        print(f"  → {details}")
    print()

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version.split()[0]
    print(f"Versión de Python: {version}")
    
    major, minor, _ = version.split('.')
    if int(major) < 3 or (int(major) == 3 and int(minor) < 8):
        print_status("Versión de Python compatible", "ERROR", 
                    "Se requiere Python 3.8 o superior")
        return False
    else:
        print_status("Versión de Python compatible", "OK")
        return True

def check_dependencies():
    """Verifica las dependencias requeridas"""
    print(f"{Colors.BOLD}Verificando dependencias...{Colors.RESET}")
    
    required_packages = [
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
    
    all_ok = True
    for package in required_packages:
        try:
            importlib.import_module(package.lower())
            print_status(f"Paquete {package}", "OK")
        except ImportError as e:
            print_status(f"Paquete {package}", "ERROR", f"No instalado: {str(e)}")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print(f"{Colors.BOLD}Verificando estructura del proyecto...{Colors.RESET}")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        "run_app.py",
        "src/gui/app.py",
        "src/core/brain.py",
        "config/settings.yaml"
    ]
    
    all_ok = True
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print_status(f"Archivo {file_path}", "OK")
        else:
            print_status(f"Archivo {file_path}", "ERROR", "No encontrado")
            all_ok = False
    
    return all_ok

def try_run_app():
    """Intenta ejecutar la aplicación y captura cualquier error"""
    print(f"{Colors.BOLD}Intentando ejecutar la aplicación...{Colors.RESET}")
    
    try:
        # Importar módulos necesarios
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Intentar importar los módulos principales
        print("Importando módulos...")
        from src.gui.app import QApplication, MainWindow, DCSBrain
        
        # Crear una aplicación de prueba
        print("Creando aplicación de prueba...")
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Inicializar el cerebro
        print("Inicializando DCSBrain...")
        app.brain = DCSBrain()
        
        # Crear ventana principal
        print("Creando ventana principal...")
        window = MainWindow()
        
        print_status("Aplicación inicializada correctamente", "OK", 
                    "La aplicación debería poder ejecutarse")
        return True
        
    except Exception as e:
        print_status("Error al ejecutar la aplicación", "ERROR", 
                    f"Excepción: {str(e)}")
        print("\nDetalles del error:")
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print(f"{Colors.BOLD}=== Diagnóstico de DCS-Clipper ==={Colors.RESET}\n")
    
    print(f"Sistema operativo: {platform.system()} {platform.release()}")
    print(f"Directorio actual: {os.getcwd()}")
    print()
    
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    structure_ok = check_project_structure()
    
    print(f"{Colors.BOLD}Resumen del diagnóstico:{Colors.RESET}")
    print_status("Versión de Python", "OK" if python_ok else "ERROR")
    print_status("Dependencias", "OK" if deps_ok else "ERROR")
    print_status("Estructura del proyecto", "OK" if structure_ok else "ERROR")
    
    if python_ok and deps_ok and structure_ok:
        app_ok = try_run_app()
        print_status("Ejecución de la aplicación", "OK" if app_ok else "ERROR")
        
        if app_ok:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ El diagnóstico no encontró problemas. La aplicación debería funcionar correctamente.{Colors.RESET}")
            print("\nPara ejecutar la aplicación, use el comando:")
            print("  python run_app.py")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Se encontraron errores al intentar ejecutar la aplicación.{Colors.RESET}")
            print("\nRevise los mensajes de error anteriores para más detalles.")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Se encontraron problemas en la configuración básica.{Colors.RESET}")
        print("\nSolucione los problemas indicados antes de intentar ejecutar la aplicación.")

if __name__ == "__main__":
    main()