#!/bin/bash

# Purpose: Run a sed script on a set of input files.{{{
#
# A backup of each file is made before the script edits it in-place.
#
# You can restore a file by running `$ mv file.bak file`.
#}}}
# Usage:
#     $ runsed.sh script.sed file ...

SCRIPT="$1"
EXT="${SCRIPT##*.}"

if [[ $# -lt 2 ]]; then
  printf -- 'Usage:  %s <script> <file>...\n' "$(basename "$0")"
  printf -- 'Example:  %s ./sed.sed myfile\n' "$(basename "$0")"
  exit 1
elif [[ "${EXT}" != 'sed' ]]; then
  printf -- 'The first argument must be a sed script!\n'
  exit 1
fi

# Ignore the sed script; we don't want it to edit itself.
shift 1

for file in "$@"; do
  printf -- 'editing %s: \n' "${file}"
  # `-s file`: True if file exists and has a size greater than zero.
  if [[ -s "${file}" ]]; then
    # Note the usage of `$$` as a suffix to create a unique temporary file name.{{{
    #
    # It's not  really reliable though,  because a file named  `file12345` could
    # already  exist in  the  directory, in  which case  the  next command  will
    # overwrite it.
    #}}}
    # This command assumes that your script begins with a shebang `/usr/bin/sed -f`.{{{
    #
    # If it doesn't, you will have to replace the command with:
    #
    #     sed -f "${SCRIPT}" "${file}" >"/tmp/${file}$$"
    #}}}
    "${SCRIPT}" "${file}" >"/tmp/${file}$$"
    if [[ ! -s "/tmp/${file}$$" ]]; then
      printf -- '  Sed produced an empty file\n'
      printf -- '   - check your sed script.\n'
    else
      # cmp - compare two files byte by byte
      # `-s` (`--quiet`, `--silent`): suppress all normal output
      if cmp -s "${file}" "/tmp/${file}$$"; then
        printf -- '  file not changed\n'
      else
        mv "${file}" "${file}.bak"  # save original, just in case
        cp "/tmp/${file}$$" "${file}"
      fi
      printf -- '  done\n\n'
    fi
    rm -f "/tmp/${file}$$"
  else
    printf -- '  original file is empty.\n'
  fi
done
printf -- 'all done\n'

