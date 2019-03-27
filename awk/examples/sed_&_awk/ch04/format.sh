#!/bin/bash

eqn='' pic='' col=''
files='' options='' roff='ditroff -Tps'
sed="| sed '/---/!s/--/\\(em/g'"
while [[ $# -gt 0 ]]; do
   case $1 in
     -E) eqn='| eqn';;
     -P) pic='| pic';;
     -N) roff='nroff'  col='| col'  sed=;;
     -*) options="${options} $1";;
      *) if [[ -f $1 ]]
         then files="${files} $1"
         else printf -- 'format: %s: file not found\n' "$1"; exit 1
         fi;;
   esac
   shift
done
eval "cat ${files} ${sed} | tbl ${eqn} ${pic} | ${roff} ${options} ${col} | lp"

