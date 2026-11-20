#!/usr/bin/env bash
# Pruebas de la separación texto/notas de limpiar.sh y de sus salidas de error.
#
# La separación es lo que mantiene las notas del modelo fuera de limpio.md. Sin
# ella el checker puntuaría las notas como prosa y diría LIMPIO midiendo lo que no es.
#
# Carga emit_copy desde limpiar.sh en lugar de copiarla, así la prueba falla si la
# función real cambia. No llama a ningún modelo, así que corre en CI.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
eval "$(sed -n "/^NOTES_SENTINEL=/,/^}$/p" "$HERE/limpiar.sh")"

fail=0
check() {  # check <nombre> <resultado>
  if [ "$2" = "0" ]; then printf '  ok     %s\n' "$1"
  else printf '  FALLA  %s\n' "$1"; fail=1; fi
}

# ── la respuesta normal ─────────────────────────────────────────────────────
out="$(printf 'Línea uno.\nLínea dos.\n\n%s\n- quité una señal\n' "$NOTES_SENTINEL" | emit_copy 2>/dev/null)"
[ "$out" = "$(printf 'Línea uno.\nLínea dos.')" ]; check 'el texto es lo que está encima del marcador' $?
err="$(printf 'Texto.\n\n%s\n- quité una señal\n' "$NOTES_SENTINEL" | emit_copy 2>&1 >/dev/null)"
case "$err" in *'quité una señal'*) check 'las notas van a stderr' 0;; *) check 'las notas van a stderr' 1;; esac
case "$out" in *'quité una señal'*) check 'las notas NO salen por stdout' 1;; *) check 'las notas NO salen por stdout' 0;; esac

# ── un borrador que tiene --- de verdad ─────────────────────────────────────
body="$(printf 'Intro.\n\n---\n\nDespués de la raya.\nÚltima línea.\n\n%s\n- una nota\n' "$NOTES_SENTINEL" | emit_copy 2>/dev/null)"
case "$body" in *'Última línea.'*) check 'el texto después de --- sobrevive' 0;; *) check 'el texto después de --- sobrevive' 1;; esac
case "$body" in *'---'*) check 'el --- se conserva' 0;; *) check 'el --- se conserva' 1;; esac
case "$body" in *'una nota'*) check 'las notas no se cuelan tras un ---' 1;; *) check 'las notas no se cuelan tras un ---' 0;; esac

# ── sin marcador: se devuelve todo y se avisa ───────────────────────────────
out="$(printf 'Solo texto.\nSegunda línea.\n' | emit_copy 2>/dev/null)"
case "$out" in *'Segunda línea.'*) check 'sin marcador no se pierde texto' 0;; *) check 'sin marcador no se pierde texto' 1;; esac
err="$(printf 'Solo texto.\n' | emit_copy 2>&1 >/dev/null)"
case "$err" in *AVISO*) check 'sin marcador avisa' 0;; *) check 'sin marcador avisa' 1;; esac

# ── marcador sin nada detrás ────────────────────────────────────────────────
err="$(printf 'Solo texto.\n\n%s\n' "$NOTES_SENTINEL" | emit_copy 2>&1 >/dev/null)"
[ -z "$err" ]; check 'notas vacías no imprimen nada en stderr' $?

# ── las líneas en blanco antes del marcador no se publican ──────────────────
# Se mide en un ARCHIVO: "$(...)" borra los saltos finales y no vería el fallo.
tmp="$(mktemp)"
printf 'Aquí acaba.\n\n\n%s\n- una nota\n' "$NOTES_SENTINEL" | emit_copy 2>/dev/null >"$tmp"
[ "$(wc -c <"$tmp" | tr -d ' ')" = "13" ]; check 'se recortan las líneas en blanco antes del marcador' $?
rm -f "$tmp"

# ── el marcador citado dentro de una frase no corta ─────────────────────────
out="$(printf 'Usamos la marca `%s` aquí.\nSigue el texto.\n' "$NOTES_SENTINEL" | emit_copy 2>/dev/null)"
case "$out" in *'Sigue el texto.'*) check 'el marcador dentro de una línea no es un corte' 0;; *) check 'el marcador dentro de una línea no es un corte' 1;; esac

