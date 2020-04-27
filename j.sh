#!/bin/bash
#Takes Japanese text from STDIN, looks it up on Jim Breen's WWWJDIC (http://nihongo.monash.edu/cgi-bin/wwwjdic?1C) and stores it in "j勉強"
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
curl -sL http://nihongo.monash.edu/cgi-bin/wwwjdic?1MUJ$1 | pup 'label:nth-child(2) text{}' | tail -n 2 >> /data/j勉強
echo "$1 saved to j勉強 file."
cat ../data/j勉強
