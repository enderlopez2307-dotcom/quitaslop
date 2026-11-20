# factupy

Convierte facturas en PDF a hojas de cálculo (Excel o CSV) con unas pocas líneas de Python.

[![PyPI](https://img.shields.io/pypi/v/factupy.svg)](https://pypi.org/project/factupy/)
[![Python](https://img.shields.io/pypi/pyversions/factupy.svg)](https://pypi.org/project/factupy/)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

`factupy` lee facturas en PDF, extrae los campos importantes (emisor, receptor, fecha, folio, impuestos, totales y partidas) y los deja listos en un `.xlsx`, un `.csv` o un `DataFrame` de pandas. Está pensada para los formatos de facturación de **México** (CFDI) y **Colombia** (factura electrónica DIAN).

## ¿Para qué sirve?

- Contabilidad y conciliación: pasa cientos de facturas a una sola hoja en minutos.
- Procesos internos: alimenta tu ERP, tu base de datos o un dashboard sin capturar a mano.
- Auditorías: genera un reporte con una fila por factura o una fila por partida.

## Características

- **Soporte para México:** detecta RFC, UUID (folio fiscal), uso de CFDI, régimen fiscal, IVA, ISR e IEPS.
- **Soporte para Colombia:** detecta NIT, CUFE, prefijo y número, IVA, retefuente y reteICA.
- **Lectura de PDF con texto** y, opcionalmente, **PDF escaneados** mediante OCR.
- **Salida flexible:** Excel, CSV, JSON o `DataFrame`.
- **Procesamiento por lotes:** una carpeta completa en una sola llamada.
- **Validaciones básicas:** avisa si los subtotales, impuestos y total no cuadran.
- **Extensible:** agrega tus propios formatos de proveedor con plantillas.

## Instalación

Requiere Python 3.9 o superior.

```bash
pip install factupy
```

Para soporte de PDF escaneados (OCR):

```bash
pip install "factupy[ocr]"
```

El OCR necesita [Tesseract](https://github.com/tesseract-ocr/tesseract) instalado en tu sistema:

```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu / Debian
sudo apt install tesseract-ocr tesseract-ocr-spa
```

## Uso rápido

### Una factura

```python
from factupy import leer_factura

factura = leer_factura("factura.pdf", pais="mx")  # "mx" o "co"

print(factura.emisor.nombre)
print(factura.total)
print(factura.partidas)
```

### Una carpeta completa a Excel

```python
from factupy import procesar_carpeta

procesar_carpeta(
    "facturas/",
    pais="co",
    salida="facturas_octubre.xlsx",
)
```

Esto genera un archivo con dos hojas:

| Hoja | Contenido |
|------|-----------|
| `Facturas` | Una fila por factura (emisor, receptor, fecha, subtotal, impuestos, total) |
| `Partidas` | Una fila por concepto o línea de cada factura |

### Con pandas

```python
from factupy import procesar_carpeta

df = procesar_carpeta("facturas/", pais="mx", como="dataframe")
print(df.groupby("emisor_rfc")["total"].sum())
```

## Línea de comandos

```bash
# Una carpeta a Excel
factupy facturas/ --pais mx --salida reporte.xlsx

# Un solo PDF a CSV
factupy factura.pdf --pais co --formato csv

# Con OCR para PDF escaneados
factupy escaneadas/ --pais mx --ocr --salida reporte.xlsx
```

Opciones principales:

| Opción | Descripción |
|--------|-------------|
| `--pais` | `mx` o `co` (obligatoria) |
| `--salida` | Ruta del archivo de salida |
| `--formato` | `xlsx` (por defecto), `csv` o `json` |
| `--ocr` | Activa el OCR para PDF escaneados |
| `--estricto` | Falla si una factura no pasa las validaciones |

## Ejemplo de resultado

| archivo | pais | folio | fecha | emisor | receptor | subtotal | iva | total |
|---------|------|-------|-------|--------|----------|----------|-----|-------|
| fac_001.pdf | mx | A-1042 | 2026-10-03 | Papelería del Centro SA de CV | Estudio Rivas SC | 1,000.00 | 160.00 | 1,160.00 |
| fac_002.pdf | co | FE-8821 | 2026-10-05 | Insumos Andinos SAS | Taller Gómez | 500,000 | 95,000 | 595,000 |

## Manejo de errores y validaciones

Por defecto, `factupy` no se detiene ante una factura problemática. La marca y sigue con las demás:

```python
resultado = procesar_carpeta("facturas/", pais="mx")

for error in resultado.errores:
    print(error.archivo, error.motivo)
```

Motivos comunes:

- `texto_no_encontrado`: el PDF es una imagen. Prueba con `--ocr`.
- `totales_no_cuadran`: subtotal más impuestos no coincide con el total.
- `formato_desconocido`: el diseño del proveedor no se reconoce. Crea una plantilla (ver abajo).

## Plantillas personalizadas

Si un proveedor usa un diseño poco común, puedes describirlo en un archivo YAML:

```yaml
# plantillas/mi_proveedor.yaml
nombre: Mi Proveedor SA de CV
pais: mx
detectar:
  contiene: "MIPROVEEDOR SA DE CV"
campos:
  folio:
    regex: "Folio:\\s*(\\w+-\\d+)"
  total:
    regex: "Total:\\s*\\$?([\\d,]+\\.\\d{2})"
```

```python
procesar_carpeta("facturas/", pais="mx", plantillas="plantillas/")
```

## Limitaciones

- La extracción desde PDF es **heurística**. Si tienes el XML original (CFDI en México o el XML de la DIAN en Colombia), úsalo: es más confiable. `factupy` también puede leerlo con `leer_xml()`.
- El OCR depende de la calidad del escaneo. Revisa siempre los resultados antes de usarlos en declaraciones o reportes oficiales.
- Esta librería **no valida facturas ante el SAT ni la DIAN**. No sustituye la verificación oficial.

## Contribuir

¡Las contribuciones son bienvenidas! Algunas formas de ayudar:

1. **Reporta un formato que no se lee bien.** Abre un issue con un PDF de ejemplo **sin datos reales** (anonimiza RFC, NIT, nombres y montos).
2. **Agrega una plantilla** para un proveedor o banco común en tu país.
3. **Mejora la documentación** o traduce ejemplos.
4. **Envía un pull request** con correcciones o nuevas funciones.

Para desarrollo local:

```bash
git clone https://github.com/tu-usuario/factupy.git
cd factupy
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Antes de enviar tu PR, corre `ruff check .` y `pytest`. Lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## Privacidad

Todo el procesamiento ocurre **en tu máquina**. `factupy` no envía tus facturas ni sus datos a ningún servicio externo.

## Hoja de ruta

- [ ] Lectura directa de XML CFDI 4.0 y UBL de la DIAN
- [ ] Complementos de pago y notas de crédito
- [ ] Soporte para otros países de la región
- [ ] Exportación a Google Sheets

## Licencia

Distribuido bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE).

---

Hecho con cariño desde y para la comunidad de desarrolladores de Latinoamérica.
