#!/bin/bash

if [[ $# -lt 3 ]]; then
  printf -- "Usage: $ gres <pat> <rep> <file>\n"
  exit 1
elif [[ ! -f "$3" ]]; then
  printf -- "%s is not a file.\n" "$3"
  exit 1
fi

A="$(tr 'x' '\001' <<<'x')"
pat="$1"
rep="$2"
file="$3"
sed "s${A}${pat}${A}${rep}${A}" "${file}"

