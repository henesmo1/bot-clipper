# Script PowerShell para instalar TensorFlow en un entorno virtual compatible

# Función para mostrar texto con colores
function Write-ColorOutput {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Text,
        
        [Parameter(Mandatory=$false)]
        [string]$ForegroundColor = 'White'
    )
    
    Write-Host $Text -ForegroundColor $ForegroundColor
}

# Encabezado
Write-ColorOutput '=== Instalador de TensorFlow para DCS-Clipper ===' 'Cyan'
Write-Host ''

# Verificar la versión de Python actual
try {
    $pythonVersion = & python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"
    $pythonVersionMajor = [int]($pythonVersion.Split('.')[0])
    $pythonVersionMinor = [int]($pythonVersion.Split('.')[1])
    
    Write-ColorOutput "Version de Python detectada: $pythonVersion" 'Cyan'
    
    # Verificar si la versión es compatible con TensorFlow
    if ($pythonVersionMajor -eq 3 -and $pythonVersionMinor -ge 9 -and $pythonVersionMinor -le 13) {
        Write-ColorOutput "La version de Python $pythonVersion es compatible con TensorFlow." 'Green'
        
        # Preguntar si desea instalar directamente o en un entorno virtual
        Write-ColorOutput "Desea instalar TensorFlow directamente o en un entorno virtual?" 'Yellow'
        Write-Host "1. Instalar directamente"
        Write-Host "2. Crear un entorno virtual"
        $opcion = Read-Host "Seleccione una opcion (1 o 2)"
        
        if ($opcion -eq "1") {
            # Instalar TensorFlow directamente
            Write-ColorOutput "Instalando TensorFlow..." 'Cyan'
            & python -m pip install tensorflow
            
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "TensorFlow se ha instalado correctamente." 'Green'
            } else {
                Write-ColorOutput "Hubo errores durante la instalacion de TensorFlow." 'Red'
                Write-ColorOutput "Intentando instalar TensorFlow CPU..." 'Yellow'
                
                & python -m pip install tensorflow-cpu
                
                if ($LASTEXITCODE -eq 0) {
                    Write-ColorOutput "TensorFlow CPU se ha instalado correctamente." 'Green'
                } else {
                    Write-ColorOutput "No se pudo instalar TensorFlow." 'Red'
                }
            }
        } elseif ($opcion -eq "2") {
            # Crear un entorno virtual
            Write-ColorOutput "Creando entorno virtual para TensorFlow..." 'Cyan'
            
            # Verificar si el directorio ya existe
            if (Test-Path "$PSScriptRoot\venv-tensorflow") {
                Write-ColorOutput "El directorio del entorno virtual ya existe." 'Yellow'
                $eliminar = Read-Host "Desea eliminarlo y crear uno nuevo? (s/n)"
                
                if ($eliminar -eq "s") {
                    Remove-Item -Recurse -Force "$PSScriptRoot\venv-tensorflow"
                } else {
                    Write-ColorOutput "Usando el entorno virtual existente." 'Yellow'
                    Write-ColorOutput "Para activar el entorno virtual, ejecute:" 'Cyan'
                    Write-Host "  .\venv-tensorflow\Scripts\activate"
                    exit 0
                }
            }
            
            # Crear el entorno virtual
            & python -m venv "$PSScriptRoot\venv-tensorflow" --prompt tensorflow-env
            
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "Entorno virtual creado correctamente." 'Green'
                Write-ColorOutput "Activando entorno virtual..." 'Cyan'
                
                # Activar el entorno virtual e instalar TensorFlow
                Write-ColorOutput "Para completar la instalacion, ejecute los siguientes comandos:" 'Cyan'
                Write-Host "  .\venv-tensorflow\Scripts\activate"
                Write-Host "  python -m pip install --upgrade pip"
                Write-Host "  python -m pip install tensorflow"
                
                Write-ColorOutput "\nUna vez instalado, puede verificar la instalacion con:" 'Cyan'
                Write-Host "  python -c \"import tensorflow as tf; print(tf.__version__)\""
            } else {
                Write-ColorOutput "Error al crear el entorno virtual." 'Red'
            }
        } else {
            Write-ColorOutput "Opcion no valida. Saliendo..." 'Red'
            exit 1
        }
    } else {
        Write-ColorOutput "La version de Python $pythonVersion no es compatible con TensorFlow." 'Yellow'
        Write-ColorOutput "TensorFlow requiere Python 3.9-3.13." 'Yellow'
        
        # Preguntar si desea instalar una versión compatible de Python
        Write-ColorOutput "Desea crear un entorno virtual con una version compatible de Python?" 'Yellow'
        Write-Host "1. Si, crear entorno virtual (requiere tener instalada una version compatible)"
        Write-Host "2. No, solo mostrar instrucciones"
        $opcion = Read-Host "Seleccione una opcion (1 o 2)"
        
        if ($opcion -eq "1") {
            # Crear entorno virtual
            Write-ColorOutput "Creando entorno virtual para TensorFlow..." 'Cyan'
            
            # Verificar si el directorio ya existe
            if (Test-Path "$PSScriptRoot\venv-tensorflow") {
                Write-ColorOutput "El directorio del entorno virtual ya existe." 'Yellow'
                $eliminar = Read-Host "Desea eliminarlo y crear uno nuevo? (s/n)"
                
                if ($eliminar -eq "s") {
                    Remove-Item -Recurse -Force "$PSScriptRoot\venv-tensorflow"
                } else {
                    Write-ColorOutput "Usando el entorno virtual existente." 'Yellow'
                    Write-ColorOutput "Para activar el entorno virtual, ejecute:" 'Cyan'
                    Write-Host "  .\venv-tensorflow\Scripts\activate"
                    exit 0
                }
            }
            
            # Intentar crear el entorno virtual
            try {
                & python -m venv "$PSScriptRoot\venv-tensorflow" --prompt tensorflow-env
                
                if ($LASTEXITCODE -eq 0) {
                    Write-ColorOutput "Entorno virtual creado correctamente." 'Green'
                    Write-ColorOutput "Para completar la instalacion, ejecute los siguientes comandos:" 'Cyan'
                    Write-Host "  .\venv-tensorflow\Scripts\activate"
                    Write-Host "  python -m pip install --upgrade pip"
                    Write-Host "  python -m pip install tensorflow"
                } else {
                    Write-ColorOutput "Error al crear el entorno virtual." 'Red'
                    Write-ColorOutput "Es posible que necesite instalar una version compatible de Python (3.9-3.13)." 'Yellow'
                }
            } catch {
                Write-ColorOutput "Error al crear el entorno virtual: $_" 'Red'
            }
        } else {
            # Mostrar instrucciones
            Write-ColorOutput "Para instalar TensorFlow, siga estos pasos:" 'Cyan'
            Write-Host "1. Instale una version compatible de Python (3.9-3.13) desde https://www.python.org/downloads/"
            Write-Host "2. Cree un entorno virtual con esa version de Python"
            Write-Host "3. Active el entorno virtual e instale TensorFlow"
            Write-Host ""
            Write-ColorOutput "Ejemplo de comandos (ajuste segun su instalacion):" 'Cyan'
            Write-Host "  python -m venv venv-tensorflow --prompt tensorflow-env"
            Write-Host "  .\venv-tensorflow\Scripts\activate"
            Write-Host "  python -m pip install --upgrade pip"
            Write-Host "  python -m pip install tensorflow"
        }
    }
} catch {
    Write-ColorOutput "Error al verificar la version de Python: $_" 'Red'
}