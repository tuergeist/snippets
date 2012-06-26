#!/usr/bin/env python
print('hi')

import os
import httplib

def clean(d):
    d=d.replace('German','')
    d=d.replace('GERMAN','')
    d=d.replace('.',' ')
    return d
    
def google(s):
    tos = s.replace(' ','+')
    tos = "/search?ie=UTF-8&q=%s" % tos
    return tos

def findWikipedia(url):
    google = 'www.google.de'
    h = httplib.HTTPConnection(google, 80, timeout=10)
    h.request("GET", url)
    res =  h.getresponse()
    r = res.read()
    wikip = r.find('de.wikipedia')
    if wikip > 0:
        print r[wikip-8:wikip+50]
    else:
        print('http://' + google + url)
    
for d in os.listdir('.'):
    if os.path.isdir(d): print(findWikipedia(google(clean(d))))
