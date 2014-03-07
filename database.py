from urlparse import urlparse
import psycopg2
import psycopg2.extensions

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

conn = None

def connect(dsn):
    global conn
    conn = psycopg2.connect(dsn)

def columns_to_str(columns):
    if not columns:
        return '*'
    return ', '.join(columns)


def wheres_to_str(wheres):
    if not wheres:
        return ''
    return 'WHERE ' + ' AND '.join(('{0}=%({0})s'.format(k) for k in wheres.keys()))


def select(table, columns=None, wheres=None, distinct=False):
    cur = conn.cursor()
    dist_str = ''
    if distinct:
        dist_str = ' DISTINCT'
    cur.execute(
        '''SELECT{0} {1} FROM {2} {3};'''.format(
                dist_str, columns_to_str(columns), table, wheres_to_str(wheres)),
        wheres)
    return cur.fetchall()
