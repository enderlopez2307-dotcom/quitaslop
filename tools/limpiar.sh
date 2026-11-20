#!/usr/bin/env bash
# Segunda pasada: un modelo de OTRA familia limpia las señales que dejó el primero.
#
# La regla: la limpieza la hace una familia de modelos distinta de la que escribió
# el borrador. Un modelo oye mal su propio acento; otra familia lo oye enseguida.
#
#   tools/limpiar.sh borrador.md                 # limpia un archivo
#   cat borrador.md | tools/limpiar.sh -         # limpia la entrada estándar
#   TIMEOUT=240 tools/limpiar.sh borrador.md     # más tiempo para un documento largo
#
# A quién se lo manda, en este orden:
#   1. hay CLI de codex y DESLOP_WRITER no es gpt  -> pasada de GPT con `codex exec`
#   2. hay CLI de claude y DESLOP_WRITER=gpt       -> pasada de Claude con `claude -p`
#   3. ninguna de las dos                          -> imprime el prompt para pegarlo a mano
#
# Códigos de salida: 66 borrador vacío o ilegible, 124 tiempo agotado, 127 sin CLI
# de la otra familia. Vuelve a pasar SIEMPRE el checker por la salida:
#   python3 tools/deslop_es.py limpio.md
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROMPT_FILE="$HERE/../prompts/limpiar.txt"
TIMEOUT="${TIMEOUT:-180}"

if [ "${1:-}" = "-" ] || [ $# -eq 0 ]; then
  DRAFT="$(cat)"
else
  # Sin esto, un nombre de archivo mal escrito mandaba un borrador VACÍO a un
  # modelo de pago y guardaba su respuesta como si fuera el texto limpio.
  [ -f "$1" ] && [ -r "$1" ] || { echo "limpiar: no puedo leer $1" >&2; exit 66; }
  DRAFT="$(cat "$1")"
fi
[ -n "$(printf '%s' "$DRAFT" | tr -d '[:space:]')" ] || {
  echo "limpiar: el borrador está vacío, no hay nada que limpiar" >&2; exit 66; }

FULL="$(cat "$PROMPT_FILE")

$DRAFT"

# Busca el binario en el PATH, en ~/.local/bin y dentro de la app de Codex para Mac,
# que trae su propia CLI aunque no esté en el PATH.
find_bin() {
  command -v "$1" 2>/dev/null && return 0
  [ -x "$HOME/.local/bin/$1" ] && { echo "$HOME/.local/bin/$1"; return 0; }
  [ "$1" = codex ] && [ -x /Applications/Codex.app/Contents/Resources/codex-cli/bin/codex ] && {
    echo /Applications/Codex.app/Contents/Resources/codex-cli/bin/codex; return 0; }
  return 1
}

# La respuesta es el texto, una línea marcador y las notas. El texto va a STDOUT
# para que `limpiar.sh borrador.md > limpio.md` guarde SOLO el texto; las notas van
# a STDERR. Si falta el marcador, se devuelve todo como texto y se avisa: una nota
# suelta se ve y se borra, un último párrafo tragado no se recupera.
NOTES_SENTINEL='<<<QUITASLOP-NOTAS>>>'

emit_copy() {
  awk -v s="$NOTES_SENTINEL" '
    $0 == s { seen = 1; next }
    seen    { notes = notes $0 "\n"; next }
            { body = body $0 "\n" }
    END {
      if (!seen) {
        printf "%s", body
        print "limpiar: AVISO, la respuesta no trae la línea " s "." > "/dev/stderr"
        print "limpiar: devuelvo todo como texto. Revisa el final antes de publicar," > "/dev/stderr"
        print "limpiar: porque las notas podrían puntuarse como si fueran prosa." > "/dev/stderr"
        exit 0
      }
      sub(/\n+$/, "", body)
      printf "%s\n", body
      if (notes != "") {
        print ""                         > "/dev/stderr"
        print "limpiar: qué cambió:"     > "/dev/stderr"
        printf "%s", notes               > "/dev/stderr"
      }
    }
  '
}

CODEX="$(find_bin codex || true)"
CLAUDE="$(find_bin claude || true)"

run_bounded() {  # run_bounded <cmd...>  macOS no trae `timeout`, así que va a mano
  OUT="$(mktemp)"; trap 'rm -f "$OUT"' RETURN
  "$@" >"$OUT" 2>&1 </dev/null &
  PID=$!; WAITED=0
  while kill -0 "$PID" 2>/dev/null; do
    if [ "$WAITED" -ge "$TIMEOUT" ]; then
      kill -9 "$PID" 2>/dev/null; wait "$PID" 2>/dev/null
      echo "limpiar: tiempo agotado tras ${TIMEOUT}s" >&2; return 124
    fi
    sleep 2; WAITED=$((WAITED + 2))
  done
  wait "$PID"; RC=$?; cat "$OUT"; return $RC
}

if [ -n "$CODEX" ] && [ "${DESLOP_WRITER:-claude}" != "gpt" ]; then
  # Escribió Claude (o Gemini, o un modelo local) -> limpia GPT.
  # -o guarda solo el último mensaje del modelo, sin banners ni el prompt.
  ANS="$(mktemp)"
  run_bounded "$CODEX" exec --skip-git-repo-check --sandbox read-only -o "$ANS" "$FULL" >/dev/null
  RC=$?
  if [ $RC -ne 0 ]; then rm -f "$ANS"; [ $RC -eq 124 ] && exit 124; echo "limpiar: codex falló ($RC)" >&2; exit $RC; fi
  emit_copy <"$ANS"; rm -f "$ANS"
elif [ -n "$CLAUDE" ] && [ "${DESLOP_WRITER:-claude}" = "gpt" ]; then
  # Escribió GPT -> limpia Claude. Se captura antes de partir: en una tubería manda
  # el estado del ÚLTIMO comando y un 124 se perdería.
  CLAUDE_OUT="$(run_bounded "$CLAUDE" -p "$FULL")" || exit $?
  printf '%s\n' "$CLAUDE_OUT" | emit_copy
else
  # Solo hay a mano la CLI de la misma familia que escribió el borrador. Usarla sería
  # que el modelo se corrija a sí mismo, justo lo que este script existe para evitar.
  echo "limpiar: no encuentro la CLI de la otra familia (un borrador de Claude necesita" >&2
  echo "codex; uno de GPT necesita claude). Pega el bloque de abajo en el chat de la otra familia:" >&2
  echo >&2
  printf '%s\n' "$FULL"
  exit 127
fi
