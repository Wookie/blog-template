from datetime import datetime
import os.path
import email.utils
import time
import copy
import codecs
import urllib

### BLOG POST DATE CONVERSION

def hook_preconvert_date_conversion():
    posts = [p for p in pages if "post" in p] # get all blog post pages
    for p in posts:
        if "date" in p and p["date"] != "1970-01-01":
            # convert 2013-08-08 into August 8, 2013 
            p["printdate"] = datetime.strptime(p["date"], "%Y-%m-%d").strftime("%B %e, %Y")
        else:
            p["printdate"] = "DRAFT"

### INDEX GENERATION

def hook_preconvert_index():
    posts = [p for p in pages if "post" in p] # get all blog post pages
    posts.sort(key=lambda p: p.date, reverse=True)

    # create a virtual page containing the source of the first blog post
    ip = Page("index.md", virtual=posts[0].source)

    # copy over the attributes
    for attr in posts[0]:
        if not ip.has_key(attr):
            ip[attr] = posts[0][attr]

    # fix up the title
    ip["title"] = "LPo"

    # append the copy to the list of pages
    pages.append(ip)

### SITEMAP GENERATION

_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
"""

_SITEMAP_URL = """
<url>
    <loc>%s/%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>%s</changefreq>
    <priority>%s</priority>
</url>
"""

def hook_preconvert_sitemap():
    """Generate Google sitemap.xml file."""
    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    urls = []
    for p in pages:
        urls.append(_SITEMAP_URL % (options.base_url.rstrip('/'), urllib.quote(p.url), date,
                    p.get("changefreq", "monthly"), p.get("priority", "0.8")))
    fname = os.path.join(options.project, "output", "sitemap.xml")
    fp = open(fname, 'w')
    fp.write(_SITEMAP % "".join(urls))
    fp.close()

### RSS FEED GENERATION

_RSS = """<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>%s</title>
<link>%s</link>
<description>%s</description>
<language>en-us</language>
<pubDate>%s</pubDate>
<lastBuildDate>%s</lastBuildDate>
<docs>http://blogs.law.harvard.edu/tech/rss</docs>
<generator>Poole</generator>
%s
</channel>
</rss>
"""

_RSS_ITEM = """
<item>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <pubDate>%s</pubDate>
    <guid>%s</guid>
</item>
"""

def hook_postconvert_rss():
    items = []
    posts = [p for p in pages if "post" in p and p.title != "LPo"] # get all blog post pages
    posts.sort(key=lambda p: p.date, reverse=True)
    for p in posts:
        title = p.post
        link = "%s/%s" % (options.base_url.rstrip("/"), urllib.quote(p.url))
        desc = p.get("description", "")
        date = time.mktime(time.strptime("%s 12" % p.date, "%Y-%m-%d %H"))
        date = email.utils.formatdate(date)
        items.append(_RSS_ITEM % (title, link, desc, date, link))

    items = "".join(items)

    # --- CHANGE THIS --- #
    title = "LPo"
    link = "%s/" % options.base_url.rstrip("/")
    desc = "Mostly about hacking Mozilla B2G."
    date = email.utils.formatdate()

    rss = _RSS % (title, link, desc, date, date, items)

    fp = open(os.path.join(output, "rss.xml"), 'w')
    fp.write(rss)
    fp.close()

### GITHUB GISTS

def gist(gist_id):
    return '<script src="https://gist.github.com/dhuseby/%s.js"></script>' % gist_id


