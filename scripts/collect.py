#!/usr/bin/env python3
"""Fetch RSS/Atom metadata for a free, static, link-only Ethiopian economy news index.
No keys, no scraping of linked article pages, no external dependencies.
"""
import calendar
import datetime as dt
import email.utils
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FEEDS = BASE / 'feeds.json'
OUT = BASE / 'site' / 'news.json'
MAX_FEED_BYTES = 2_000_000
MAX_ITEMS = 180
TIMEOUT = 16
UTC = dt.timezone.utc

PATTERNS = {
    'Trade & Exports': r'export|import|trade|customs|tariff|coffee|gold|sesame|commodit|trade deficit',
    'Banking & Finance': r'bank|finance|financial|currency|foreign exchange|forex|birr|interest rate|inflation|bond|debt|credit|loan|monetary|insurance',
    'Investment & Business': r'invest|business|entrepreneur|company|companies|market|private sector|startup|revenue|profit|merger|acquisition|investment',
    'Agriculture': r'agricult|farm|crop|fertili|livestock|coffee|grain|wheat|food security|irrigation',
    'Gold & Mining': r'mining|minerals?|gold|\bore\b|exploration|extractive',
    'Manufacturing': r'manufactur|factory|factories|industrial|textile|garment|assembly',
    'Energy & Infrastructure': r'energy|electric|power|dam|hydro|solar|road|rail|infrastructur|construction|logistics|\bport\b|airport|airline|aviation|telecom',
    'Policy & Economy': r'econom|gdp|growth|tax|budget|policy|reform|regulat|minister|development|fiscal|central bank|employment|jobs|housing',
}
ECONOMY = re.compile('|'.join(f'(?:{p})' for p in PATTERNS.values()),re.I)
ETHIOPIA = re.compile(r'ethiop|addis|birr|abiy|oromia|amhara|tigray|hawassa|dire dawa|djibouti corridor|ethio telecom|nbe\b',re.I)
STRIP_TAGS = re.compile(r'<[^>]*>')

def clean(s):
    return re.sub(r'\s+', ' ', STRIP_TAGS.sub(' ', s or '')).strip()

def parse_date(s):
    if not s: return None
    try:
        d=email.utils.parsedate_to_datetime(s)
        if d:
            if d.tzinfo is None: d=d.replace(tzinfo=UTC)
            return d.astimezone(UTC).isoformat().replace('+00:00','Z')
    except (TypeError, ValueError, OverflowError): pass
    try:
        d=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
        if d.tzinfo is None:d=d.replace(tzinfo=UTC)
        return d.astimezone(UTC).isoformat().replace('+00:00','Z')
    except (TypeError, ValueError): return None

def normalize_url(u):
    try:
        p=urllib.parse.urlparse(u.strip())
        if p.scheme not in ('http','https') or not p.netloc: return None
        query=urllib.parse.parse_qsl(p.query, keep_blank_values=False)
        query=[(k,v) for k,v in query if not (k.lower().startswith('utm_') or k.lower() in ('fbclid','gclid'))]
        return urllib.parse.urlunparse((p.scheme,p.netloc.lower(),p.path or '/', '', urllib.parse.urlencode(query), ''))
    except Exception:return None

def text(n, tag):
    e=n.find(tag)
    return ''.join(e.itertext()).strip() if e is not None else ''

def extract(xml, source):
    root=ET.fromstring(xml)
    found=[]
    if root.tag.endswith('rss') or root.find('channel') is not None:
        entries=root.findall('./channel/item')
        for n in entries:
            found.append((text(n,'title'),text(n,'link'),text(n,'pubDate') or text(n,'{http://purl.org/dc/elements/1.1/}date')))
    else:
        ns='{http://www.w3.org/2005/Atom}'
        for n in root.findall(f'.//{ns}entry'):
            link=''
            for el in n.findall(f'{ns}link'):
                if el.attrib.get('rel','alternate')=='alternate':link=el.attrib.get('href','');break
            found.append((text(n,f'{ns}title'),link,text(n,f'{ns}published') or text(n,f'{ns}updated')))
    out=[]
    now=dt.datetime.now(UTC)
    for title,url,date in found:
        title=clean(title)[:240]
        url=normalize_url(url)
        published=parse_date(date)
        if not (title and url and published):continue
        when=dt.datetime.fromisoformat(published.replace('Z','+00:00'))
        if when>now+dt.timedelta(hours=6) or when<now-dt.timedelta(days=75):continue
        if not ECONOMY.search(title):continue
        if not source.get('ethiopiaFocused',False) and not ETHIOPIA.search(title):continue
        categories=[category for category, pattern in PATTERNS.items() if re.search(pattern,title,re.I)]
        out.append({
            'id': hashlib.sha256(url.encode()).hexdigest()[:18],
            'title':title,'url':url,'publisher':source['name'],
            'publishedAt':published,'categories':categories[:3] or ['Policy & Economy']
        })
    return out

def fetch(source):
    req=urllib.request.Request(source['url'],headers={
        'User-Agent':'EthiopiaEconomicAtlasNews/1.0 (public link-only RSS reader; contact via project repository)',
        'Accept':'application/rss+xml,application/atom+xml,application/xml,text/xml;q=0.8',
    })
    with urllib.request.urlopen(req,timeout=TIMEOUT) as response:
        if int(response.headers.get('Content-Length','0') or 0)>MAX_FEED_BYTES:raise ValueError('feed too large')
        raw=response.read(MAX_FEED_BYTES+1)
        if len(raw)>MAX_FEED_BYTES:raise ValueError('feed too large')
        return raw

def main():
    sources=json.loads(FEEDS.read_text())
    previous={}
    if OUT.exists():
        try:previous=json.loads(OUT.read_text())
        except ValueError:pass
    articles={a['url']:a for a in previous.get('articles',[]) if a.get('url')}
    good=0
    failures=[]
    for source in sources:
        if not source.get('enabled'):continue
        try:
            entries=extract(fetch(source),source)
            print(source['name'],len(entries),'accepted headlines')
            for a in entries:articles[a['url']]=a
            good+=1
        except (urllib.error.URLError,TimeoutError,ValueError,ET.ParseError,OSError) as ex:
            failures.append(f"{source['name']}: {str(ex)[:140]}")
    now=dt.datetime.now(UTC)
    cleaned=[]
    for a in articles.values():
        try:
            when=dt.datetime.fromisoformat(a['publishedAt'].replace('Z','+00:00'))
            if now-dt.timedelta(days=75)<=when<=now+dt.timedelta(hours=6):cleaned.append(a)
        except (ValueError,KeyError):continue
    cleaned.sort(key=lambda a:a['publishedAt'],reverse=True)
    # Only claim a successful update when at least one feed returns successfully.
    updated=now.isoformat(timespec='seconds').replace('+00:00','Z') if good else previous.get('lastSuccessfulCollection')
    obj={
        'edition':'Ethiopia Economic Atlas News Monitor',
        'lastSuccessfulCollection':updated,
        'items':len(cleaned[:MAX_ITEMS]),
        'workingSources':good,
        'configuredSources':sum(1 for s in sources if s.get('enabled')),
        'articles':cleaned[:MAX_ITEMS],
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    if failures:print('Feed notices:',*failures,sep='\n - ',file=sys.stderr)
    if not good:print('No successful feeds; retained existing headlines.',file=sys.stderr)
    return 0

if __name__=='__main__':sys.exit(main())
