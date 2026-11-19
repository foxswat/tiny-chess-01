# tiny-chess-01 engine, v30 (K_END).
# Endgame king table (K_END) replaces the middlegame king PST once the
# queens are off; search is alpha-beta with quiescence, null-move pruning,
# a 64K transposition table, and a 110k-node budget per move.
# v39 (tuned): VN 335, rook PST x0.85 (coord sweep, 3k screening)
# v41 (budget): 110k-node budget — in-process trial-0 2.5/6, Elo 1191,
# clears the 1154 floor; 120k also cleared but timed out in the real
# trial (per-move limit under load), 110k is the fastest floor-clearing
# rung. 100k gave no gain (2.0/6).
# v37 (speed fix): 80k-node budget (was 150k) so avg move time is
# <=3s and a full trial finishes well inside the 1800s wall; post() now
# has a 10s timeout + 3 tries, falling back to re-polling /game so one
# hung connection cannot eat the whole trial.
import json, os, urllib.request as u
U = os.getenv("MAKEFUN_ENV_URL")
V = (0, 100, 335, 330, 500, 900, 0)
SC = (1, 1, 1, 0.85, 1, 1)
T = [
 "::::::::DDDDDDDD<<>@@><<;;<??<;;:::>>:::;98::89;;<<66<<;::::::::",
 "0244442026::::624:<==<:44;=>>=;44:=>>=:44;<==<;426:;;:6202444420",
 "688888868::::::88:;<<;:88;;<<;;88:<<<<:88<<<<<<88;::::;868888886",
 ":"*8+";<<<<<<;"+"9::::::9"*5+":::;;:::",
 (Q:="68888886")+(S:="8::::::8")+("8:;;;;:8")*4+S+Q,
 "42200224"*4+"64422446"+"86666668"+">>::::>>"+">@<::<@>",
]
E = [(V[abs(p)] + (ord(T[abs(p)-1][((q >> 4) ^ 7*(p > 0))*8 + (q & 7)]) - 58)*5*SC[abs(p)-1])
     * ((p > 0)*2 - 1) * (p != 0)
     for p in range(-6, 7) for q in range(128)]
KN = (31, 33, 14, 18, -31, -33, -14, -18)
BD = (15, 17, -15, -17)
RD = (1, 16, -1, -16)
TT = [0]*65536
class Ab(Exception):
    pass
def post(p, b):
    for _ in range(3):
        try:
            return json.load(u.urlopen(u.Request(U + p, data=json.dumps(b).encode()), timeout=10))
        except Exception:
            pass
    return post("/game", {}) if p != "/game" else {"status": "done"}
def atk(s, w):
    """Is square s attacked by side w (True=White)?"""
    for D, a in (((-15, -17) if w else (15, 17), 1), (KN, 2), (BD + RD, 6)):
        for d in D:
            t = s + d
            if not t & 136 and B[t] == a*(2*w - 1):
                return 1
    for d in BD + RD:
        t = s + d
        while not t & 136:
            q = B[t]
            if q:
                if (q > 0) == w and abs(q) in (5, 3 + (abs(d) in (1, 16))):
                    return 1
                break
            t += d
    return 0
def ap(s, o, k):
    """Append move s->o if capture, or if quiet and not captures-only (k)."""
    q = B[o]
    if q and (q < 0) == W or not q and not k:
        MS.append(s | o << 7)
def gen(k):
    """Generate moves; k=True means captures only (quiescence). Sorted by sco."""
    global MS, TM
    MS = []
    TM = TT[hash(tuple(B)) & 65535]
    for s in range(128):
        if s & 136:
            continue
        p = B[s]
        if not p or (p < 0) == W:
            continue
        t = abs(p)
        if t == 1:
            d = 32*W - 16
            R = 7*W
            o = s + d
            if not k and not B[o]:
                if (o >> 4) == R:
                    MS.append(s | o << 7 | 5 << 14)
                else:
                    MS.append(s | o << 7)
                    if (s >> 4) == 6 - 5*W and not B[o + d]:
                        MS.append(s | (o + d) << 7)
            for o in (s + d - 1, s + d + 1):
                if o & 136:
                    continue
                q = B[o]
                if q and (q < 0) == W:
                    if (o >> 4) == R:
                        MS.append(s | o << 7 | 5 << 14)
                    else:
                        MS.append(s | o << 7)
        elif t in (2, 6):
            for d in (KN, BD + RD)[t == 6]:
                o = s + d
                if not o & 136:
                    ap(s, o, k)
            if t == 6 and not k and s == (116, 4)[W]:
                o = (112, 0)[W]
                for to, rf, bi, mi, ex in ((6, 7, 1, 5, -1), (2, 0, 2, 3, 1)):
                    if (C & (bi*(4, 1)[W]) and B[o + rf] == (-4, 4)[W]
                            and not B[o + mi] and not B[o + to]
                            and (ex < 0 or not B[o + ex])
                            and not any(atk(o + x, not W) for x in (4, mi, to))):
                        MS.append(s | (o + to) << 7 | (8, 4)[to == 6] << 17)
        else:
            for d in (BD, RD, BD + RD)[t - 3]:
                o = s + d
                while not o & 136:
                    if B[o]:
                        ap(s, o, k)
                        break
                    if not k:
                        MS.append(s | o << 7)
                    o += d
    MS.sort(key=sco, reverse=1)
    return MS
