# MobileBackup-CLI

Una herramienta de línea de comandos diseñada para automatizar el respaldo de fotos y vídeos desde tu dispositivo móvil a un disco duro externo de forma rápida, segura y eficiente.

## 🚀 Características
- **Copias incrementales:** Detecta automáticamente los archivos nuevos o modificados para ahorrar tiempo y ancho de banda.
- **Soporteマルチformato:** Compatible con `.jpg`, `.png`, `.heic` y `.mov`.
- **Cross-platform:** Funciona nativamente en Linux, macOS y Windows.
- **Configuración sencilla:** Define rutas de origen y destino mediante un archivo `.env` o flags de comando.
- **Logs detallados:** Seguimiento en tiempo real del progreso de la transferencia.

## 🛠 Instalación

### Requisitos previos
- Python 3.8 o superior.
- Acceso a la carpeta del móvil (vía USB, SSHFS o montaje de red).

### Instalación rápida
Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/tu-usuario/mobilebackup-cli.git
cd mobilebackup-cli
pip install -r requirements.txt
```

Para un uso global, instala el ejecutable:
```bash
pip install .
```

## 📖 Uso

### Configuración básica
Antes de empezar, asegúrate de que tu dispositivo móvil esté montado en el sistema de archivos.

### Ejecución manual
Para realizar una copia de seguridad inmediata:

```bash
mobilebackup --source /ruta/al/movil --dest /ruta/al/disco_externo
```

### Modo automático (Recomendado)
Puedes configurar un *cron job* o una tarea programada para ejecutar el backup automáticamente cada noche. El comando básico es:

```bash
mobilebackup --sync --source /ruta/al/movil --dest /ruta/al/disco_externo
```

### Opciones disponibles
- `-s, --source`: Ruta del directorio de origen en el móvil.
- `-d, --dest`: Ruta del directorio de destino en el disco externo.
- `-y, --yes`: Omite la confirmación antes de iniciar.
- `-v, --verbose`: Muestra el progreso detallado de cada archivo.
- `--dry-run`: Simula la copia de seguridad sin mover ningún archivo (útil para depurar rutas).

## ⚙️ Configuración avanzada
Puedes crear un archivo `.config.json` en tu directorio local para evitar escribir las rutas cada vez:

```json
{
  "source": "/media/user/mobile_storage/DCIM",
  "destination": "/media/user/external_disk/Backups/Photos",
  "auto_sync": true,
  "log_level": "info"
}
```

## 🤝 Contribución
Las contribuciones son bienvenidas. Si encuentras algún bug o tienes una idea para mejorar la herramienta, abre un *issue* o envía un *pull request*.

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
