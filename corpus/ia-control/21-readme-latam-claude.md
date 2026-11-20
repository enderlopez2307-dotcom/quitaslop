# TurnosEscuela

Aplicación web de código abierto para que las escuelas y liceos de Chile organicen los turnos, reemplazos y horarios de sus profesores, sin planillas ni grupos de WhatsApp.

![Licencia](https://img.shields.io/badge/licencia-AGPL--3.0-blue)
![Estado](https://img.shields.io/badge/estado-beta-orange)

## ¿Qué problema resuelve?

En muchos colegios, los turnos de patio, los reemplazos por licencia y la distribución de horas se arman a mano en Excel. Eso genera cruces de horario, profesores sobrecargados y mucho tiempo perdido de jefatura de UTP e inspectoría.

TurnosEscuela centraliza todo en un solo lugar, es gratuita y cada establecimiento puede alojarla en sus propios servidores.

## Características

- **Calendario de turnos** semanal y mensual: patio, entrada, salida, casino, biblioteca y actividades especiales.
- **Reemplazos en minutos:** al registrar una licencia o permiso, la app sugiere docentes disponibles según su horario.
- **Detección de conflictos:** avisa si un docente queda en dos lugares a la vez o supera sus horas contratadas.
- **Horas lectivas y no lectivas:** lleva el control de ambos tipos de horas por docente.
- **Horas cronológicas y pedagógicas:** configurables según la duración de los bloques de cada colegio.
- **Reparto equitativo:** distribuye los turnos para que nadie cargue siempre con los peores horarios.
- **Notificaciones** por correo y avisos dentro de la app.
- **Exportación** a PDF, Excel y calendario (`.ics`).
- **Roles:** administrador, UTP, inspectoría y docente.
- **Funciona en el celular**, para consultar el turno desde la sala de profesores o el patio.

## Capturas de pantalla

> Agrega aquí capturas en `docs/img/` cuando las tengas.

## Instalación

### Requisitos

- Node.js 20 o superior
- PostgreSQL 15 o superior
- Git

### Pasos

```bash
git clone https://github.com/TU-ORGANIZACION/turnos-escuela.git
cd turnos-escuela
cp .env.example .env
npm install
npm run db:migrate
npm run dev
```

Luego abre `http://localhost:3000`.

### Con Docker

```bash
docker compose up -d
```

## Configuración

Edita el archivo `.env`:

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Conexión a PostgreSQL |
| `SESSION_SECRET` | Clave larga y aleatoria para las sesiones |
| `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` | Servidor de correo para notificaciones |
| `ESCUELA_NOMBRE` | Nombre del establecimiento |
| `ESCUELA_RBD` | RBD del establecimiento (opcional) |
| `ZONA_HORARIA` | Por defecto `America/Santiago` |

## Primeros pasos

1. Crea la cuenta de administrador al iniciar por primera vez.
2. Define los bloques horarios y la duración de la hora pedagógica.
3. Carga a los docentes (manualmente o con una planilla CSV).
4. Crea los tipos de turno y sus reglas.
5. Genera el calendario y revisa los conflictos que marque la app.

Para importar docentes, usa la plantilla en `docs/plantilla-docentes.csv`.

## Privacidad y datos personales

La app guarda datos de trabajadores, por lo que conviene cumplir la normativa chilena de protección de datos personales. Recomendamos:

- Alojar la instalación en un servidor bajo control del establecimiento o su sostenedor.
- No registrar datos de salud. Para licencias basta indicar "ausente", sin diagnóstico.
- Hacer respaldos periódicos de la base de datos.

Revisa con el sostenedor o su asesor legal que el uso cumpla la normativa vigente y los contratos de cada docente.

## Aviso importante

TurnosEscuela es una herramienta de apoyo a la organización. No reemplaza la revisión de contratos, el Estatuto Docente ni el Código del Trabajo. Las reglas de horas y turnos son configurables, y cada colegio debe verificar que su configuración sea correcta.

## Hoja de ruta

- [x] Calendario de turnos y detección de conflictos
- [x] Gestión de reemplazos
- [ ] Aplicación móvil instalable (PWA)
- [ ] Integración con sistemas de gestión escolar
- [ ] Intercambio de turnos entre docentes con aprobación
- [ ] Reportes de carga horaria por docente y por año

## Cómo contribuir

¡Toda ayuda es bienvenida, sobre todo de gente que trabaja en colegios!

1. Haz un fork del repositorio.
2. Crea una rama: `git checkout -b mi-mejora`.
3. Haz tus cambios y agrega pruebas si corresponde.
4. Ejecuta `npm test` y `npm run lint`.
5. Abre un Pull Request explicando qué cambia y por qué.

También puedes ayudar sin programar:

- Reportando errores o proponiendo ideas en [Issues](https://github.com/TU-ORGANIZACION/turnos-escuela/issues).
- Contándonos cómo organiza los turnos tu colegio.
- Traduciendo o mejorando la documentación.

Lee `CONTRIBUTING.md` y el `CODIGO_DE_CONDUCTA.md` antes de participar.

## Licencia

Distribuido bajo la licencia **AGPL-3.0**. Puedes usarla, modificarla y compartirla libremente. Si la ofreces como servicio a terceros, debes publicar tus cambios. Consulta el archivo `LICENSE`.

## Contacto

¿Dudas o quieres implementarla en tu colegio? Escribe a `contacto@turnosescuela.cl` o abre una discusión en la pestaña **Discussions** del repositorio.

Hecho en Chile, para los colegios de Chile.
