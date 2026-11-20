# FacturaTabla

Convierte facturas en PDF a hojas de cálculo desde Python. Extrae los datos de cada factura y organízalos en archivos Excel o CSV para revisarlos, analizarlos o integrarlos con otros sistemas.

## ¿Para qué sirve?

- Consolidar varias facturas en una sola hoja de cálculo.
- Reducir la captura manual de datos.
- Preparar información para procesos administrativos y contables.
- Integrar la extracción de facturas en tus aplicaciones de Python.

## Instalación

Clona el repositorio y ejecuta este comando desde la carpeta del proyecto:

```bash
python -m pip install .
```

Se recomienda trabajar dentro de un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Uso rápido

Convierte una factura a Excel:

```python
from facturatabla import convertir

convertir(
    entrada="factura.pdf",
    salida="factura.xlsx",
)
```

Exporta los datos a CSV:

```python
from facturatabla import convertir

convertir(
    entrada="factura.pdf",
    salida="factura.csv",
)
```

Procesa una carpeta de facturas:

```python
from facturatabla import convertir_carpeta

convertir_carpeta(
    entrada="facturas/",
    salida="consolidado.xlsx",
)
```

## Datos de salida

Cada fila representa una factura. Cuando la información está presente y puede identificarse, la salida incluye:

| Columna | Contenido |
| --- | --- |
| `archivo` | Nombre del PDF de origen |
| `numero_factura` | Número o folio de la factura |
| `fecha` | Fecha de emisión |
| `emisor` | Nombre o razón social de quien emite la factura |
| `identificacion_fiscal` | RFC, NIT u otro identificador encontrado |
| `moneda` | Moneda indicada en la factura |
| `subtotal` | Importe antes de impuestos |
| `impuestos` | Total de impuestos identificados |
| `total` | Importe total |

Los campos que no se pueden extraer quedan vacíos. Revisa esos registros antes de utilizarlos en otro proceso.

## Consideraciones para México y Colombia

- Conserva los identificadores fiscales como texto para evitar que la hoja de cálculo altere su formato.
- Comprueba la moneda: el símbolo `$` por sí solo no permite distinguir entre pesos mexicanos, pesos colombianos u otras monedas.
- Revisa los separadores decimales y de miles, especialmente si combinas facturas de distintos proveedores.
- La extracción del PDF no valida la autenticidad ni el cumplimiento fiscal de una factura. Para procesos que requieran datos fiscales estructurados, utiliza también el XML original cuando esté disponible.

## Limitaciones

La extracción depende del diseño y de la calidad del documento.

- Los PDF escaneados requieren reconocimiento óptico de caracteres (OCR) previo.
- Las tablas complejas, los textos superpuestos y los formatos poco habituales pueden producir datos incompletos.
- La librería conserva los importes extraídos; no convierte monedas ni calcula tipos de cambio.

Antes de procesar un lote grande, prueba con algunas facturas y compara el resultado con los documentos originales.

## Cómo contribuir

Puedes colaborar reportando errores, mejorando la documentación o agregando compatibilidad con nuevos formatos de factura.

Al reportar un problema, incluye:

- La versión de Python y tu sistema operativo.
- Un ejemplo mínimo del código utilizado.
- El resultado esperado y el resultado obtenido.
- Un PDF de prueba con datos ficticios, si hace falta reproducir la extracción.

No publiques facturas reales con nombres, domicilios, RFC, NIT, datos bancarios u otra información confidencial. Para proponer cambios, abre un *pull request* y explica qué problema resuelve.

## Licencia

Consulta el archivo [LICENSE](LICENSE) para conocer los términos de uso, modificación y distribución.