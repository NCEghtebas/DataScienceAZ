import sys
import csv
from database import connect, select


def country_list():
    return [c[0] for c in select('earsnet', ('country',), distinct=True)]


def read_csv(country_filter):
    with open('sh.xpd.totl.zs_Indicator_en_csv_v2.csv') as f:
        f.readline()
        f.readline()
        r = csv.DictReader(f)
        for row in r:
            if row['Country Name'] in country_filter:
                for k, v in row.items():
                    if k.isdigit() and len(v) > 0:
                        yield row['Country Name'], int(k), float(v) / 100


def create_table(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS health_expendature;')
    cur.execute('''CREATE TABLE health_expendature (
                       country TEXT, year SMALLINT, expendature REAL
                );''')


def insert_row(conn, row):
    cur = conn.cursor()
    cur.execute('INSERT INTO health_expendature VALUES (%s, %s, %s);', row)


def main():
    conn = connect(sys.argv[1])
    create_table(conn)
    for row in read_csv(country_list()):
        insert_row(conn, row)
        print row
    conn.commit()


if __name__ == '__main__':
    main()
