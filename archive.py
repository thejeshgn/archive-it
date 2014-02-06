#Well uses many scripts and also the parts written by me
#Thanks to
#For site map parsing
#https://gist.github.com/chrisguitarguy/1305010
#Archive.is for 
#http://blog.archive.is/post/45031162768/can-you-recommend-the-best-method-script-so-i-may-batch


from __future__ import with_statement 
from argparse import ArgumentParser

import requests
from BeautifulSoup import BeautifulStoneSoup as Soup
import re
import time

def parse_sitemap(url):
    resp = requests.get(url)
    
    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        return False
    
    # BeautifulStoneSoup to parse the document
    soup = Soup(resp.content)
    
    # find all the <url> tags in the document
    urls = soup.findAll('url')
    
    # no urls? bail
    if not urls:
        return False
    
    # storage for later...
    out = []
    
    #extract what we need from the url
    for u in urls:
        loc = u.find('loc').string
        #print loc
        prio = u.find('priority').string
        change = u.find('changefreq').string
        last = u.find('lastmod').string
        out.append([loc, prio, change, last])
    return out



def service_archiveis(url):
    payload = {'url': url}
    #r = requests.post("http://httpbin.org/post", data=payload)
    r       = requests.post("http://archive.is/submit/", data=payload)
    soup    = Soup(r.text)
    script  = soup.script
    urls    = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(script))
    return urls[0]

#print service_archiveis('http://thejeshgn.com')



if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store', dest='url', help='The file contain one url per line')
    options.add_argument('-o', '--output', action='store', dest='out', default='out.txt', help='Where you would like to save the results')
    options.add_argument('-s', '--service', action='store', dest='service', default='archiveis', help='What service do you like to use')

    args = options.parse_args()
    urls = parse_sitemap(args.url)
    if not urls:
        print 'There was an error in reading sitemap!'


    with open(args.out, 'w') as out:
        for u in urls:
            time.sleep(.5) 
            if args.service == 'archiveis':
                archive_url = service_archiveis(u[0])
            else:
                print "Please select a service to archive."
            line = u[0]+','+archive_url+'\n'
            print line
            out.write(line)
    print "Archived "+str(len(urls))+" number of URLs with "+str(service)        

