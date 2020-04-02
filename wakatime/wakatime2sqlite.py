#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from argparse import ArgumentParser
import sqlite3
import json
import os
import sys

filename = None
sqlitefile = None

def resume(sqlitefile):
    try:
        db = sqlite3.connect(sqlitefile)
        db.text_factory = str
    except Error as e:
        print('Error: ',e)
        sys.exit(0)

    cursor = db.cursor()
    query_day = '''
        SELECT 
            date_at,
            CAST((total/3600) as int) as horas,
            CAST((total/60) as int) - CAST((60*CAST((total/3600) as int)) as int) as minutos,	
            total
        FROM wakatime_day
    '''
    cursor.execute(query_day)
    rows_days = cursor.fetchall()

    cursor = db.cursor()
    query_record = '''
        SELECT 
            date_at,
            type,
            name,
            CAST((SUM(total)/3600) as int) as horas,
            CAST((SUM(total)/60) as int) - CAST((60*CAST((SUM(total)/3600) as int)) as int) as minutos,	
            SUM(total)
        FROM wakatime_record
        GROUP BY
            date_at,
            type,
            name;
    '''
    cursor.execute(query_record)
    rows_records = {}
    for row in cursor.fetchall():
        if row[0] not in rows_records:
            rows_records[row[0]] = {}
        if row[1] not in rows_records[row[0]]:
            rows_records[row[0]][row[1]] = {}
        str_total = ''
        if int(row[3]) > 0:
            str_total += '{} hours '.format(row[3])
        if int(row[4]) > 0:
            str_total += '{} minutes '.format(row[4])
        if str_total != '':
            rows_records[row[0]][row[1]][row[2]] = str_total.strip()

    types={
        'languages': 'Languages', 
        'editors': 'Editors', 
        'operating_systems': 'Operating Systems'
    }
    for row in rows_days:
        year, month, day = row[0].split('-')
        if(not os.path.isdir(os.path.join(year, month))):
            os.makedirs(os.path.join(year, month))
        fileday = open(os.path.join(year,month,day+'.md'), 'w')
        fileday.write('# Wakatime {}\n\n'.format(row[0]))
        fileday.write('Time Total: **{} hours {} minutes**\n\n'.format(row[1], row[2]))
        for t in types.keys():
            if row[0] in rows_records and t in rows_records[row[0]]:
                fileday.write('### {}:\n'.format(types[t]))
                for lang in rows_records[row[0]][t].keys():
                    fileday.write('- {}: **{}** \n'.format(lang, rows_records[row[0]][t][lang]))
            fileday.write('\n')
        fileday.close()
        print('{} Done !'.format(row[0]))
    db.close()


def wakatime2sqlite(filename, sqlitefile_output):
    f = open(filename,'r')
    wakatime = json.load(f)

    db = sqlite3.connect(sqlitefile_output)
    db.text_factory = str

    # Create tables
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wakatime_day(
            date_at DATE,
            total INTEGER
        );
    ''')
    cursor.execute('DELETE FROM wakatime_day;')
    db.commit();

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wakatime_record(
            date_at DATE,
            type TEXT,
            name TEXT,
            total INTEGER
        );
    ''')
    cursor.execute('DELETE FROM wakatime_record;')
    db.commit();

    # iter
    cursor = db.cursor()
    for day in wakatime['days']:
        date_at = day['date']
        total = day['grand_total']['total_seconds']
        cursor.execute('INSERT INTO wakatime_day(date_at, total) VALUES(?,?)', [date_at, total])
        # various
        types = ['editors', 'languages', 'categories','operating_systems']
        for t in types:
            for i in day[t]:
                cursor.execute(
                        'INSERT INTO wakatime_record(date_at, type, name, total) VALUES(?,?,?,?);', 
                        [date_at, t, i['name'], i['total_seconds']]
                )
        # projects
        for p in day['projects']:
            cursor.execute(
                'INSERT INTO wakatime_record(date_at, type, name, total) VALUES(?,?,?,?);',
                [date_at, 'projects', p['name'], p['grand_total']['total_seconds']]
            )
    db.commit()

    print('Done. File {} created'.format(sqlitefile_output))

argp = ArgumentParser(
    prog = 'Wakatime2SQLite',
    description = 'Wakatime2SQLite allow you to transform your data to SQLite database',
    epilog = 'GPL v3.0',
    #version = '3.0'
)
actions = ['import', 'resume']
argp.add_argument('-a', dest='action', choices=actions, help='Action', required=True)
argp.add_argument('-i', help='Input file', required=True)
argp.add_argument('-o', help='Output file')
argp.add_argument('-s', help='Start date')
argp.add_argument('-e', help='End date')
args = vars(argp.parse_args())

if args['action'] not in actions:
    argp.print_help()
elif args['action'] == 'import':
    sqlitefile = 'wakatime.db'
    filename = args['i']
    if 'o' in args and args['o'] is not None:
        sqlitefile = args['o']
    if not os.path.isfile(filename):
        argp.error('File {} not exists'.format(filename))
    itsok = 'y'
    if os.path.isfile(sqlitefile):
        itsok = input('The file {} exist\'s right now, do you want replace? [y/n]: '.format(sqlitefile))
    if itsok.strip() in ['y','Y']:
        wakatime2sqlite(filename, sqlitefile)
elif args['action'] == 'resume':
    sqlitefile = args['i']
    if not os.path.isfile(sqlitefile):
        argp.error('File {} not exists'.format(filename))
    resume(sqlitefile)
    
