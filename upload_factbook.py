'''
Script to upload CIA wolrd fact book data into database

Alethea and Chloe
4/30/14

'''
import os
import sys
import re
from database import select, connect
from collections import namedtuple


def getcountrylist():
    countries= select("earsnet", ["country"], distinct = True)
    countrylist=[]
    for country in countries:
        countrylist.append(country[0].decode('utf8'))
    return countrylist

def finddata(country, fn):
    with open(fn, 'r') as f:
        for line in f:
            line = ' '.join(line.split())
            if country in line:
                return ' '.join(line.split())

def retreivefn(statnum):
    for year in sorted(os.listdir('factbook')): 
        fn = os.path.join('factbook', year, '{0}.txt'.format(statnum))
        if os.path.exists(fn):
            yield (int(year), fn)


def retreivedata(country, statnum):
    for year, fn in retreivefn(statnum):
        yield (year, finddata(country, fn))


def raw(data):
    return data

def number(data):
    m = re.search(r'([0-9]{0,3}(,[0-9]{3,3}))(\s|$)', data)
    if m is None:
        return None
    return int(''.join(m.group(1).split(',')))

def currency(data):
    conversion = {'million': 1e6, 'billion': 1e9, 'trillion': 1e12}
    m = re.search(r'\$([0-9\.]+)\s+(\w*)\s?',data)
    if m is None:
        return None
    return float(m.group(1)) * conversion[m.group(2)]


def percentage(data):
    m = re.search(r'([0-9\.]+)\%', data)
    if m is None:
        return None
    return float(m.group(1))/100.0

def rate(data):
    m= re.search(r'([0-9\.]+)\s+deaths', data)
    if m is None:
        return None
    return float(m.group(1))/1000.0

def percentageGroup(*keywords):
    def innerPercentageGroup(data):
        res = []
        for keyword in keywords:
            m = re.search(r'{0}\W+([0-9\.]+)\%'.format(keyword), data)
            if m is None:
                res.append(None)
            else:
                res.append(float(m.group(1)) / 100)
        return res
    return innerPercentageGroup

Stat = namedtuple('Stat', ['func', 'name', 'columns', 'count'])

stats= {
    2001: Stat(currency, 'gdp', 'gdp BIGINT', 1),
    2119: Stat(number, 'population', 'population BIGINT', 1),
    2002: Stat(percentage, 'population_growth_rate', 'rate REAL', 1),
    2003: Stat(percentage, 'gdp_growth_rate', 'rate REAL', 1),
    2021: Stat(raw, 'natural_hazards', 'hazards TEXT', 1),
    2032: Stat(raw, 'current_environmental_issues', 'enviornmental TEXT', 1),
    2034: Stat(percentage, 'militray_expenditure', 'military REAL', 1), 
    2046: Stat(percentage, 'poverty_population', 'poverty REAL', 1),
    2048: Stat(percentageGroup('agriculture', 'services', 'industry'),
               'labor_force',
               'agriculture REAL, services REAL, industry REAL',
               3),
    2056: Stat(currency, 'budget' ,'budget BIGINT', 1),
    2059: Stat(raw, 'climate_description', 'climate TEXT', 1), 
    2066: Stat(rate, 'death_rate', 'rate REAL', 1)}

def create_tables(conn):
    cur = conn.cursor()
    for stat in stats.values():
        cur.execute('DROP TABLE IF EXISTS {0};'.format(stat.name))
        cur.execute(
            'CREATE TABLE {0} (year SMALLINT, country TEXT, {1});'.format(
                stat.name, stat.columns))

def insert_row(conn, year, country, stat, value):
    cur = conn.cursor()
    placeholder = '%s, %s' + ', %s' * stat.count
    values = [year, country]
    if isinstance(value, str):
        values.append(value)
    else:
        try:
            values.extend(value)
        except TypeError:
            values.append(value)
    cur.execute(
        'INSERT INTO {0} VALUES ({1});'.format(stat.name, placeholder),
        values)

def main():
    conn = connect(sys.argv[1])
    create_tables(conn)
    for country in getcountrylist():
        for statnum, stat in stats.items():
            for datum in retreivedata(country, statnum):
                if datum[1] is not None:
                    value = stat.func(datum[1])
                    if value is not None:
                        print stat.name, country, datum[0], value
                        insert_row(conn, datum[0], country, stat, value)
    conn.commit()

if __name__ == '__main__':
    main()
