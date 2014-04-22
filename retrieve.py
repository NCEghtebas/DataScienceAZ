import os
import sys

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


def main():
	for datum in retreivedata('France', 2212):
		print datum

if __name__ == '__main__':
    main()

