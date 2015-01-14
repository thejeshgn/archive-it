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
import json
from easygui import * 

def getListOfSubSiteMaps(url):
    sitemaps = []
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if '200' != str(resp.status_code):
        return False
    
    # BeautifulStoneSoup to parse the document
    soup = Soup(resp.content)
    
    # find all the <url> tags in the document
    urls = soup.findAll('url')
    
    if not urls:
         sms = soup.findAll('sitemap')
         if sms:
            for sm in sms:
                loc =sm.find('loc').string
                sitemaps.append(loc)
    else:
        sitemaps.append(url)
    print  str(sitemaps)
    return sitemaps



def parse_sitemap(url):
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if '200' != str(resp.status_code):
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

def service_archiveorg(url):
    r1 = requests.get("https://web.archive.org/save/"+str(url))    
    r2 = requests.get("http://archive.org/wayback/available?url="+str(url))
    data = json.loads(r2.text)
    archived_snapshots = data["archived_snapshots"]
    if len(archived_snapshots):
        closet = archived_snapshots['closest']
        return closet['url']
    else:
        return "not yet"



def service_archiveis(url):
    payload = {'url': url}
    #r = requests.post("http://httpbin.org/post", data=payload)
    r = requests.post("http://archive.today/submit/", data=payload)
    soup    = Soup(r.text)
    script  = soup.script
    urls    = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(script))
    return urls[0]

#print service_archiveis('http://thejeshgn.com')



if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store', dest='url', help='Provide the path of sitemap url')
    options.add_argument('-o', '--output', action='store', dest='out', default='out.txt', help='Where you would like to save the results')
    options.add_argument('-s', '--service', action='store', dest='service', default='archiveis', help='What service do you like to use')
    options.add_argument('-c', '--cmd', action='store', dest='cmd', default=False, help='Do you want to run as cmd?')
    
    title = "Archive IT"
    url = None
    out = 'out.txt'
    service = None
    bufsize = 0
    args = options.parse_args()
    if args.cmd == True:
        url = args.url
        out = args.out
        service = args.service
    else:
        while 1:
            msg = "Please enter the URL path for sitemap?"
            url = enterbox(msg,title, "https://thejeshgn.com/sitemap.xml")
            if url != None:
                break

        choices = ["archiveis","archiveorg"]
        service = choicebox("What archive service do you like to use?",title, choices=choices)
        out = filesavebox("Create a file to save the log ", title)
        debug_message = "Running for the sitemap="+str(url)+"\n"+"On the service="+str(service)+"\n"+"Log file to see the out puts:"+str(out)
        print debug_message
        codebox("Settings", "Settings", debug_message) 

    sitemaps = getListOfSubSiteMaps(url)

    for sitemap_url in sitemaps:
        print "Starting for >"+str(sitemap_url)
        urls = parse_sitemap(sitemap_url)
        print urls
        if not urls:
            print 'There was an error in reading sitemap!'


        with open(out, 'a', bufsize) as output:
            for u in urls:
                time.sleep(.5) 
                if service == 'archiveis':
                    archive_url = service_archiveis(u[0])
                elif service == 'archiveorg':
                    archive_url = service_archiveorg(u[0])
                else:
                    print "Please select a service to archive."
                line = u[0]+','+archive_url+'\n'
                print line
                output.write(line)
    print "Archived "+str(len(urls))+" number of URLs with "+str(service)        

