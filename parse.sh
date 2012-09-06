#!/bin/bash

fname=$1

cat "$fname" | sed -e 's/<sms/\n<sms/g' | 
               sed -e 's/<mms/\n<mms/g' | 
               sed -e 's/<thread/\n<thread/g' |
               sed -e 's/<\/thread/\n<\/thread/g' > parsable.xml
