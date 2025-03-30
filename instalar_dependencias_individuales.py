#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para instalar dependencias faltantes una por una

Este script instala las dependencias faltantes de DCS-Clipper de forma individual,
mostrando el progreso y manejando posibles errores para cada dependencia.
"""

import sys
import subprocess
import importlib
import time
import os

# Archivo de registro para la salida
LOG_FILE = 'instalacion_dependencias.log'

# Abrir archivo de registro
log_file = open(LOG_FILE, 'w', encoding='utf-8')

# Función para escribir en el archivo de registro y en la consola
def log(message):
    print(message)
    log_file.write(message + '\n')
    log_file.flush()  # Asegurar que se escriba inmediatamente

def print_header(text):
    log(f"\n=== {text} ===\n")

def print_success(text):
    log(f"✓ {text}")

def print_error(text):
    log(f"✗ {text}")

def print_info(text):
    log(f"{text}")

def instalar_dependencia(nombre_modulo, nombre_paquete, opciones_adicionales=None):
    print_header(f"Instalando {nombre_modulo}")
    
    # Verificar si ya está instalado
    try:
        if nombre_modulo == "PIL":
            # Caso especial para Pillow que se importa como PIL
            modulo = importlib.import_module(nombre_modulo)
        else:
            modulo = importlib.import_module(nombre_modulo.lower())
            
        version = getattr(modulo, "__version__", "desconocida")
        print_success(f"{nombre_modulo} ya está instalado (versión {version})")
        return True
    except ImportError:
        print_info(f"{nombre_modulo} no está instalado. Procediendo con la instalación...")
    
    # Preparar comando de instalación
    comando = [sys.executable, "-m", "pip", "install", nombre_paquete]
    if opciones_adicionales:
        comando.extend(opciones_adicionales)
    
    # Ejecutar instalación
    log(f"Ejecutando: {' '.join(comando)}")
    try:
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        log(resultado.stdout)
        
        # Verificar si la instalación fue exitosa
        try:
            if nombre_modulo == "PIL":
                modulo = importlib.import_module(nombre_modulo)
            else:
                modulo = importlib.import_module(nombre_modulo.lower())
                
            version = getattr(modulo, "__version__", "desconocida")
            print_success(f"{nombre_modulo} ha sido instalado correctamente (versión {version})")
            return True
        except ImportError:
            print_error(f"La instalación de {nombre_modulo} parece haber fallado.")
            return False
    except subprocess.CalledProcessError as e:
        print_error(f"Error durante la instalación de {nombre_modulo}")
        print(f"Salida de error:\n{e.stderr}")
        return False

def main():
    print_header("INSTALACIÓN DE DEPENDENCIAS INDIVIDUALES")
    log("Este script instalará las dependencias faltantes una por una.")
    log("Si alguna instalación falla, se continuará con la siguiente dependencia.")
    
    # Lista de dependencias a instalar (nombre del módulo, nombre del paquete, opciones adicionales)
    dependencias = [
        ("PyQt6", "PyQt6", ["--no-cache-dir"]),
        ("PIL", "pillow", None),
        ("tensorflow", "tensorflow", None),
        ("torch", "torch", None)
    ]
    
    resultados = []
    
    # Instalar cada dependencia
    for modulo, paquete, opciones in dependencias:
        exito = instalar_dependencia(modulo, paquete, opciones)
        resultados.append((modulo, exito))
        # Pequeña pausa entre instalaciones
        time.sleep(1)
    
    # Mostrar resumen
    print_header("RESUMEN DE INSTALACIÓN")
    for modulo, exito in resultados:
        if exito:
            print_success(f"{modulo}: Instalado correctamente")
        else:
            print_error(f"{modulo}: Falló la instalación")
    
    # Instrucciones adicionales para dependencias que fallaron
    fallidas = [modulo for modulo, exito in resultados if not exito]
    if fallidas:
        print_header("INSTRUCCIONES ADICIONALES")
        log("Para las dependencias que fallaron, puede intentar instalarlas manualmente:")
        
        if "PyQt6" in fallidas:
            print_info("\nPara PyQt6:")
            log("pip install PyQt6 --no-cache-dir")
            log("Asegúrese de tener instaladas las herramientas de desarrollo de C++")
        
        if "tensorflow" in fallidas:
            print_info("\nPara TensorFlow:")
            log("pip install tensorflow")
            log("O para versión con soporte GPU:")
            log("pip install tensorflow[gpu]")
        
        if "torch" in fallidas:
            print_info("\nPara PyTorch:")
            log("pip install torch torchvision torchaudio")
            log("O para versión con soporte NVIDIA GPU:")
            log("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    
    log("\nPara verificar si todas las dependencias están instaladas correctamente, ejecute:")
    log("python verificar_dependencias.py")
    
    # Cerrar el archivo de registro
    log_file.close()
    log(f"Se ha guardado un registro detallado en {LOG_FILE}")

if __name__ == "__main__":
    main()