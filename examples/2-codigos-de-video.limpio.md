> Descargas un archivo con 31 códigos, se lo das a Claude en tu computadora y le pides que los instale. Después pones un video tuyo en esa carpeta, escribes, por ejemplo, `/subtitulos mi-video.mp4` y Claude te devuelve el video editado.

Cada código contiene instrucciones que probé con mis propios videos. Le indica a Claude qué hacer, con qué medidas y cómo revisar el resultado antes de dártelo.

Al terminar tendrás:

- Los 31 códigos instalados en una carpeta de tu computadora.
- Los códigos para quitar silencios de tu video, añadir subtítulos, animaciones y zooms, y ajustar el color, con un código para cada tarea.
- Si conectas Higgsfield, 8 efectos con IA: desapareces, te derrites, te clonas, eres un gigante en la ciudad o sales en la pantalla de un estadio.

## Antes de empezar

Necesitas:

- La aplicación de escritorio de Claude, con tu sesión iniciada. Se descarga en claude.com/download.
- Un plan de pago de Claude, porque los códigos trabajan en la pestaña **Code** y Code no está en el plan gratis.
- Una computadora. Yo los probé en un Mac. En Windows deberían funcionar igual, pero todavía no lo comprobé.
- Un video tuyo hablando a cámara, en vertical, como sale del celular.
- Para los 8 efectos con IA, una cuenta de Higgsfield con créditos. Los otros 23 códigos no la necesitan.

La primera vez, Claude te pedirá permiso para instalar los programas gratis que necesita para editar, como ffmpeg, que edita video, y un transcriptor, que convierte lo que dices en texto. Acepta esos permisos para que pueda usarlos.

## 1. Descarga los códigos

<a class="prompt-download" href="/guias/codigos-de-video.zip" download data-guide-zip-download>
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11"></path><path d="m7 11 5 5 5-5"></path><path d="M5 20h14"></path></svg>
<span class="prompt-download__text"><span class="prompt-download__name">Descarga los códigos (.zip)</span><span class="prompt-download__hint">Descárgalo en tu computadora. No hace falta abrirlo: en el paso 2 se lo das a Claude tal cual.</span></span>
</a>

Si abriste esta guía en el celular, ábrela en tu computadora: enderlopez.com/guias/codigos-de-video/

## 2. Instálalos en Claude

1. Abre la aplicación de Claude en tu computadora.
2. Toca la pestaña **Code**, arriba en el centro. No uses **Chat**: esa pestaña no ve los archivos de tu computadora.
3. Debajo del cuadro donde escribes, toca **Elegir…** y después **Abrir carpeta…**
4. Entra a **Escritorio**, toca **Nueva carpeta**, llámala `mis-videos` y toca **Abrir**.
5. Arrastra el archivo `codigos-de-video.zip` al cuadro donde escribes, pega este prompt y pulsa **Enter**:

```text
Instala los códigos de video que te adjunto (codigos-de-video.zip): descomprímelo dentro de esta carpeta en .claude/skills/, de forma que cada código quede en su propia carpeta. Después dime cuáles quedaron instalados y comprueba qué programas me faltan para usarlos.
```

Usa siempre esta misma carpeta `mis-videos`: los códigos quedan instalados dentro de ella.
