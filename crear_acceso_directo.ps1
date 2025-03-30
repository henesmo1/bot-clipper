# Script para crear un acceso directo a DCS-Clipper

# Obtener la ruta del escritorio
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Ruta completa al archivo run_app.py
$appPath = Join-Path -Path $PSScriptRoot -ChildPath "run_app.py"

# Obtener la ruta de Python (asumiendo que está en el PATH)
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    $pythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
}

if (-not $pythonPath) {
    Write-Host "Error: No se pudo encontrar Python instalado. Por favor, instale Python y asegúrese de que esté en el PATH." -ForegroundColor Red
    exit 1
}

# Crear el objeto de acceso directo
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$desktopPath\clipper.lnk")

  # Configurar el acceso directo
  $Shortcut.TargetPath = "$pythonPath"
  $Shortcut.Arguments = "`"$appPath`""
  $Shortcut.WindowStyle = 1 # Ventana normal
  $Shortcut.WorkingDirectory = $PSScriptRoot
  $Shortcut.Description = "Aplicación DCS-Clipper para gestión de contenido para redes sociales"

  # Intentar establecer un icono (usando el icono de Python por defecto)
  $pythonDirPath = Split-Path -Path $pythonPath -Parent
  $possibleIconPath = Join-Path -Path $pythonDirPath -ChildPath "DLLs\py.ico"
  if (Test-Path $possibleIconPath) {
      $Shortcut.IconLocation = $possibleIconPath
  }

  # Guardar el acceso directo
  $Shortcut.Save()

  # Verificar si se creó correctamente
  if (Test-Path "$desktopPath\clipper.lnk") {
      Write-Host "Acceso directo creado exitosamente en el escritorio. La salida de la consola se mostrará en la ventana de la aplicación." -ForegroundColor Green
      Write-Host "Si la aplicación no se inicia correctamente, verifique:"
      Write-Host "1. Que Python esté instalado y en el PATH" -ForegroundColor Yellow
      Write-Host "2. Que todas las dependencias estén instaladas (ejecute instalar_dependencias.ps1)" -ForegroundColor Yellow
      Write-Host "3. Que la ruta al proyecto sea correcta" -ForegroundColor Yellow
      Read-Host -Prompt "Presione Enter para continuar..."
  } else {
      Write-Host "Error: No se pudo crear el acceso directo." -ForegroundColor Red
      Read-Host -Prompt "Presione Enter para salir..."
  }