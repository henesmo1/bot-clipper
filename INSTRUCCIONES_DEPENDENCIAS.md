# Instrucciones para Gestionar Dependencias de DCS-Clipper

Este documento proporciona instrucciones para verificar, instalar y gestionar las dependencias necesarias para ejecutar DCS-Clipper correctamente.

## Scripts Disponibles

Se han creado varios scripts para facilitar la gestión de dependencias:

### 1. Verificar Dependencias

Para comprobar si todas las dependencias necesarias están instaladas:

```powershell
.\verificar_deps.ps1
```

Este script:
- Verifica todas las dependencias requeridas
- Muestra cuáles están instaladas y cuáles faltan
- Guarda los resultados en `verificacion_deps.txt`
- Proporciona instrucciones para instalar las dependencias faltantes

### 2. Instalar Dependencias

Para instalar todas las dependencias necesarias automáticamente:

```powershell
.\instalar_dependencias.ps1
```

Este script:
- Instala todas las dependencias listadas en `config/requirements.txt`
- Muestra el progreso de la instalación
- Informa si la instalación fue exitosa o si hubo errores

### 3. Iniciar la Aplicación con Verificación

Para iniciar la aplicación con verificación previa de dependencias:

```powershell
.\iniciar_app.ps1
```

Este script:
- Verifica las dependencias críticas antes de iniciar la aplicación
- Ofrece instalarlas automáticamente si faltan
- Inicia la aplicación si todas las dependencias están disponibles

## Solución de Problemas

Si encuentra errores al instalar dependencias:

1. **Problemas con PyQt6**: Asegúrese de tener instaladas las herramientas de desarrollo de C++
   ```powershell
   pip install PyQt6 --no-cache-dir
   ```

2. **Problemas con TensorFlow/Torch**: Estas bibliotecas pueden requerir versiones específicas según su hardware
   ```powershell
   # Para CPU solamente
   pip install tensorflow
   pip install torch torchvision torchaudio
   
   # Para NVIDIA GPU
   pip install tensorflow[gpu]
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Diagnóstico completo**: Para un diagnóstico más detallado del sistema
   ```powershell
   python diagnostico.py
   ```

## Ejecución Manual

Si prefiere instalar las dependencias manualmente:

```powershell
pip install -r config/requirements.txt
```

Y para ejecutar la aplicación directamente:

```powershell
python run_app.py
```

## Requisitos del Sistema

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Conexión a Internet para descargar paquetes