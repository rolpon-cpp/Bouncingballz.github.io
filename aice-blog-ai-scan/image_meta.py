# This code was written by Claude (AI-generated). Scans image metadata for AI-generation markers (C2PA, generator tags, SynthID-style labels) and builds contact sheets.
import os,sys,re,json
from PIL import Image, ExifTags
d=os.path.dirname(os.path.abspath(__file__))
KEYS=[b'c2pa',b'jumb',b'openai',b'dall',b'midjourney',b'stable diffusion',b'firefly',b'gemini',b'imagen',b'trainedAlgorithmicMedia',b'Made with Google AI',b'chatgpt',b'sora',b'flux',b'comfyui',b'parameters',b'canva',b'blender',b'photoshop',b'gimp',b'Screenshot',b'grok',b'ideogram',b'leonardo']
rows=[]
for f in sorted(os.listdir(d+'/images')):
    p=d+'/images/'+f; raw=open(p,'rb').read(); low=raw.lower()
    hits=[k.decode() for k in KEYS if k.lower() in low]
    try:
        im=Image.open(p); info={k:(str(v)[:80]) for k,v in im.info.items() if k not in('icc_profile','exif','xmp','photoshop')}
        ex={ExifTags.TAGS.get(k,k):str(v)[:60] for k,v in (im.getexif() or {}).items()}
        size=im.size
    except Exception as e: info={'err':str(e)};ex={};size=None
    rows.append(dict(file=f,size=size,bytes=len(raw),marker_hits=hits,info=info,exif=ex))
    print(f,size,hits,{k:v for k,v in ex.items() if k in('Make','Model','Software','DateTime','ImageDescription','Artist')},{k:v for k,v in info.items() if k not in('dpi','jfif','jfif_version','jfif_unit','jfif_density','progressive','progression','gamma','srgb','chromaticity')})
json.dump(rows,open(d+'/data/image_metadata.json','w'),indent=1)
# contact sheets
os.makedirs(d+'/sheets',exist_ok=True)
fs=sorted(os.listdir(d+'/images'))
from PIL import ImageDraw
for s in range(0,len(fs),6):
    sheet=Image.new('RGB',(1500,1040),'white'); dr=ImageDraw.Draw(sheet)
    for j,f in enumerate(fs[s:s+6]):
        try: im=Image.open(d+'/images/'+f).convert('RGB')
        except Exception as e: continue
        im.thumbnail((490,490)); x=(j%3)*500+5; y=(j//3)*520+5
        sheet.paste(im,(x,y)); dr.text((x,y+495),f[:70],fill='black')
    sheet.save(f"{d}/sheets/sheet_{s//6+1:02d}.jpg",quality=85)
