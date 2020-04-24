#!/bin/bash
#Takes Japanese text from STDIN, looks it up on Jim Breen's WWWJDIC (http://nihongo.monash.edu/cgi-bin/wwwjdic?1C) and stores it in "j勉強"
read input
curl -sL http://nihongo.monash.edu/cgi-bin/wwwjdic?1MUJ$input|pup 'label:nth-child(2) text{}' | tail -n 2 >> ../data/j勉強
