#!/bin/bash
# Source: https://hackernoon.com/how-to-hack-github-kind-of-12b08a46d02e

Y=`date +"%Y"`
D31=(01,03,05,07,08,10,12)
path="loginout"

commit(){
  year=`date +"%Y"`
  month=`date +"%m"`
  day=`date +"%d"`
  path_file=""
  if [ "$(($year - $1))" -ge 0 ] && [ "$((10#$month - 10#$2))" -ge 0 ]; then
    if [ $month = $2 ]; then
      if [ "$((10#$day - 10#$3))" -ge 0 ]; then
        #echo "En el mes: $year-$month-$day $1-$2-$3"
        path_file="$path/$1/$2/$3"
      fi
    else
      path_file="$path/$1/$2/$3"
    fi
  fi
  if [ ! $path_file = "" ]; then
    if [ ! -f $path_file ]; then
      echo "Add $path_file"
      echo "hacking github" > $path_file
      export GIT_COMMITTER_DATE="$1-$2-$3 12:00:00"
      export GIT_AUTHOR_DATE="$1-$2-$3 12:00:00"
      git add $path_file -f
      git commit --date="$1-$2-$3 12:00:00" -m "$1 $2 $3 hacking"
      git push origin master-grey
    fi
  fi
}

for M in {01..12}
do
  if [[ ${D31[*]} =~ $M ]]; then
    for D in {01..31}
    do
      commit $Y $M $D
    done
  else
    if [ $M = 02 ]; then
      for D in {01..28}
      do
        commit $Y $M $D
      done
    else
      for D in {01..30}
      do
        commit $Y $M $D
      done
    fi
  fi
done
