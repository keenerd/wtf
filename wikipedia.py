#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# https://en.wikipedia.org/w/index.php?title=List_of_computing_and_IT_abbreviations&action=edit

import re, urllib2
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

pull = lambda url: urllib2.urlopen(urllib2.Request(url))
wikip = lambda article: pull('https://en.wikipedia.org/w/index.php?title=%s&action=edit' % article)

# todo: List_of_file_formats

def stock():
    ad = defaultdict(list)
    for line in open('acronyms'):
        if '\t' not in line:
            continue
        line = line.strip()
        a,d = line.split('\t')
        ad[a].append(d)
    for line in open('acronyms.comp'):
        if '\t' not in line:
            continue
        line = line.strip()
        a,d = line.split('\t')
        ad[a].append(d)
    return ad

def exists(key, value, lut):
    key = key.upper()
    if key not in lut:
        return False
    value = value.upper()
    return any(v.upper()==value for v in lut[key])

def computing_abbrev():
    "This parser is very brittle, but the input is very well formed"
    wikip = open  # uncomment for local debug
    html = wikip('List_of_computing_and_IT_abbreviations').read()
    soup = BeautifulSoup(html)
    text = soup.textarea.contents[0]
    ad = defaultdict(list)
    for pair in re.findall('\* \[\[.*—.*', str(text)):
        try:
            a,_,d = pair.partition('—')
            a = a[4:].rpartition('|')[-1].replace(']]', '')
            d = d.replace('[[', '').replace(']]', '').replace('—', ' - ')
            ad[a].append(d.strip())
        except:
            #print 'failed on', pair
            continue
    return ad


def main():
    "build all the new lists"
    # okay, there is just the one for now
    ad = computing_abbrev()
    stk = stock()

    tech = open('acronyms.computing', 'w')
    tech.write('$ArchLinux: wikipedia computer abbrevs 2018-05-31\n\n')
    for a,ds in sorted(ad.items()):
        for d in ds:
            if exists(a, d, stk):
                continue
            tech.write('%s\t%s\n'% (a.upper(), d))
    tech.close()

if __name__ == '__main__':
    main()

