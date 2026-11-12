# This code was written by Claude (AI-generated).
# Scans each blog post for AI-writing signals using:
#  1) GPT-2 perplexity + burstiness (the approach GPTZero-style detectors are built on)
#  2) Two open RoBERTa AI-text classifiers
#  3) Stylometric "tells" (em dashes, AI-favoured vocabulary, stock phrases) vs human signals (typos, slips)
import os,re,json,math,sys,statistics as st
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM,AutoModelForSequenceClassification
d=os.path.dirname(os.path.abspath(__file__))
torch.set_grad_enabled(False)
gt=AutoTokenizer.from_pretrained('gpt2'); gm=AutoModelForCausalLM.from_pretrained('gpt2').eval()
def ppl(text):
    ids=gt(text,return_tensors='pt',truncation=True,max_length=1024).input_ids
    if ids.shape[1]<5: return None
    return math.exp(gm(ids,labels=ids).loss.item())
CLFS={}
for name in ['openai-community/roberta-base-openai-detector','fakespot-ai/roberta-base-ai-text-detection-v1','Hello-SimpleAI/chatgpt-detector-roberta']:
    try:
        t=AutoTokenizer.from_pretrained(name); m=AutoModelForSequenceClassification.from_pretrained(name).eval()
        lab={v.lower():k for k,v in m.config.id2label.items()}
        ai=[k for v,k in lab.items() if v in('fake','ai','chatgpt','label_1','machine','generated')]
        CLFS[name]=(t,m,ai[0] if ai else 1); print('loaded',name,m.config.id2label,file=sys.stderr)
    except Exception as e: print('skip',name,str(e)[:100],file=sys.stderr)
def clf(text):
    out={}
    for n,(t,m,ai) in CLFS.items():
        x=t(text,return_tensors='pt',truncation=True,max_length=512)
        out[n.split('/')[0]]=torch.softmax(m(**x).logits,-1)[0,ai].item()
    return out
AIWORDS=r"\b(delve|tapestry|testament|crucial|pivotal|seamless(ly)?|foster(s|ing)?|leverag(e|es|ing)|underscore(s|d)?|moreover|furthermore|additionally|ultimately|in conclusion|notably|vibrant|landscape|realm|multifaceted|nuanced|intricate|comprehensive|robust|elevate(s|d)?|resonate(s|d)?|compelling|invaluable|embark|journey|navigate|harness|showcas(e|es|ing)|meticulous(ly)?|captivat(e|ing)|enhanc(e|es|ed|ing)|plays? a (crucial|key|vital|significant) role|it'?s worth noting|not (just|only|merely))\b"
HUMAN=r"(\bi\. e\.|\bits’ |\bit’s (bold|audience)|\ba (audience|eye|in-depth|informational|overall)\b|\b(\w+) \2\b| & |vs\.?|\bwhilst\b|\ba lot\b|\breally\b|\bvery\b|\bstuff\b|\bcool\b)"
def sents(t): return [s for s in re.split(r'(?<=[.!?])\s+',t) if len(s.split())>=3]
def analyse(name,text):
    paras=[p.strip() for p in text.split('\n') if len(p.split())>=35]
    words=len(text.split())
    rows=[]
    for p in paras:
        r=dict(words=len(p.split()),ppl=ppl(p),**clf(p),text=p[:160]); rows.append(r)
    W=sum(r['words'] for r in rows) or 1
    agg={k:sum(r[k]*r['words'] for r in rows)/W for k in (rows[0].keys() if rows else []) if k not in('words','text')}
    ss=sents(' '.join(paras)); sp=[x for x in (ppl(s) for s in ss) if x]
    sl=[len(s.split()) for s in ss]
    return dict(post=name,words=words,scored_words=W if rows else 0,**{k:round(v,3) for k,v in agg.items()},
        burstiness_ppl_sd=round(st.pstdev(sp),1) if len(sp)>1 else None,
        sent_len_mean=round(st.mean(sl),1) if sl else None, sent_len_sd=round(st.pstdev(sl),1) if len(sl)>1 else None,
        em_dashes=text.count('—'), semicolons=text.count(';'),
        ai_vocab_per_1k=round(1000*len(re.findall(AIWORDS,text,re.I))/max(words,1),1),
        human_markers_per_1k=round(1000*len(re.findall(HUMAN,text,re.I))/max(words,1),1),
        paragraphs=rows)
res=[]
for f in sorted(os.listdir(d+'/posts')):
    raw=open(d+'/posts/'+f).read()
    body=raw.split('\n\n',1)[1].split('--- IMAGES ---')[0]
    res.append(analyse(f[:2],body)); print(f[:2],{k:v for k,v in res[-1].items() if k!='paragraphs'},flush=True)
base=analyse('AI_BASELINE',open(d+'/calibration/ai_baseline.txt').read()); res.append(base)
print('BASE',{k:v for k,v in base.items() if k!='paragraphs'})
json.dump(res,open(d+'/data/text_scan_results.json','w'),indent=1)
