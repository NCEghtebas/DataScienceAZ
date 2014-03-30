#!/usr/bin/env python2

import sys
import csv
import psycopg2


def make_table(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS EARSNet
        (pathogen TEXT, antibiotic TEXT, year SMALLINT, country TEXT,
        s SMALLINT, i SMALLINT, r SMALLINT, n SMALLINT, 
        UNIQUE(pathogen, antibiotic, year, country));''')


def upload_row(cur, row_dict):
    cur.execute('''INSERT INTO EARSNet
        (pathogen, antibiotic, year, country, s, i, r, n) VALUES
        (%(pathogen)s, %(antibiotic)s, %(year)s, %(country)s,
        %(s)s, %(i)s, %(r)s, %(n)s);''', row_dict)


def parse_csv(cur, filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            upload_row(cur, {
                'country': row[0],
                'year': int(row[1]),
                'antibiotic': row[2],
                's': int(row[3]),
                'i': int(row[4]),
                'r': int(row[5]),
                'n': int(row[6]),
                'pathogen': row[10]
            })


def main():
    database = {
        'host': 'alethea.io',
        'database': 'olinaz',
        'user': 'olinaz',
        'password': 'linezolid'
    }
    print 'Connecting...',
    conn = psycopg2.connect(**database)
    print 'Done'
    cur = conn.cursor()
    make_table(cur)
    conn.commit()
    for filename in sys.argv[1:]:
        print 'Uploading {0}...'.format(filename),
        parse_csv(cur, filename)
        conn.commit()
        print 'Success'


if __name__ == '__main__':
    main()
