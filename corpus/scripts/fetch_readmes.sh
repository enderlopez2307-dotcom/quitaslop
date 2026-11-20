#!/usr/bin/env bash
# READMEs en español de proyectos MIT, en su último commit anterior a 2022.
set -u
OUT="$(cd "$(dirname "$0")/../humano" && pwd)"
TSV="$(dirname "$0")/../fuentes-humano.tsv"
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
  [ "$n" -ge 120 ] && [ $((es * 100 / n)) -ge 8 ] || { echo "skip $repo n=$n es=$es"; body=""; continue; }
  i=$((i + 1)); name=$(printf 'readme-%02d' $i)
  printf '%s\n' "$body" > "$OUT/$name.md"
  printf '%s\treadme\t%s\tMIT\t%s\thttps://github.com/%s/blob/%s/README.md\n' "$name" "$region" "$date" "$repo" "$sha" >> "$TSV"
  echo "$name $repo $n"; body=""
done <<'L'
datosgobar/portal-andino latam
kodetop/docker-php-mysql latam
jmrplens/TFG-TFM_EPS espana
arielcr/numero-a-letras latam
atscub/nautapy latam
jlobos/rut.js latam
NatanVilchis/termuxpy latam
Developero-oficial/php-mvc latam
datosgobar/georef-ar-api latam
JossMP/sunatphp latam
leoasis/workshop-pensando-en-react latam
brunocascio/docker-espanol latam
lecano/php-numero-a-letras latam
PythonistaMX/py101 latam
parzibyte/cotizaciones_web latam
juandbc/festivos-colombia latam
SVelizDonoso/taketv latam
hectorespert/python-oligo espana
Eitol/colombian-cedula-reader latam
joanby/python-ml-course espana
L
