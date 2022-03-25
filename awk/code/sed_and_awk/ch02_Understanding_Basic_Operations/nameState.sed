#!/usr/bin/sed -f

# Purpose: expand abbreviated notation of states
# Test: `$ ./nameState.sed ./input/addresses`

s/ CA/, California/
s/ MA/, Massachusetts/
s/ OK/, Oklahoma/
s/ PA/, Pennsylvania/
s/ VA/, Virginia/
