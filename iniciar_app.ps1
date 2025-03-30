# Script PowerShell para iniciar DCS-Clipper con verificación de dependencias

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
Write-ColorOutput "=== Iniciando DCS-Clipper ===" "Cyan"
Write-Host ""

# Verificar dependencias críticas
$dependenciasCriticas = @("PyQt6", "yaml", "numpy")
$faltantes = @()

Write-ColorOutput "Verificando dependencias críticas..." "Cyan"
foreach ($dep in $dependenciasCriticas) {
    $result = & python -c "import sys; import importlib; try: importlib.import_module('$($dep.ToLower())'); sys.exit(0); except ImportError: sys.exit(1)" 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        $faltantes += $dep
# Si faltan dependencias críticas, ofrecer instalarlas
if ($faltantes.Count -gt 0) {
    Write-ColorOutput "✗ Faltan dependencias críticas para ejecutar la aplicación:" "Red"
    foreach ($dep in $faltantes) {
        Write-Host "  - $dep"
    }
    
    Write-Host ""
    Write-ColorOutput "¿Desea instalar las dependencias faltantes ahora? (S/N)" "Yellow"
    $respuesta = Read-Host
    
    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        Write-Host ""
        Write-ColorOutput "Instalando dependencias..." "Cyan"
        & python -m pip install -r "$PSScriptRoot\config\requirements.txt"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-ColorOutput "✓ Dependencias instaladas correctamente." "Green"
        } else {
            Write-Host ""
            Write-ColorOutput "✗ Hubo errores durante la instalación." "Red"
            Write-ColorOutput "Por favor, ejecute manualmente: .\instalar_dependencias.ps1" "Yellow"
            exit 1
        }
}

# Iniciar la aplicación
Write-Host
Write-ColorOutput "Iniciando DCS-Clipper..." "Cyan"
try {
    & python "$PSScriptRoot\run_app.py"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-ColorOutput "✗ La aplicación se cerró con errores (código $LASTEXITCODE)." "Red"
        Write-ColorOutput "Para diagnóstico completo, ejecute: python diagnostico.py" "Yellow"
    }
} catch {
    Write-Host ""
    Write-ColorOutput "✗ Error al iniciar la aplicación: $_" "Red"
    Write-ColorOutput "Para diagnóstico completo, ejecute: python diagnostico.py" "Yellow"
}
}
}
}
}
}

# Iniciar la aplicación
Write-Host
Write-ColorOutput "Iniciando DCS-Clipper..." "Cyan"
try {
    & python "$PSScriptRoot\run_app.py"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-ColorOutput "✗ La aplicación se cerró con errores (código $LASTEXITCODE)." "Red"
        Write-ColorOutput "Para diagnóstico completo, ejecute: python diagnostico.py" "Yellow"
    }
} catch {
    Write-Host ""
    Write-ColorOutput "✗ Error al iniciar la aplicación: $_" "Red"
    Write-ColorOutput "Para diagnóstico completo, ejecute: python diagnostico.py" "Yellow"
}