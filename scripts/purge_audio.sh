#!/bin/bash
find /var/www/html/eoc/audio -type f -name '*_[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9].wav' -exec sh -c 'fdate="${1%_[0-9][0-9]_[0-9][0-9].wav}"; fdate="${fdate##*_}";ndate=$(echo $fdate | sed 's/-/\//g'); n2date=$(date -d $ndate +%Y/%m/%d);  [ "$n2date" "<" "$(date  -d "0 days ago" "+%Y/%m/%d")" ] && rm "$1"' find-sh {} \;
