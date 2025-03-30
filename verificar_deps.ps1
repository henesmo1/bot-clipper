# Script PowerShell para verificar dependencias de DCS-Clipper

# Función para mostrar texto con colores
function Write-ColorOutput {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Text,
        
        [Parameter(Mandatory=$false)]
        [string]$ForegroundColor = "White"
    )
    
    Write-Host $Text -ForegroundColor $ForegroundColor
}

# Encabezado
Write-ColorOutput "=== Verificación de Dependencias de DCS-Clipper ===" "Cyan"
Write-Host ""

# Obtener versión de Python
$pythonVersion = & python -c "import sys; print(sys.version)"
Write-Host "Python version: $pythonVersion"
Write-Host ""

Write-ColorOutput "Verificación de dependencias:" "Cyan"

# Lista de dependencias a verificar
$deps = @(
    "PyQt6",
    "yaml",
    "numpy",
    "pandas",
    "requests",
    "PIL",  # Pillow se importa como PIL
    "moviepy",
    "tensorflow",
    "torch"
)

# Archivo para guardar resultados
$outputFile = "verificacion_deps.txt"
"Python version: $pythonVersion`n`nVerificación de dependencias:" | Out-File -FilePath $outputFile -Encoding utf8

$faltantes = @()

# Verificar cada dependencia
foreach ($dep in $deps) {
    $result = & python -c "import sys; import importlib; try: importlib.import_module('$($dep.ToLower())'); print('OK'); sys.exit(0); except ImportError as e: print(str(e)); sys.exit(1)" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "${dep}: OK" -ForegroundColor "Green"
        "${dep}: OK" | Out-File -FilePath $outputFile -Append -Encoding utf8
    } else {
        Write-ColorOutput "${dep}: ERROR - $result" -ForegroundColor "Red"
        "${dep}: ERROR - $result" | Out-File -FilePath $outputFile -Append -Encoding utf8
        $faltantes += $dep
    }
}

Write-Host ""

# Si hay dependencias faltantes, mostrar instrucciones
if ($faltantes.Count -gt 0) {
    Write-ColorOutput "Dependencias faltantes:" "Yellow"
    foreach ($dep in $faltantes) {
        Write-Host "  - $dep"
    }
    
    Write-Host ""
    Write-ColorOutput "Para instalar las dependencias faltantes, ejecute:" "Yellow"
    
    # Mapeo de nombres de módulos a paquetes pip
    $pipPackages = @{
        "PyQt6" = "PyQt6"
        "yaml" = "pyyaml"
        "numpy" = "numpy"
        "pandas" = "pandas"
        "requests" = "requests"
        "PIL" = "pillow"
        "moviepy" = "moviepy"
        "tensorflow" = "tensorflow"
        "torch" = "torch"
    }
    
    $installCmd = "pip install"
    foreach ($dep in $faltantes) {
        $installCmd += " $($pipPackages[$dep])"
    }
    
    Write-Host "  $installCmd"
    
    Write-Host ""
    Write-ColorOutput "Nota: Después de instalar las dependencias, ejecute nuevamente este script para verificar." "Yellow"
} else {
    Write-ColorOutput "✓ Todas las dependencias están instaladas correctamente." "Green"
}

Write-Host ""
Write-ColorOutput "Para ejecutar la aplicación, use el comando:" "Cyan"
Write-Host "  python run_app.py"

Write-Host ""
Write-ColorOutput "Resultados guardados en: $outputFile" -ForegroundColor "Cyan"

if ($faltantes.Count -gt 0) {
    Write-ColorOutput "Dependencias faltantes:" "Yellow"
    foreach ($dep in $faltantes) {
        Write-Host "  - $dep"
    }
    
    Write-Host ""
    Write-ColorOutput "Para instalar las dependencias faltantes, ejecute:" "Yellow"
    
    $installCmd = "pip install"
    foreach ($dep in $faltantes) {
        $installCmd += " $($pipPackages[$dep])"
    }
    
    Write-Host "  $installCmd"
    
    Write-Host ""
    Write-ColorOutput "Nota: Después de instalar las dependencias, ejecute nuevamente este script para verificar." "Yellow"
} else {
    Write-ColorOutput "✓ Todas las dependencias están instaladas correctamente." "Green"
}