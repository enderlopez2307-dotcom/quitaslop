#!/usr/bin/env bash
# Control: READMEs en español de proyectos MIT que no se usaron al elegir las reglas.
set -u
OUT="$(cd "$(dirname "$0")/../humano-control" && pwd)"
TSV="$(dirname "$0")/../fuentes-humano-control.tsv"
i=0
while read -r repo region; do
  sha=$(gh api "repos/$repo/commits?until=2021-12-31T23:59:59Z&per_page=1" --jq '.[0].sha' 2>/dev/null) || continue
  date=$(gh api "repos/$repo/commits/$sha" --jq '.commit.committer.date[:10]' 2>/dev/null)
  for f in README.md readme.md Readme.md README.MD; do
    body=$(curl -sf "https://raw.githubusercontent.com/$repo/$sha/$f") && break
  done
  [ -n "${body:-}" ] || continue
  n=$(printf '%s' "$body" | wc -w | tr -d ' ')
  es=$(printf '%s' "$body" | tr 'A-Z' 'a-z' | grep -oE '\b(el|la|los|las|que|para|con|una|del|se|es)\b' | wc -l | tr -d ' ')
  [ "$n" -ge 120 ] && [ $((es * 100 / n)) -ge 5 ] || { echo "skip $repo n=$n es=$es"; body=""; continue; }
  i=$((i + 1)); name=$(printf 'control-readme-%02d' $i)
  printf '%s\n' "$body" > "$OUT/$name.md"
  printf '%s\treadme\t%s\tMIT\t%s\thttps://github.com/%s/blob/%s/README.md\n' "$name" "$region" "$date" "$repo" "$sha" >> "$TSV"
  echo "$name $repo $n"; body=""
done <<'L'
datosgobar/portal-andino latam
juandbc/festivos-colombia latam
SVelizDonoso/taketv latam
hectorespert/python-oligo espana
PythonistaMX/py101 latam
L
