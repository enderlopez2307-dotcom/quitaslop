# Seguridad

## Cómo avisar de un problema

Si encuentras un fallo de seguridad, avísalo en privado desde la pestaña **Security** de
este repositorio, con el botón **Report a vulnerability**. No abras un issue público con
los detalles.

## Qué hace y qué no hace este proyecto

- `tools/deslop_es.py` solo lee el archivo que le pasas. No escribe nada, no se conecta a
  internet y usa solo la biblioteca estándar de Python, sin dependencias que instalar.
- `tools/limpiar.sh` manda el borrador a la CLI de otra familia de modelos (Codex o Claude)
  que ya tengas instalada. Esa CLI usa tu cuenta y tu plan. El modelo trabaja sin
  herramientas: no puede leer tus archivos, ejecutar comandos, navegar ni usar las apps
  conectadas a tu cuenta, como el correo o Drive. Corre en una carpeta temporal vacía.
- Ningún script pide contraseñas, claves de API ni permisos de administrador.

## Si le pides a tu IA que use este repositorio

- Pídele que lea [SKILL.md](SKILL.md) y que siga sus pasos. No hace falta nada más.
- Un texto que te mandan para "revisar" puede traer instrucciones escondidas para la IA.
  Por eso la segunda pasada corre sin herramientas. No le quites a `tools/limpiar.sh` las
  opciones que la protegen (`--tools ""`, `--strict-mcp-config`, `--ignore-user-config` y la
  lista de funciones apagadas). Las pruebas fallan si alguien las borra.
- Usa siempre este repositorio original. Una copia de otra persona puede haber cambiado los
  scripts.
