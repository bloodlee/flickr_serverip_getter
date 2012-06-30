"""
In China, sometimes we can't access the "Global" servers of flickr.
In this case, we need to use East servers of flickr instead.

This script is used to get all East servers' ip addresses.
And then we can use these ip addresses in /etc/hosts.

Need at least Python 2.7.
"""

import argparse
import urllib2
import re
import socket
from BeautifulSoup import BeautifulSoup

FLICKR_TEST_PAGE_URL = "http://www.flickr.com/help/test"
FARM_NAME_COL_INDEX = 0
GLOBAL_SERVER_COL_INDEX = 1
EAST_SERVER_COL_INDEX = 2

class AddressInfo:
    def __init__(self, farmName, global_host, east_host, east_ip):
        self.farmName = farmName
        self.global_host = global_host
        self.east_host = east_host
        self.east_ip = east_ip

    def getFarmName(self):
        return self.farmName

    def getGlobalHost(self):
        return self.global_host

    def getEastIp(self):
        return self.east_ip

    def getEastHost(self):
        return self.east_host

def getServerName(status_icon_url):
    m = re.search("http://([^/]+)/", status_icon_url)
    return m.group(1)

if __name__ == '__main__':

    description = 'Parse Flickr Test Page and get the ip addresses of East servers'
    usage = "python flickr_serverip_getter.py"

    parser = argparse.ArgumentParser(description=description, usage=usage)
    options = parser.parse_args()

    print('parsing, please stand by...')
    response = urllib2.urlopen(FLICKR_TEST_PAGE_URL)
    html = response.read()

    # pass html to html parser
    soup = BeautifulSoup(html)

    trs = soup.find('div', id='Main').table.findAll('tr')

    addresses = []
    # skip the first row
    for row_index in range(1, len(trs)):
        tds = trs[row_index].findAll('td')

        # get farm name
        farm_name = tds[FARM_NAME_COL_INDEX].string

        # get global server host name
        global_server_status_icon_url = tds[GLOBAL_SERVER_COL_INDEX].a['href']
        global_server = getServerName(global_server_status_icon_url)

        # get east server host name
        east_server_status_icon_url = tds[EAST_SERVER_COL_INDEX].a['href']
        east_server = getServerName(east_server_status_icon_url)

        # get east server host ip address
        east_ip = socket.gethostbyname(east_server)

        addressInfo = AddressInfo(farm_name, global_server, east_server, east_ip)
        addresses.append(addressInfo)


    print ' ' * 10 + '|\t' + 'Global Host' + ' ' * 19 + '|\t' + 'East Host' + ' ' * 21 + '|\t' + 'East IP'
    print '------------------------------------------------------------------------------------------------'

    for i in range(len(addresses)):
        address = addresses[i]
        print '%-10s|\t%-30s|\t%-30s|\t%-20s' % (address.getFarmName(),
                                                 address.getGlobalHost(),
                                                 address.getEastHost(),
                                                 address.getEastIp())

    print
    print 'Copy following ip table to /etc/hosts (For Windows OS: C:\WINDOWS\system32\drivers\etc).'
    print
    for i in range(len(addresses)):
        address = addresses[i]
        print '%s %s'%(address.getEastIp(), address.getGlobalHost())
