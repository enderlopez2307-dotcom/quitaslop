#!/usr/bin/env bash
# Genera el corpus de IA: cada encargo de briefs.tsv (o de $BRIEFS) con una familia de modelos, en ia/ (o en $DEST).
#   gen.sh claude | gpt | gemma
set -u
FAM="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../${DEST:-ia}"
CODEX=/Applications/Codex.app/Contents/Resources/codex-cli/bin/codex
LMS=$HOME/.lmstudio/bin/lms
cd "${TMPDIR:-/tmp}"
while IFS=$'\t' read -r id fmt reg prompt; do
  f="$OUT/$id-$fmt-$reg-$FAM.md"
  [ -s "$f" ] && continue
  p="$prompt Responde solo con el texto final."
  case "$FAM" in
    claude) claude -p --model sonnet "$p" > "$f" 2>/dev/null </dev/null ;;
    gpt)    $CODEX exec --skip-git-repo-check --sandbox read-only -o "$f" "$p" >/dev/null 2>&1 </dev/null ;;
    gemma)  $LMS chat google/gemma-4-12b-qat -p "$p" 2>/dev/null </dev/null \
              | awk '{a[NR]=$0} /<\/think>/{t=NR} END{for(i=t+1;i<=NR;i++)print a[i]}' > "$f" ;;
  esac
  echo "$FAM $id $(wc -w < "$f")"
done < "$HERE/${BRIEFS:-briefs.tsv}"
