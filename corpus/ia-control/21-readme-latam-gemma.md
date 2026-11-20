# TurnosEscolares 🏫

TurnosEscolares es una aplicación web de código abierto diseñada para ayudar a las instituciones educativas en Chile a organizar, gestionar y visualizar los turnos de los docentes de manera eficiente, transparente y colaborativa.

## 📝 Descripción
La gestión de turnos (recreos, supervisiones, almuerzos y otras labores no lectivas) suele ser un desafío logístico para las escuelas. Esta herramienta permite a las direcciones y coordinaciones académicas automatizar la asignación de turnos, reducir la carga administrativa y permitir que los profesores consulten sus responsabilidades en tiempo real desde cualquier dispositivo.

## ✨ Características principales
- **Gestión de Turnos:** Creación de turnos para diferentes bloques horarios y áreas de la escuela.
- **Calendario Interactivo:** Visualización clara de las asignaciones semanales y mensuales.
- **Asignación por Niveles:** Organiza a los docentes por departamentos, ciclos o niveles educativos.
- **Notificaciones:** Avisos sobre cambios de último minuto o nuevas asignaciones.
- **Exportación de Datos:** Descarga de planillas en formato PDF o Excel para impresión física.
- **Interfaz Adaptativa:** Diseño "mobile-first" para que los docentes revisen sus turnos desde el celular.

## 🛠 Tecnologías utilizadas
*(Ajustar según tu stack tecnológico real)*
- **Frontend:** React.js / Next.js / Vue.js
- **Backend:** Node.js / Python (FastAPI) / PHP (Laravel)
- **Base de Datos:** PostgreSQL / MySQL / MongoDB
- **Despliegue:** Docker, Vercel o Render

## 🚀 Instalación Local

Sigue estos pasos para ejecutar el proyecto en tu propio entorno de desarrollo:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/turnos-escolares.git
   cd turnos-escolares
   ```

2. **Instalar dependencias:**
   ```bash
   # Para el frontend
   cd client
   npm install
   
   # Para el backend
   cd ../server
   npm install
   ```

3. **Configurar variables de entorno:**
   Crea un archivo `.env` en la carpeta del servidor con las credenciales necesarias (DB_URL, SECRET_KEY, etc.).

4. **Ejecutar la aplicación:**
   ```bash
   # Iniciar backend
   cd server
   npm run dev
   
   # Iniciar frontend
   cd client
   npm run dev
   ```

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si quieres ayudar a mejorar esta herramienta para las escuelas chilenas:
1. Haz un Fork del proyecto.
2. Crea una rama para tu mejora (`git checkout -b feature/NombreDeLaMejora`).
3. Haz commit de tus cambios (`git commit -m 'Añade la mejora'`).
4. Sube los cambios (`git push origin feature/NombreDeLaMejora`).
5. Abre un Pull Request.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
*Desarrollado con ❤️ para la comunidad educativa chilena.*
