# Add to .bash_profile next line:
# DAILYPATH="$HOME/dailyupdate"
DAILYPATH="$HOME/code/dailyupdate/"

loginout_path="$DAILYPATH/loginout"
date=`date +"%Y-%m-%d %H:%M"`
year=`date +"%Y"`
month=`date +"%m"`
day=`date +"%d"`

. ~/.keychain/`/bin/hostname`-sh

cd $DAILYPATH

if [ ! -d "$loginout_path" ]; then
    mkdir $loginout_path
fi

if [ ! -d "$loginout_path/$year" ]; then
    mkdir $loginout_path/$year
fi

if [ ! -d "$loginout_path/$year/$month" ]; then
    mkdir $loginout_path/$year/$month
fi

logtext="$date: $1"
echo "$date: $1" >> "$loginout_path/$year/$month/$day"

git pull origin master-grey
git add $loginout_path
git commit -m "Log on $date"
git push origin master-grey
