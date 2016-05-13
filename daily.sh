path="$HOME/dailyupdate"
music_path="$path/music"
date=`date +"%Y-%m-%d %H:%M"`
year=`date +"%Y"`
month=`date +"%m"`

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

#echo "." >> README.md
AGENT="ssh-agent -s"
if [ ! -d $HOME/.ssh/agent ]; then
    mkdir -p $HOME/.ssh/agent
fi
#
# Start an agent if there isn't one running already.
#
pid=`ps -u$LOGNAME | grep ssh-age | awk '{print $1}'`
if [ -z "$pid" ]; then
    $AGENT | grep -v echo > $HOME/.ssh/agent/$HOST & pid=$!
    sleep 1 # Let it fork and stuff
fi
ssh-add $HOME/.ssh/git_rsa

git add *
git commit -m "Changes on $date"
git push origin master