def make(m):
    global W, C, S, KD, NQ
    u = (B[:], C, S, KD, NQ)
    f = m & 127
    t = m >> 7 & 127
    pr = m >> 14 & 7
    fl = m >> 17
    p = B[f]
    c = B[t]
    z = (pr or abs(p)) * (2*W - 1)
    if abs(p) == 6 and NQ == 0:
        d = ke(t, p) - ke(f, p)
    else:
        d = E[(z + 6)*128 + t] - E[(p + 6)*128 + f]
    if c:
        d -= E[(c + 6)*128 + t]
    if fl & 12:
        r = t - 2 + 3*(t & 7 == 6)
        g = t + 1 - 2*(t & 7 == 6)
        k = B[r]
        d += E[(k + 6)*128 + g] - E[(k + 6)*128 + r]
    # Update king adjustment before a last-queen capture switches tables.
    if abs(p) == 6:
        KD += (ke(t, p) - E[(p + 6)*128 + t]) - (ke(f, p) - E[(p + 6)*128 + f])
    if pr:
        if NQ == 0:
            d -= KD
        NQ += 1
    if abs(c) == 5:
        NQ -= 1
        if NQ == 0:
            d += KD
    S += d
    B[t] = z
    B[f] = 0
    if fl & 12:
        B[g] = B[r]
        B[r] = 0
    for q, n in ((4, 3), (7, 1), (0, 2), (116, 12), (119, 4), (112, 8)):
        if f == q or t == q:
            C &= ~n
    W = not W
    return u
def unmake(u):
    global W, C, S, KD, NQ
    B[:] = u[0]
    C, S, KD, NQ = u[1:]
    W = not W
def ke(q, p):
    return (70 - 10*(abs(2*(q & 7) - 7) + abs(2*(q >> 4) - 7))) * (1 if p > 0 else -1)
def ev():
    return S*(2*W - 1) + 10
def sco(m):
    f = m & 127
    t = m >> 7 & 127
    c = B[t]
    v = 10*V[abs(c)] - abs(B[f]) if c else 0
    return v + (900 if m >> 14 & 7 else 0) + (99999 if m == TM else 0)
def sr(d, a, be, y):
    global N, BM, W
    N += 1
    if N > 1.1e5:
        raise Ab
    if d <= 0:
        s = ev()
        if s >= be:
            return be
        if s > a:
            a = s
    if d > 2 and not atk(B.index(6*(2*W - 1)), not W):
        W = not W
        v = -sr(d - 3, -be, -be + 1, 1)
        W = not W
        if v >= be:
            return be
    ms = gen(d <= 0)
    leg = 0
    for m in ms:
        u = make(m)
        if atk(B.index(6*(1 - 2*W)), W):
            unmake(u)
            continue
        leg += 1
        try:
            v = -sr(d - 1, -be, -a, y + 1)
        except Ab:
            unmake(u)
            raise
        unmake(u)
        if v >= be:
            TT[hash(tuple(B)) & 65535] = m
            return be
        if v > a:
            a = v
            if not y:
                BM = m
    if d > 0 and not leg:
        return -100000 + d if atk(B.index(6*(2*W - 1)), not W) else 0
    return a
def parse(f):
    global B, W, C, S, KD, NQ
    B = [0]*128
    q = 112
    z = f.split()
    W = z[1] == "w"
    C = sum(1 << j for j in range(4) if "KQkq"[j] in z[2])
    for ch in z[0]:
        if ch == "/":
            q -= 24
        elif ch.isdigit():
            q += int(ch)
        else:
            v = "PNBRQK".index(ch.upper()) + 1
            B[q] = v*(2*ch.isupper() - 1)
            q += 1
    S = KD = NQ = 0
    for q, p in enumerate(B):
        S += E[(p + 6)*128 + q]
        if abs(p) == 6:
            KD += ke(q, p) - E[(p + 6)*128 + q]
        if abs(p) == 5:
            NQ += 1
    if NQ == 0:
        S += KD
def uci(m):
    f = m & 127
    t = m >> 7 & 127
    p = m >> 14 & 7
    return (chr(97 + (f & 7)) + str(f // 16 + 1) + chr(97 + (t & 7)) + str(t // 16 + 1)
            + (" pnbrqk"[p] if p else ""))
def choose(legal):
    global N, BM
    N = 0
    BM = None
    for d in range(64):
        o = BM
        try:
            sr(d, -1e5, 1e5, 0)
        except Ab:
            BM = o
            break
    u = uci(BM) if BM else legal[0]
    return u if u in legal else legal[0]
while (g:=post("/game",{}))["status"]!="done":
    while g["status"]=="your_move":
        parse(g["fen"])
        g=post("/move",{"game":g["game"],"move":choose(g["legal_moves"])})
