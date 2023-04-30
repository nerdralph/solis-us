#!/usr/bin/awk
# Ralph Doncaster 2023 public domain
# awk -f avg.awk file.csv

BEGIN { FS="," }

{ ac += $2; dc += $3 }

END { print ac " Wac / " dc " Wdc = " 100 * ac/dc "%" }

