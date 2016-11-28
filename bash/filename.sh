#!/bin/bash

printf $0
printf "\n"
printf ${0##*/}
printf "\n"
printf ${0%.*}
printf "\n"
a=`echo ${0##*/}`   # remember you can not give space when assigning
printf ${a%.*}
printf "\n"

# echo ${filename#*.}
# echo ${filename%.*}

# $ ./shortest.sh
# After deletion of shortest match from front: string.txt
# After deletion of shortest match from back: bash.string
