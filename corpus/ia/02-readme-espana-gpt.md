# FotoBackup

Copia las fotos y los vídeos de tu móvil a un disco externo desde la terminal. Comprueba la integridad de cada archivo y evita volver a copiar los que ya están guardados.

Los originales permanecen en el móvil. FotoBackup no los borra ni modifica.

## Requisitos

- Un móvil conectado por USB y desbloqueado.
- Las fotos del móvil accesibles como una carpeta local.
- Un disco externo montado, con permisos de escritura y espacio suficiente.

Si tu sistema muestra el móvil mediante MTP, tendrás que montarlo con una herramienta compatible antes de ejecutar FotoBackup. En iPhone, puede ser necesario importar primero los originales al ordenador.

Las fotos que estén únicamente en iCloud o Google Fotos deben descargarse antes.

## Instalación

Descarga el ejecutable correspondiente a tu sistema desde la sección **Releases** del proyecto y añade su carpeta al `PATH`.

Comprueba que funciona:

```bash
fotobackup --version
```

Para consultar las opciones disponibles:

```bash
fotobackup --help
```

## Primera copia

Los ejemplos utilizan rutas de Linux. Sustitúyelas por las de tu móvil y tu disco externo.

Primero, comprueba qué se copiaría sin escribir ningún archivo:

```bash
fotobackup backup \
  --origen "/media/ana/Movil/DCIM" \
  --destino "/media/ana/Disco externo/Fotos del móvil" \
  --simular
```

Revisa el número de archivos y el espacio necesario. Después, ejecuta la copia:

```bash
fotobackup backup \
  --origen "/media/ana/Movil/DCIM" \
  --destino "/media/ana/Disco externo/Fotos del móvil"
```

Mantén el móvil conectado y desbloqueado hasta que termine.

> Antes de empezar, confirma que el disco externo está montado. Una carpeta con el nombre esperado puede existir aunque el disco esté desconectado.

## Cómo se guardan los archivos

FotoBackup conserva la estructura de carpetas del origen:

```text
Fotos del móvil/
├── Camera/
│   ├── IMG_20261118_103000.jpg
│   └── VID_20261118_104500.mp4
└── Screenshots/
    └── Screenshot_20261118.png
```

Copia los archivos originales sin convertirlos ni comprimirlos. Los metadatos incluidos en cada archivo, como la fecha de captura o la ubicación, se conservan.

Si quieres incluir otras carpetas, como las imágenes recibidas por mensajería, ejecuta una copia adicional indicando su ruta.

## Copias posteriores

Vuelve a ejecutar el mismo comando. FotoBackup compara el contenido y omite los archivos que ya están copiados y verificados.

Si encuentra un archivo distinto con el mismo nombre, guarda ambas versiones añadiendo un sufijo. No sobrescribe la copia existente.

Las fotos que borres del móvil seguirán en el disco externo: la herramienta hace copias de seguridad, no sincroniza los borrados.

## Verificar una copia

Para comprobar los archivos guardados frente al registro de la copia:

```bash
fotobackup verify \
  --destino "/media/ana/Disco externo/Fotos del móvil"
```

La verificación utiliza sumas de comprobación para detectar archivos alterados o incompletos. No necesita que el móvil esté conectado.

## Si la copia se interrumpe

Puedes detener el proceso con `Ctrl+C`. Para continuar, vuelve a ejecutar el mismo comando.

Los archivos completos y verificados se omiten. Los que hayan quedado a medias se vuelven a copiar.

## Problemas habituales

| Problema | Qué revisar |
|---|---|
| No se encuentra el origen | Desbloquea el móvil, activa la transferencia de archivos y comprueba la ruta. |
| Permiso denegado | Revisa los permisos de lectura del origen y de escritura del destino. |
| Espacio insuficiente | Libera espacio o utiliza otro disco. |
| Falla un vídeo grande | Comprueba el formato del disco: FAT32 no admite archivos de más de 4 GiB. |
| Error de verificación | Repite la copia y revisa el cable, la conexión y el estado del disco. |

## Antes de desconectar

Comprueba que el proceso ha terminado sin errores y expulsa el disco desde el sistema operativo.

Para fotos irremplazables, conserva otra copia en un dispositivo o ubicación diferente.