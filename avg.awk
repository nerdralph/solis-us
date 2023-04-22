#!/usr/bin/awk
# Ralph Doncaster 2023 public domain

BEGIN {
    FS=","
}

{
    ac += $2
    dc += $3
}

END {
    print ac " Wac / " dc " Wdc = " 100 * ac/dc "%"
}

