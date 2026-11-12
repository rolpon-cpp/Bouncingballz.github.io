# This code was written by Claude (AI-generated). Extracts blog posts from WordPress JSON into plain text.
import json, re, html, sys, os
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.imgs=[]; s.links=[]; s.skip=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in('script','style'): s.skip+=1
        if t=='img': s.imgs.append((a.get('src',''),a.get('alt','')))
        if t=='a': s.links.append(a.get('href',''))
        if t=='iframe': s.links.append('IFRAME '+a.get('src',''))
        if t in('p','h1','h2','h3','h4','li','br','figcaption','blockquote','tr'): s.out.append('\n')
        if t in('h1','h2','h3','h4'): s.out.append('## ')
        if t=='li': s.out.append('- ')
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
        if t in('p','h1','h2','h3','h4','li','figcaption'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
d=os.path.dirname(os.path.abspath(__file__))
posts=json.load(open(d+'/data/posts_p1.json'))
posts.sort(key=lambda p:p['date'])
os.makedirs(d+'/posts',exist_ok=True)
idx=[]
for i,p in enumerate(posts,1):
    h=P(); h.feed(p['content']['rendered'])
    txt=re.sub(r'\n\s*\n+','\n\n',''.join(h.out)).strip()
    title=html.unescape(p['title']['rendered'])
    fn=f"{i:02d}_{p['slug'][:50]}.txt"
    with open(d+'/posts/'+fn,'w') as f:
        f.write(f"TITLE: {title}\nDATE: {p['date']}\nMODIFIED: {p['modified']}\nURL: {p['link']}\n\n{txt}\n\n--- IMAGES ---\n"+'\n'.join(f"{s} | alt={a}" for s,a in h.imgs)+"\n--- LINKS ---\n"+'\n'.join(h.links)+'\n')
    idx.append((fn,p['date'],len(txt.split()),len(h.imgs),len(h.links)))
for r in idx: print(*r)
