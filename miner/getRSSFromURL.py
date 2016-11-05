#!/usr/bin/env python

""" get RSS feed URLs from a website's content

    input: website URL
    output: list of rss feeds

    depends: BeautifulSoup

License:
            All rights reserved.

    Copyright 2015 Mark Menkhus

    Licensed under the Apache License, Version 2.0 (the "License");

    You may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

__author__ = "Mark Menkhus; menkhus@icloud.com"
__version__ = ".1"

import urllib2
from BeautifulSoup import BeautifulSoup
import re


def getRSSFromSite(siteURL=r'http://www.news.com'):
    """ read a web site, and return the RSS feed for
    that particular page.

    idea source: internet, accessed Feb 22, 2015, http://www.quora.com/What-is-
    the-best-Python-library-for-detecting-a-websites-RSS-feeds-s-using-the-
    root-URL
    """
    try:
        page = urllib2.urlopen(siteURL)
        soup = BeautifulSoup(page)
        link = soup.find('link', type='application/rss+xml')
        if link['href']:
            return link['href']
        else:
            return None
    except Exception, msg:
        #print "getRSSFromURL: nonfatal, getRSSFromSite: %s, %s" % (siteURL, msg)
        return None


def getURLsFromPage(page="no data here"):
    """ read a web page, and return the href URLs from that page
    """
    try:
        page = urllib2.urlopen(page)
        soup = BeautifulSoup(page)
    except Exception, msg:
        #print "getRSSFromURL: nonfatal, getURLsFromPage: %s" % (msg, )
        return None
    links = []
    for tag in soup.findAll('a', href=True):
        if re.search(r'http://', tag['href']):
            links.append(tag['href'])
    if links:
        return set(links)
    else:
        return None


def getRSSFromURL(site='http://www.slashdot.org'):
    """ get RSS feed URLs from a website's content

        input: website URL
        output: list of rss feeds on that page, and on
        the linked pages.
    """
    rss = []
    # get rss href links on page
    rss.append(getRSSFromSite(site))
    # get urls on page
    urls = getURLsFromPage(site)
    if urls:
        for each in urls:
            item = getRSSFromSite(each)
            if item:
                if re.search('http', item, re.IGNORECASE):
                    rss.append(item)
    if rss:
        return set(rss)
    else:
        return None


def main():
    """ input url on command line, display other urls found on
    page, and display  each rss href on referred pages
    """
    import sys
    if len(sys.argv) > 1:
        website = sys.argv[1]
        rss = getRSSFromURL(website)
        print "getting RSS feeds from %s" % (website,)
        for each in rss:
            print each
        sys.exit()
    else:
        print "usage: getRSSFromURL url"
        sys.exit(1)

if __name__ == '__main__':
    main()