# ── tildes y eñes llegan intactas ───────────────────────────────────────────
out="$(printf '¿Cómo estás? ¡Qué bien, niño!\n\n%s\n' "$NOTES_SENTINEL" | emit_copy 2>/dev/null)"
[ "$out" = '¿Cómo estás? ¡Qué bien, niño!' ]; check 'tildes, eñes, ¿ y ¡ intactos' $?

# ── salidas de error del script completo (sin llamar a ningún modelo) ───────
bash "$HERE/limpiar.sh" /no/existe.md >/dev/null 2>&1; [ $? -eq 66 ]; check 'archivo inexistente sale con 66' $?
vacio="$(mktemp)"; printf '  \n\n' >"$vacio"
bash "$HERE/limpiar.sh" "$vacio" >/dev/null 2>&1; [ $? -eq 66 ]; check 'borrador vacío sale con 66' $?
rm -f "$vacio"
# Sin CLI de la otra familia: una copia del script con las dos vacías.
sinCLI="$(mktemp -d)"; mkdir -p "$sinCLI/tools" "$sinCLI/prompts"
sed 's|^CODEX=.*|CODEX=""|; s|^CLAUDE=.*|CLAUDE=""|' "$HERE/limpiar.sh" > "$sinCLI/tools/limpiar.sh"
cp "$HERE/../prompts/limpiar.txt" "$sinCLI/prompts/"
out="$(printf 'Borrador de prueba.\n' | bash "$sinCLI/tools/limpiar.sh" - 2>/dev/null)"; rc=$?
[ $rc -eq 127 ]; check 'sin CLI de la otra familia sale con 127' $?
case "$out" in *'Borrador de prueba.'*) check 'sin CLI imprime el prompt con el borrador' 0;; *) check 'sin CLI imprime el prompt con el borrador' 1;; esac
case "$out" in *'<<<QUITASLOP-NOTAS>>>'*) check 'el prompt impreso pide el marcador' 0;; *) check 'el prompt impreso pide el marcador' 1;; esac
rm -rf "$sinCLI"

# ── el modelo que limpia trabaja sin herramientas ───────────────────────────
# Un borrador puede traer instrucciones escondidas para el modelo. Estas marcas en el
# script son lo que impide que las cumpla; si alguien las borra, esta prueba falla.
S="$HERE/limpiar.sh"
grep -q -- '--tools ""' "$S"; check 'claude corre sin herramientas' $?
grep -q -- '--strict-mcp-config' "$S"; check 'claude corre sin servidores MCP' $?
grep -q -- '--setting-sources ""' "$S"; check 'claude corre sin la configuración del usuario' $?
grep -q -- '--ignore-user-config' "$S"; check 'codex corre sin la configuración del usuario' $?
grep -q -- '--sandbox read-only' "$S"; check 'codex corre en modo solo lectura' $?
# Solo cuenta la lista que se apaga de verdad (el bloque "for f in ... do"), no los comentarios.
OFFLIST=" $(sed -n '/^for f in /,/; do$/p' "$S" | tr -d '\\;' | tr -s '[:space:]' ' ') "
for f in apps shell_tool unified_exec code_mode_host multi_agent plugins browser_use computer_use; do
  case "$OFFLIST" in *" $f "*) check "codex sin la función $f" 0;; *) check "codex sin la función $f" 1;; esac
done
grep -q 'web_search="disabled"' "$S"; check 'codex sin búsqueda web' $?
grep -q '<"$PROMPT_TMP"' "$S"; check 'el prompt va por la entrada estándar, no como argumento' $?
grep -q 'cd "$SAFE_DIR"' "$S"; check 'el modelo corre en una carpeta vacía' $?

[ "$fail" = "0" ] && echo "todas las pruebas de limpiar pasaron" || { echo "las pruebas de limpiar FALLARON"; exit 1; }
