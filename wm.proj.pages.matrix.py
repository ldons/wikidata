#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2017 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pwb
import pywikibot
from wikidatafun import *

def main():
    site = pywikibot.Site('wikidata', 'wikidata')
    repo = site.data_repository()
    qq = [
        'Q4167836', #cats
        'Q4167410', #disambig
        'Q13406463', #lists
        'Q11266439', #templates
        'Q17633526', #wikinews article
    ]
    translations = {}
    langs = []
    for q in qq:
        item = pywikibot.ItemPage(repo, q)
        item.get()
        labels = item.labels
        for lang, label in labels.items():
            if not q in translations:
                translations[q] = {}
            if not lang in langs:
                langs.append(lang)
            translations[q][lang] = label
    langs.sort()
    rows = []
    c = 1
    for lang in langs:
        wplink = '[[:%s:|%s]] (<!--[https://%s.wikipedia.org/wiki/Special:ActiveUsers?username=&groups=sysop&wpFormIdentifier=specialactiveusers au]{{·}} [https://%s.wikipedia.org/wiki/Special:Recentchanges rc]{{·}} -->[[:Category:User %s|babel]])' % (lang, lang, lang, lang, lang)
        row = [str(c), wplink]
        for q in qq:
            if lang in translations[q]:
                row.append('[[%s|%s]]' % (q, translations[q][lang]))
            else:
                row.append('[[%s|no]]' % (q))
        rows.append(row)
        c += 1
    headersplain = ' !! '.join([translations[q]['en'] for q in qq])
    rowsplain = '\n|-\n| '.join([' || '.join(row) for row in rows])
    output = """
This page contains all available translations for different types of Wikimedia pages. Please, check the translations for your language, add the missing ones and fix any mistakes. Don't edit this table directly, click in the links and edit the labels there. A bot will update this table regularly. Thank you.

{| class="wikitable sortable plainlinks" style="text-align: center;font-size: 90%%;"
! # !! Language !! %s
|-
| %s
|}""" % (headersplain, rowsplain)
    #print(output)
    page = pywikibot.Page(site, 'User:Emijrp/Wikimedia project pages matrix')
    page.text = output
    page.save('BOT - Updating')

if __name__ == "__main__":
    main()