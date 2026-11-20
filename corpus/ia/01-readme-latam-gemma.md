# InvoiceParser-PY 📄➡️📊

Una librería de Python robusta y fácil de usar para extraer datos de facturas en formato PDF y convertirlos automáticamente a hojas de cálculo (Excel, CSV, Google Sheets).

Diseñada específicamente para desarrolladores en México y Colombia que buscan automatizar procesos contables, gestionar gastos de freelancers o digitalizar archivos de facturación de manera eficiente.

## ✨ Características

*   **Extracción Precisa:** Identifica automáticamente campos clave como Fecha, Folio/Número de Factura, Conceptos, Impuestos (IVA, Retenciones) y Totales.
*   **Multi-formato:** Exporta directamente a `.xlsx`, `.csv` y `.json`.
*   **Soporte Regional:** Optimizado para reconocer estructuras comunes de facturas en México (CFDI) y Colombia (Factura Electrónica).
*   **Limpio y Rápido:** Procesamiento asíncrono para manejar grandes volúmenes de archivos en segundos.
*   **Fácil de Integrar:** Compatible con scripts de automatización, bots de Telegram o aplicaciones web (Flask, Django, FastAPI).

## 🚀 Instalación

Puedes instalar la librería mediante `pip`:

```bash
pip install invoice-parser-py
```

## 💻 Uso rápido

Aquí tienes un ejemplo básico de cómo convertir un archivo PDF a un archivo Excel:

```python
from invoice_parser import InvoiceConverter

# Inicializar el convertidor
converter = InvoiceConverter()

# Convertir una factura individual
converter.to_excel("factura_001.pdf", "resultado_001.xlsx")

# Procesar una carpeta entera de facturas
converter.batch_convert("./facturas_mes", "./resultados_mes")

print("¡Conversión completada con éxito!")
```

## 🛠 Configuración para México y Colombia

La librería incluye perfiles preconfigurados para mejorar la precisión según el país:

```python
# Ejemplo para México (CFDI)
converter = InvoiceConverter(region="MX")

# Ejemplo para Colombia (DIAN)
converter = InvoiceConverter(region="CO")
```

## 📦 Contenido del paquete

*   `core/`: Lógica principal de extracción de texto y parsing.
*   `parsers/`: Módulos específicos para diferentes layouts de proveedores.
*   `utils/`: Herramientas de limpieza de datos y manejo de archivos.

## 🤝 Contribuciones

¡Como proyecto de código abierto, tu ayuda es bienvenida! Si encuentras algún error o quieres añadir soporte para un nuevo formato de factura, sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una rama para tu mejora (`git checkout -b feature/NuevaMejora`).
3. Haz commit de tus cambios (`git commit -m 'Añadida mejora'`).
4. Haz un push a la rama (`git push origin feature/NuevaMejora`).
5. Abre un Pull Request.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
*Desarrollado con ❤️ para la comunidad de desarrolladores en Latinoamérica.*
