#!/usr/bin/env python
# -*- coding: utf-8 -*-


import httplib
import os
import sys

class Lister:

    def __init__(self, listOfDirs):
        self._lod = listOfDirs

    def printOut(self):
        for d in self._lod:
            print('-------------------- %s' % d)
            wplink = self.findWikipedia(self.google(self.clean(d)))
            print("\n%s - %s" % (wplink, self.getContent(wplink)))

    def getContent(self, link):
        baseurl = link.split('/')[2]
        url = '/'.join(link.split('/')[3:])
        url = url.replace('%25C3%25A4', 'ä').replace('%25C3%25BC', 'ü').replace('%25C3%25B6', 'ö').replace('%25E2%2580%2593', '–')
        print baseurl, url
        h = httplib.HTTPConnection(baseurl, 80, timeout = 10)
        h.request("GET", '/' + url, headers = {'User-Agent':'film info script, cbecker@nachtwach.de (private use only)'})
        res = h.getresponse()
        r = res.read()
        pos = r.find('toctitle')
        lines = r[pos - 1500:pos].splitlines()
        out = ''
        next = False
        for line in lines:
            if next:
                if line.find('<table') >= 0:
                    next = False
                else:
                    out += line

            if line.find('</div>') >= 0:
                next = True
        return out

    @staticmethod
    def clean(d):
        d = d.replace('.', ' ')
        first = d.split('-')[0]
        return first

    @staticmethod
    def google(s):
        tos = s.replace(' ', '+')
        tos = "/search?ie=UTF-8&q=%s" % tos
        print tos
        return tos

    @staticmethod
    def stripLink(r):
        wikip = r.find('de.wikipedia')
        if (wikip < 0):
            wikip = r.find('en.wikipedia')
        if wikip < 0: return None
        endpos = r.find('&amp', wikip)
        res = r[wikip - len('http://'):endpos]
        return res

    @staticmethod
    def findWikipedia(url):
        google = 'www.google.de'
        h = httplib.HTTPConnection(google, 80, timeout = 10)
        h.request("GET", url)
        res = h.getresponse()
        r = res.read()
        res = Lister.stripLink(r)
        if res is not None:
            return res
        else:
            return 'http://' + google + url

if __name__ == '__main__':
    sdir = sys.argv[1]
    print sdir
    lod = []
    for d in os.listdir(sdir + '/'):
        if os.path.isdir(os.path.join(sdir, d)):
            lod.append(d)
    lister = Lister(lod)
    lister.printOut()
