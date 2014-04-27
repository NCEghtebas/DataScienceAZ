import os
import sys
import re

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
	m = re.search(r'\$([0-9\.]+)\s+(\w*)\s?',data)
	if m is None:
		return None
	if(m.group(2) == 'billion'):
		return float(m.group(1) ) * 1e9
	elif(m.group(2) == 'trillion'):
		return float(m.group(1)) *1e12


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

stats= {
	2001: currency,2002: percentage,2003: percentage,2012:percentage,
	2021: raw,2032:raw,2034: percentage, 2046:percentage,
	2048:percentageGroup('agriculture', 'services', 'industry'),
	2056: currency,2059: raw, 2066:rate}

def main():
	for statnum, function in stats.items():
		print statnum
		for datum in retreivedata('France', statnum):
			if function is not None and datum[1] is not None:
				print (datum[0], function(datum[1]))
				pass
			# print datum

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