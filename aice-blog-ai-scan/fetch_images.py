# This code was written by Claude (AI-generated). Downloads every image used in the blog posts, politely (rate-limit aware).
import json,re,os,subprocess,time
d=os.path.dirname(os.path.abspath(__file__))
posts=json.load(open(d+'/data/posts_p1.json')); posts.sort(key=lambda p:p['date'])
missing=0
for i,p in enumerate(posts,1):
    for src in re.findall(r'<img[^>]+src="([^"]+)"',p['content']['rendered']):
        full=re.sub(r'-\d+x\d+(?=\.\w+$)','',src)
        fn=f"{d}/images/p{i:02d}_{os.path.basename(full)}"
        if os.path.exists(fn) and os.path.getsize(fn)>0: continue
        ok=False
        for url in (full,src):
            for attempt in range(4):
                r=subprocess.run(['curl','-sS','-f','-o',fn,url],capture_output=True)
                if r.returncode==0: ok=True;break
                if b'429' in r.stderr: time.sleep(8*(attempt+1))
                else: break
            if ok: break
        if not ok:
            missing+=1; print('FAILED',fn)
            if os.path.exists(fn): os.remove(fn)
        time.sleep(1.5)
print('missing',missing, 'have',len(os.listdir(d+'/images')))
