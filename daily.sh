path="$HOME/dailyupdate"
music_path="$path/music"
date=`date +"%Y-%m-%d %H:%M"`
year=`date +"%Y"`
month=`date +"%m"`

# add this code to .bash_profle or .zshrc
# Link: http://serverfault.com/questions/92683/execute-rsync-command-over-ssh-with-an-ssh-agent-via-crontab/236437#236437
#if [ -x /usr/bin/keychain ]; then
#    /usr/bin/keychain --quiet --clear $HOME/.ssh/git_rsa
#fi

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

# Only path music
git pull origin dev
git add music
git commit -m "Lastfm: $date"
git push origin master
