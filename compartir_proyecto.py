import os
import zipfile

# Directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Archivos y directorios a excluir
exclusions = []

# Ruta del archivo ZIP
zip_path = os.path.join(project_dir, 'DCS-Clipper.zip')

# Crear archivo ZIP
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_dir):
        # Excluir directorios
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclusions]
        for file in files:
            file_path = os.path.join(root, file)
            # Excluir archivos
            if any(exclusion in file_path for exclusion in exclusions):
                continue
            # Agregar archivo al ZIP
            zipf.write(file_path, os.path.relpath(file_path, project_dir))

print(f'Proyecto empaquetado en {zip_path}')