# fotodisco

Copia de seguridad incremental de las fotos y vídeos de tu móvil en un disco externo, desde la terminal.

`fotodisco` copia solo lo que no tienes ya en el disco, verifica cada archivo con un hash y organiza el resultado por año y mes. Funciona con Android (por ADB) y con iPhone (por libimobiledevice), en macOS y Linux.

## Características

- **Incremental.** La segunda copia solo transfiere lo nuevo. No vuelve a copiar lo que ya está.
- **Verificada.** Cada archivo se comprueba con SHA-256 después de copiarlo.
- **Sin duplicados.** Si renombras o mueves una foto en el disco, no se vuelve a copiar, porque se compara por contenido y no por nombre.
- **Orden automático.** Estructura `AAAA/MM/` según la fecha de captura (EXIF) y, si no existe, la fecha de modificación.
- **Nunca borra.** No elimina nada del móvil ni del disco, salvo que se lo pidas con `--liberar-espacio`.
- **Modo simulación.** `--simular` te dice qué haría sin tocar nada.

## Requisitos

- Python 3.10 o superior
- Android: [`adb`](https://developer.android.com/tools/adb) y la depuración USB activada
- iPhone: `libimobiledevice` e `ifuse`
- Un disco externo con espacio suficiente, formateado en **exFAT**, **APFS** o **ext4**

> **Ojo con FAT32.** No admite archivos de más de 4 GB, así que los vídeos largos fallarán. `fotodisco` lo detecta y se niega a empezar.

### Instalar las dependencias

macOS (Homebrew):

```bash
brew install android-platform-tools libimobiledevice ifuse
```

Debian y Ubuntu:

```bash
sudo apt install adb libimobiledevice-utils ifuse
```

## Instalación

```bash
pipx install fotodisco
```

Comprueba que funciona:

```bash
fotodisco --version
```

## Uso rápido

1. Conecta el móvil por USB y desbloquéalo. En Android, acepta el aviso de depuración USB. En iPhone, pulsa «Confiar».
2. Conecta el disco externo.
3. Lanza la copia:

```bash
fotodisco copiar --destino /Volumes/MiDisco/Fotos
```

La primera vez puede tardar bastante, según cuántas fotos tengas. Las siguientes serán mucho más rápidas.

### Probar sin riesgo

```bash
fotodisco copiar --destino /Volumes/MiDisco/Fotos --simular
```

## Comandos

| Comando | Qué hace |
|---|---|
| `fotodisco copiar` | Copia lo nuevo del móvil al disco |
| `fotodisco verificar` | Recalcula los hashes del disco y avisa de archivos dañados |
| `fotodisco dispositivos` | Lista los móviles detectados |
| `fotodisco estado` | Muestra cuántos archivos hay pendientes de copiar |

## Opciones de `copiar`

| Opción | Descripción |
|---|---|
| `--destino RUTA` | Carpeta de destino en el disco (obligatoria) |
| `--dispositivo ID` | Móvil concreto, si hay varios conectados |
| `--simular` | Muestra lo que haría sin copiar nada |
| `--solo-fotos` | Ignora los vídeos |
| `--desde AAAA-MM-DD` | Copia solo archivos posteriores a esa fecha |
| `--estructura PLANTILLA` | Plantilla de carpetas. Por defecto `{año}/{mes}` |
| `--liberar-espacio` | Borra del móvil lo ya copiado **y verificado** (pide confirmación) |
| `--hilos N` | Transferencias en paralelo. Por defecto 2 |

## Ejemplos

Copiar solo lo de este año:

```bash
fotodisco copiar --destino /Volumes/MiDisco/Fotos --desde 2026-01-01
```

Organizar por año y nombre de mes:

```bash
fotodisco copiar --destino /Volumes/MiDisco/Fotos --estructura "{año}/{mes_nombre}"
```

Comprobar que el disco no tiene archivos corruptos:

```bash
fotodisco verificar --destino /Volumes/MiDisco/Fotos
```

## Cómo funciona

1. Lista los archivos multimedia del móvil (`DCIM`, `Pictures`, `Movies`).
2. Compara con el índice local que guarda en `.fotodisco/indice.db`, dentro del propio disco.
3. Copia los archivos que no están, primero a un nombre temporal.
4. Calcula el SHA-256 del archivo copiado y lo compara con el original.
5. Solo si coincide, lo renombra al nombre definitivo.

Si desconectas el cable a mitad, no pasa nada grave: los archivos a medias se quedan como temporales y se descartan en la siguiente ejecución.

## Configuración

Puedes guardar tus opciones habituales en `~/.config/fotodisco/config.toml`:

```toml
destino = "/Volumes/MiDisco/Fotos"
estructura = "{año}/{mes}"
hilos = 2
solo_fotos = false
```

Con esto basta con ejecutar `fotodisco copiar`.

## Problemas frecuentes

**No detecta mi Android.** Revisa que la depuración USB esté activada y que el cable transmita datos, porque algunos solo cargan. Prueba con `adb devices`. Si aparece como `unauthorized`, desbloquea el móvil y acepta el aviso.

**No detecta mi iPhone.** Desbloquéalo, pulsa «Confiar» y ejecuta `idevicepair pair`. En macOS reciente, puede que tengas que dar permiso a la terminal en *Ajustes del Sistema > Privacidad y seguridad*.

**Va lento.** Prueba otro puerto USB y un cable de calidad. Subir `--hilos` no siempre ayuda: en discos mecánicos, 2 suele ser lo mejor.

**Aparecen fotos en `sin-fecha/`.** Son archivos sin EXIF ni fecha de modificación fiable, algo habitual en imágenes recibidas por mensajería.

## Limitaciones

- No copia las fotos que solo están en la nube (iCloud o Google Fotos) y no se han descargado al móvil.
- Las Live Photos de iPhone se copian como dos archivos (imagen y vídeo) con el mismo nombre base.
- No cifra la copia. Si necesitas cifrado, usa un disco cifrado a nivel de sistema (FileVault, LUKS).

## Seguridad y privacidad

Todo ocurre en local. `fotodisco` no envía datos a ningún servidor ni recoge telemetría.

## Contribuir

Los *issues* y las *pull requests* son bienvenidos. Antes de abrir una PR:

```bash
git clone https://github.com/tu-usuario/fotodisco
cd fotodisco
pip install -e ".[dev]"
pytest
```

## Licencia

MIT. Consulta el archivo [LICENSE](LICENSE).
