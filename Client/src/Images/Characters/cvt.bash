#!/bin/bash
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
FILES=`find .`
for f in $FILES
do
  echo "$f"
done
# restore $IFS
IFS=$SAVEIFS
