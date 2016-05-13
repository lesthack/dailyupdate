path="$HOME/dailyupdate"
music_path="$path/music"
date=`date +"%Y-%m-%d %H:%M"`
year=`date +"%Y"`
month=`date +"%m"`

. ~/.keychain/`/bin/hostname`-sh
cd $path

if [ ! -d "$music_path" ]; then
    mkdir $music_path
fi

if [ ! -d "$music_path/$year" ]; then
    mkdir $music_path/$year
fi

if [ ! -d "$music_path/$year/$month" ]; then
    mkdir $music_path/$year/$month
fi

# scrobbling
python lastfm.py -p "$path" -s

git add *
git commit -m "Changes on $date"
git push origin master
