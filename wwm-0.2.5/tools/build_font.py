# 合成フォント: 元Cinzel Decorative(英数) + Noto Sans JP サブセット(かな・訳文の漢字)
import importlib.util,sys
from fontTools.ttLib import TTFont
from fontTools import subset, merge
spec=importlib.util.spec_from_file_location('t','tools/trans_ja.py'); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
strs=list(t.T.values())+[x for v in t.COMBOS.values() for x in v]+list(t.EMBLEMS.values())
for lst in (t.SLOTS,t.DESC_SLOTS,t.WHEEL_LEA,t.ACTION_LEA,t.HINT_SLOTS): strs+=[j for _,_,j in lst]
strs+=[e[4] for e in t.INLINE]+[e[3] for e in t.FMT_SITES]
chars={ord(c) for s in strs for c in s if ord(c)>=0x80}
chars|=set(range(0x3000,0x3100))|set(range(0xff01,0xff5f))|{0x2026,0x2015,0x2018,0x2019,0x201c,0x201d,0x00b7}
noto=sys.argv[1]; cinzel=sys.argv[2]; out=sys.argv[3]
f=TTFont(noto); cm=f.getBestCmap(); chars={c for c in chars if c in cm}
opt=subset.Options(); opt.layout_features=[]; opt.drop_tables+=['GSUB','GPOS','GDEF','BASE','STAT','vhea','vmtx','DSIG','FFTM','prep','gasp']
opt.notdef_outline=True; opt.name_IDs=['*']; opt.hinting=False; opt.glyph_names=False
s=subset.Subsetter(opt); s.populate(unicodes=sorted(chars)); s.subset(f); f.save('font/noto_sub.ttf')
m=merge.Merger(merge.Options(drop_tables=['DSIG','FFTM'])).merge([cinzel,'font/noto_sub.ttf']); m.save(out)
g=TTFont(out); b=TTFont(cinzel); nm=g['name']
for tb,attrs in (('hhea',['ascent','descent','lineGap']),('OS/2',['sTypoAscender','sTypoDescender','sTypoLineGap','usWinAscent','usWinDescent'])):
    for a in attrs: setattr(g[tb],a,getattr(b[tb],a))
for n in list(nm.names):
    if n.nameID in (16,17,18,21,22,25): nm.removeNames(nameID=n.nameID)
fam='Walk With Me Inscription JP'
for pid,eid,lid in ((3,1,0x409),(1,0,0)):
    nm.setName(fam,1,pid,eid,lid); nm.setName('Regular',2,pid,eid,lid); nm.setName('WalkWithMeInscriptionJP-1.0',3,pid,eid,lid)
    nm.setName(fam,4,pid,eid,lid); nm.setName('WalkWithMeInscriptionJP',6,pid,eid,lid)
for n in nm.names:
    if n.nameID==0: n.string=n.toUnicode()+"; includes a subset of Noto Sans JP (c) 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'."
g['OS/2'].usWeightClass=700; g['head'].macStyle=0; g['OS/2'].fsSelection=(g['OS/2'].fsSelection & ~0x21)|0x40
g.save(out)
g=TTFont(out); bc,gc=b.getBestCmap(),g.getBestCmap()
assert all(b['hmtx'][bc[k]]==g['hmtx'][gc[k]] for k in bc)
assert all((b['glyf'][bc[k]].coordinates if b['glyf'][bc[k]].numberOfContours>0 else None)==(g['glyf'][gc[k]].coordinates if g['glyf'][gc[k]].numberOfContours>0 else None) for k in bc)
print('chars',len(chars),'cmap',len(gc),'metrics',g['hhea'].ascent,g['hhea'].descent)
