import os
import urllib.request
import re
import sys
import time

def get_item_names(api_key):
"""
    Gets the name of all items currently known on the CS:GO steam market.
    Queries item_url for a string containing all known sellable CS:GO items, returning into ret_url.
    Finds all market_hash_names contained in the return string using regular expression re_m_name.
    Matches are put into matches and written with proper escaping to item names.txt.
    Querying steam market for prices using these names is commented out as it is rate limited to 20 calls/minute
    and that is too slow for ~7000 items.

    Keyword arguments:
        api_key -- string of an api key provided by http://csgo.steamlytics.xyz/api
"""
    re_m_name = re.compile(r'\"market_hash_name\":\"(.+?)\"')
    item_url = 'http://api.csgo.steamlytics.xyz/v1/items/?key=%s' % (api_key)
    ret_url = urllib.request.urlopen(item_url)
    matches = re_m_name.findall(ret_url.read().decode('utf-8'))

    f = open('item names.txt', 'w')
    for names in matches:
        names_escaped = urllib.parse.quote(names)
        names_proper = names_escaped.replace('%5Cu2605%20', '%E2%98%85%20')
        single_item_url = 'http://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name=%s' 
                            % (names_proper)
        print(names, file=f, sep='\n')
        #time.sleep(3.1)
        #print(urllib.request.urlopen(single_item_url).read().decode('utf-8'), file=f, sep='\n')

if __name__ == '__main__':
    get_item_names(str(sys.argv[1]))
