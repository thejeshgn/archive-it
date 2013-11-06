archive-it
==========

Archive your blog using archive.org's wayback machine. 



#Logic

#### 1. Read the url_of_sitemap, time_delay in seconds, delta/full from command prompt

```

example
$python archive.py http://thejeshgn.com/sitemap.xml 1 delta

```

#### 2. Read sitemap.xls from the url, get urls one by one


#### 3. If delta check if the URL is available on wayback machine

```
example:

wget http://archive.org/wayback/available?url=http://thejeshgn.com/2013/11/01/i-will-set-heaven-on-fire/

if it returns 

{"archived_snapshots":{}}

then no snapshots available, so run the save
```

#### 4. If no snapsot available or full run then save the page

```
example

wget http://web.archive.org/save/http://thejeshgn.com/2013/11/01/i-will-set-heaven-on-fire/

```

#### 5. Return stats




