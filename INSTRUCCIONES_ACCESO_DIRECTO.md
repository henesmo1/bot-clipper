# Instrucciones para crear un acceso directo a DCS-Clipper

Este documento explica cómo crear un acceso directo en tu escritorio para ejecutar fácilmente la aplicación DCS-Clipper.

## Método 1: Usando el script PowerShell (Recomendado)

Hemos creado un script PowerShell que automatiza la creación del acceso directo. Para utilizarlo:

1. Abre PowerShell como administrador:
   - Haz clic derecho en el menú de inicio
   - Selecciona "Windows PowerShell (Admin)" o "Terminal (Admin)"

2. Navega hasta la carpeta del proyecto:
   ```powershell
   cd "C:\Users\Henry\CascadeProjects\DCS-Clipper"
   ```

3. Ejecuta el siguiente comando para permitir la ejecución de scripts:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

4. Ejecuta el script de creación del acceso directo:
   ```powershell
   .\crear_acceso_directo.ps1
   ```

5. Verifica que el acceso directo se haya creado en tu escritorio.

## Método 2: Creación manual

Si prefieres crear el acceso directo manualmente:

1. Haz clic derecho en el escritorio
2. Selecciona "Nuevo" > "Acceso directo"
3. En la ubicación del elemento, escribe:
   ```
   python "C:\Users\Henry\CascadeProjects\DCS-Clipper\run_app.py"
   ```
   (Ajusta la ruta si has instalado el proyecto en otra ubicación)
4. Haz clic en "Siguiente"
5. Nombra el acceso directo como "DCS-Clipper"
6. Haz clic en "Finalizar"
7. (Opcional) Para cambiar el icono, haz clic derecho en el acceso directo, selecciona "Propiedades" y luego "Cambiar icono"

## Solución de problemas

Si encuentras algún problema al crear el acceso directo:

- Asegúrate de que Python esté instalado y agregado al PATH del sistema
- Verifica que todas las dependencias del proyecto estén instaladas
- Comprueba que la ruta al proyecto sea correcta

Si el script PowerShell muestra un error, puedes intentar ejecutar la aplicación directamente desde la línea de comandos para identificar el problema:

```
python "C:\Users\Henry\CascadeProjects\DCS-Clipper\run_app.py"
```