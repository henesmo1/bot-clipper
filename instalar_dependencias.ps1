# Script PowerShell optimizado para instalar dependencias de DCS-Clipper

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
Write-ColorOutput "=== INSTALADOR DE DEPENDENCIAS DCS-Clipper ===" "Cyan"
Write-Host ""

# Verificar si Python está instalado
try {
    $pythonVersion = & python --version
    Write-ColorOutput "Python detectado: $pythonVersion" "Green"
} catch {
    Write-ColorOutput "Error: Python no está instalado o no está en el PATH." "Red"
    Write-ColorOutput "Descargue Python desde https://www.python.org/downloads/" "Yellow"
    exit 1
}

# Verificar si pip está disponible
try {
    $pipVersion = & python -m pip --version
    Write-ColorOutput "Pip detectado: $pipVersion" "Green"
} catch {
    Write-ColorOutput "Error: No se pudo ejecutar pip. Asegúrese de que pip esté instalado." "Red"
    Write-ColorOutput "Ejecute: python -m ensurepip --upgrade" "Yellow"
    exit 1
}

Write-Host ""
Write-ColorOutput "Instalando dependencias desde requirements.txt..." "Cyan"

# Instalar dependencias desde requirements.txt
try {
    & python -m pip install --upgrade pip
    & python -m pip install -r "$PSScriptRoot\config\requirements.txt"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-ColorOutput "✓ Todas las dependencias se instalaron correctamente." "Green"
    } else {
        Write-Host ""
        Write-ColorOutput "✗ Hubo errores durante la instalación." "Red"
        Write-ColorOutput "Revise los mensajes de error anteriores e intente nuevamente." "Yellow"
        exit 1
    }
} catch {
    Write-Host ""
    Write-ColorOutput "✗ Error crítico durante la instalación: $_" "Red"
    exit 1
}

Write-Host ""
Write-ColorOutput "Para verificar las dependencias instaladas, ejecute:" "Cyan"
Write-Host "  .\verificar_deps.ps1"

Write-Host ""
Write-ColorOutput "Para ejecutar la aplicación, use el comando:" "Cyan"
Write-Host "  python run_app.py"
