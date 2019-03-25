#!/usr/bin/sed -f

# Purpose: Expand the abbreviated notation of the states.
# Usage:{{{
#
#     $ ./nameState.sed list
#     John Daggett, 341 King Road, Plymouth, Massachusetts~
#     Alice Ford, 22 East Broadway, Richmond, Virginia~
#     Orville Thomas, 11345 Oak Bridge Road, Tulsa, Oklahoma~
#     Terry Kalkas, 402 Lans Road, Beaver Falls, Pennsylvania~
#     Eric Adams, 20 Post Road, Sudbury, Massachusetts~
#     Hubert Sims, 328A Brook Road, Roanoke, Virginia~
#     Amy Wilde, 334 Bayshore Pkwy, Mountain View, California~
#     Sal Carpenter, 73 6th Street, Boston, Massachusetts~
#}}}

s/ CA/, California/
s/ MA/, Massachusetts/
s/ OK/, Oklahoma/
s/ PA/, Pennsylvania/
s/ VA/, Virginia/
