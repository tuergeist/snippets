#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 26.06.2012

@author: Christoph Becker <tuergeist@googlemail.com>
'''
import unittest
from list import Lister


class ListTest(unittest.TestCase):
    teststr = '''Chronicle
Inception-2010.DVDRip.XviD.AC3.5 1-eXceSs
Stieg.Larsson.Verdammnis.2-2009.GERMAN.DC.1080p.BluRay.x264-MiSFiTS
Elegy o die Kunst zu lieben-Drama.PCruz.106min
Das.gibt.Aerger-2012.BDRip.AC3.German.XviD
Stieg.Larsson.Verdammnis.1-2009.GERMAN.DC.1080p.BluRay.x264-MiSFiTS
Gelobtes Land
Die Paepstin
Safe.House
Stieg.Larsson.Verblendung-Millenium.1
Zeit.der.Trauer-German.2009.96min
Kooky
Die.Fremde-SibelKekilli.Tuerkendrama119min
In.Time-SciFi.109min.JustinTimberlake.OliviaWilde
New.York.fuer.Anfaenger-German.DVDRip.XviD
Yen Town
Der.Ruf.der.Wale-German.AC3.BDRiP.XViD
Die.Thomas.Crown.Affaere-1999.109min
Monday
Super8-SciFi.FSK12.112min
The.Grey.Unter.Woelfen-DVDRip.Line.Dubbed.German.XviD-VCF
Die.perfekte.Ex
Das.weisse.Band-German.720p.BluRay.x264-DEFUSED
Snow.White.and.the.Huntsman-TS.LD.German.iNTERNAL.XViD-AOE'''

    def test_grabName(self):
        lister = Lister(ListTest.teststr.split())
        lister.printOut()

if __name__ == '__main__':
    unittest.main()
