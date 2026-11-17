import json,os,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL") or exit(1)
V=(0,100,320,330,500,900,0)
T=["::::::::DDDDDDDD<<>@@><<;;<??<;;:::>>:::;98::89;;<<66<<;::::::::","0244442026::::624:<==<:44;=>>=;44:=>>=:44;<==<;426:;;:6202444420","688888868::::::88:;<<;:88;;<<;;88:<<<<:88<<<<<<88;::::;868888886",":"*64,":"*64,":"*64]
KN=(31,33,14,18,-31,-33,-14,-18)
BD=(15,17,-15,-17);RD=(1,16,-1,-16)
B=[0]*128;W=True;C=0;N=0;MS=[];BM=None;TT=[0]*65536
class Ab(Exception):pass
def post(p,b):
 r=u.Request(U+p,data=json.dumps(b).encode())
 with u.urlopen(r) as x:return json.load(x)
def atk(s,w):
 for D,a in (((-15,-17) if w else (15,17),1),(KN,2),(BD+RD,6)):
  for d in D:
   t=s+d
   if not t&136 and B[t]==a*(2*w-1):return 1
 for d in BD+RD:
  t=s+d
  while not t&136:
   q=B[t]
   if q:
    if (q>0)==w and (abs(q)==5 or abs(q)==(4,3)[abs(d) in (15,17)]):return 1
    break
   t+=d
 return 0
def ap(s,o,k):
 q=B[o]
 if q and (q<0)==W or not q and not k:MS.append(s|o<<7)
def gen(k):
 global MS,TM
 MS=[];TM=TT[hash(tuple(B))&65535]
 for s in range(128):
  if s&136:continue
  p=B[s]
  if not p or (p<0)==W:continue
  t=abs(p)
  if t==1:
   d=32*W-16;R=7*W
   o=s+d
   if not k and not B[o]:
    if (o>>4)==R:MS.append(s|o<<7|5<<14)
    else:
     MS.append(s|o<<7)
     if (s>>4)==(1,6)[not W] and not B[o+d]:MS.append(s|(o+d)<<7)
   for o in (s+d-1,s+d+1):
    if o&136:continue
    q=B[o]
    if q and (q<0)==W:
     if (o>>4)==R:MS.append(s|o<<7|5<<14)
     else:MS.append(s|o<<7)
  elif t in (2,6):
   for d in (KN,BD+RD)[t==6]:
    o=s+d
    if not o&136:ap(s,o,k)
   if t==6 and not k and s==(116,4)[W]:
    o=(112,0)[W]
    for to,rf,bi,mi,ex in ((6,7,1,5,-1),(2,0,2,3,1)):
     if C&(bi*(4,1)[W]) and B[o+rf]==(-4,4)[W] and not B[o+mi] and not B[o+to] and (ex<0 or not B[o+ex]) and not (atk(o+4,not W) or atk(o+mi,not W) or atk(o+to,not W)):MS.append(s|(o+to)<<7|(8,4)[to==6]<<17)
  else:
   for d in (BD,RD,BD+RD)[t-3]:
    o=s+d
    while not o&136:
     if B[o]:ap(s,o,k);break
     if not k:MS.append(s|o<<7)
     o+=d
 MS.sort(key=sco,reverse=True)
 return MS
def make(m):
 global W,C
 u=(B[:],C)
 f=m&127;t=m>>7&127;pr=m>>14&7;fl=m>>17
 p=B[f]
 B[t]=(pr if pr else abs(p))*(2*W-1)
 B[f]=0
 if fl&12:
  r=t+1-3*(t&7!=6);g=t-1+2*(t&7!=6);B[g]=B[r];B[r]=0
 for q,n in ((4,3),(7,1),(0,2),(116,12),(119,4),(112,8)):
  if f==q or t==q:C&=~n
 W=not W
 return u
def unmake(u):
 global W,C
 B[:]=u[0];C=u[1];W=not W
def ev():
 s=0
 for q,p in enumerate(B):
  if p and not q&136:
   a=abs(p);r=q>>4;f=q&7
   i=(r^7*(p>0))*8+f
   v=V[a]+(ord(T[a-1][i])-58)*5
   s+=v if p>0 else -v
 return s*(2*W-1)
def sco(m):
 f=m&127;t=m>>7&127
 c=B[t]
 v=10*V[abs(c)]-abs(B[f]) if c else 0
 return v+(900 if m>>14&7 else 0)+(99999 if m==TM else 0)
def sr(d,a,be,y):
 global N,BM,W
 N+=1
 if N>120000:raise Ab
 if d<=0:
  s=ev()
  if s>=be:return be
  if s>a:a=s
 if d>2 and not atk(B.index(6 if W else -6),not W):
  W=not W
  v=-sr(d-3,-be,-be+1,1)
  W=not W
  if v>=be:return be
 ms=gen(d<=0)
 leg=0
 for m in ms:
  u=make(m)
  if atk(B.index(-6 if W else 6),W):unmake(u);continue
  leg+=1
  try:v=-sr(d-1,-be,-a,y+1)
  except Ab:unmake(u);raise
  unmake(u)
  if v>=be:TT[hash(tuple(B))&65535]=m;return be
  if v>a:
   a=v
   if not y:BM=m
 if d>0 and not leg:return -100000+d if atk(B.index(6 if W else -6),not W) else 0
 return a
def parse(f):
 global B,W,C
 B=[0]*128;q=112;z=f.split();W=z[1]=="w";C=sum(1<<j for j in range(4) if "KQkq"[j] in z[2])
 for ch in z[0]:
  if ch=="/":q-=24
  elif ch.isdigit():q+=int(ch)
  else:
   v="PNBRQK".index(ch.upper())+1
   B[q]=v*(2*ch.isupper()-1);q+=1
def uci(m):
 f=m&127;t=m>>7&127;p=m>>14&7
 return f"{chr(97+(f&7))}{(f>>4)+1}{chr(97+(t&7))}{(t>>4)+1}"+(" pnbrqk"[p] if p else "")
def choose(legal):
 global N,BM
 N=0;BM=None
 for d in range(1,64):
  o=BM
  try:sr(d,-100000,100000,0)
  except Ab:BM=o;break
 u=uci(BM) if BM else legal[0]
 return u if u in legal else legal[0]
while (g:=post("/game",{}))["status"]!="done":
 while g["status"]=="your_move":
  parse(g["fen"])
  g=post("/move",{"game":g["game"],"move":choose(g["legal_moves"])})
