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
			if country in line:
				return ' '.join(line.split())

def retreivefn(statnum):
	for year in os.listdir('factbook'): 
		fn = os.path.join('factbook', year, '{0}.txt'.format(statnum))
		if os.path.exists(fn):
			yield (int(year), fn)


def retreivedata(country, statnum):
	for year, fn in retreivefn(statnum):
		yield (year, finddata(country, fn))


def raw(data):
	return data

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
	2001: Stat(currency, 'gdp', 'gdp MONEY', 1),
	2002: Stat(percentage, 'pop_growth_rate', 'rate REAL', 1),
	2003: Stat(percentage, 'real_gdp', 'gdp MONEY', 1),
	2021: Stat(raw, 'natural_hazards', 'hazards TEXT', 1),
	2032: Stat(raw, 'current_environmental_issues', 'enviornmental TEXT', 1),
	2034: Stat(percentage, 'militray_expenditure', 'military REAL', 1), 
	2046: Stat(percentage, 'poverty_population', 'poverty REAL', 1),
 	2048: Stat(percentageGroup('agriculture', 'services', 'industry'),
 			   'labor_force',
 			   'agriculture REAL, services REAL, industry REAL',
 			   3),
	2056: Stat(currency, 'budget' ,'budget MONEY', 1),
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
						print datum[0], value
						insert_row(conn, datum[0], country, stat, value)
	conn.commit()

if __name__ == '__main__':
    main()


'''  
2001 - GDP
2002- pop growth rate
2003- real gdp
2010- age strucure
2011- coordinates
2012- GDP compisition by sector (i.e. percentge agriculture, industry, or services)
2018- sex ratio
2021- natural hazards
2032- enviornmental "current issues"
2034- military expenditure
2038- electricity production (kwh)
2042- consumption (kwh)
2046- population below poverty line
2048- labor force by ocupation
2054- birth rates
2056- budget
2059- climate
2060- coastline1
2061- import partners
2066 - death rate
2075- ethnic groups
2078- exports
2079- debt
2085- roadways
2086- illicit drugs
2093- waterways
2102- life expectancy
2112- net migration rate
'''