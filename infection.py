"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import sys
import unicodedata
import thinkplot
import thinkstats2
from database import select, connect


def un_i18n(ustr):
    return unicodedata.normalize('NFKD', ustr).encode('ascii', 'ignore')

def to_filename(ustr):
    return '_'.join(un_i18n(unicode(ustr)).split())

def main():
    connect(sys.argv[1])
    keys = [{'country': c, 'pathogen': p, 'antibiotic': a} for c, p, a in 
        select('earsnet', ('country', 'pathogen', 'antibiotic'), distinct=True)]

    for k in keys:
        print k
        ig = {year: float(i) / n for year, i, n in select('earsnet', ('year', 'i', 'n'), k)}
        if sum(ig.values()) == 0:
            print u'Zero probability for {country} {pathogen} {antibiotic}, skipping...'.format(**k)
            continue
        # form the pmf
        #pmfia = thinkstats2.MakePmfFromDict(ia, 'infection rate')
        pmf= thinkstats2.MakePmfFromDict(ig, 'infection rate')
        #pmf = thinkstats2.MakePmfFromList(irate, 'infection rate')
        print 'mean', pmf.Mean()
        print 'var', pmf.Var()
        
        # plot the Pmfs
        thinkplot.Pmf(pmf)
        thinkplot.Save(xlabel='Year',
                       ylabel='Infection rate',
                       title=un_i18n(u'PMF {pathogen}/{antibiotic} Infection Rates in {country}'.format(**k)),
                       root=to_filename(u'infection/i{country}_{pathogen}_{antibiotic}'.format(**k)))
 
if __name__ == '__main__':
    main()
