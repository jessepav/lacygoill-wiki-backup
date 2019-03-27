#!/usr/bin/sed -f

s/^$/.LP/
/^+  */d
s/^  *//
s/  */ /g
s/\.  */.  /g
