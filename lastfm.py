from argparse import ArgumentParser
from datetime import datetime
import requests
import traceback
import json
import sys
import os

last_url = 'http://ws.audioscrobbler.com/2.0/'
last_user = 'lesthack'
last_apikey = '17bd7f0d94443f6339322ec910429126'

argp = ArgumentParser(
    prog='lesthackbot',
    description='Bot',
    epilog='GPL v3.0',
    version='1.0'
)
argp.add_argument('-s', '--scrobbler', action='store_true', help='Scrobbler')
argp.add_argument('-d', dest='destiny', action='store', help='Path.', default=False)
args = vars(argp.parse_args())

if not args['destiny'] or not args['scrobbler']:
    argp.print_help()
else:
    params = {
        'method': 'user.getRecentTracks',
        'limit': 1,
        'user': last_user,
        'page': 1,
        'api_key': last_apikey,
        'format': 'json'
    }

    try:
        r = requests.get(last_url, params=params)
        json_response = json.loads(r.content)

        album = json_response['recenttracks']['track'][0]['album']['#text']
        artist = json_response['recenttracks']['track'][0]['artist']['#text']
        track = json_response['recenttracks']['track'][0]['name']

        if len(album) == 0: album = 'unknown'
        if len(artist) == 0: artist = 'unknown'
        if len(track) == 0: track = 'unknown'

        last_track = ''
        current_track = u'{artist} - {album} - {track}'.format(
            artist=artist,
            album=album,
            track=track
        ) 
        scrobbler_file = '{base}/{day}.md'.format(base=args['destiny'], day=str(datetime.now().day).zfill(2))
        if not os.path.isfile(scrobbler_file):
            sf = open(scrobbler_file, 'w')
            sf.write('#Log of {day} day\n\n'.format(day=str(datetime.now().day).zfill(2)))
        else:
            sf = open(scrobbler_file, 'r')
            last_track = str(sf.readlines()[-1][6:]).strip()
            sf.close()
            sf = open(scrobbler_file, 'a')
        if last_track != current_track:
            sf.write(u'\n{hour}:{minute} {track}'.format(
                hour=str(datetime.now().hour).zfill(2),
                minute=str(datetime.now().minute).zfill(2),
                track=current_track)
            )
        sf.close()
    except Exception as e:
        print 'Error: ',e
        traceback.print_exc(file=sys.stdout) 
