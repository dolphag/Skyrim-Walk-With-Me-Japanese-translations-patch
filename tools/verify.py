import json,struct,pefile,collections,importlib.util,sys
from capstone import *
from capstone.x86 import *
orig=open('wwm/SKSE/Plugins/Wayfarer.dll','rb').read()
new=open('out/Wayfarer.dll','rb').read()
pe=pefile.PE('out/Wayfarer.dll'); pe0=pefile.PE('wwm/SKSE/Plugins/Wayfarer.dll')
IB=pe.OPTIONAL_HEADER.ImageBase
print('sections:',[s.Name.rstrip(b'\0').decode() for s in pe.sections])
print('SizeOfImage',hex(pe.OPTIONAL_HEADER.SizeOfImage),'file',len(new))
# 1) diff coverage
ch=json.load(open('changes.json'))
allowed=set()
for fo,ln,_ in ch: allowed.update(range(fo,fo+ln))
diff=[i for i in range(len(orig)) if orig[i]!=new[i]]
bad=[i for i in diff if i not in allowed]
print('changed bytes in original range:',len(diff),'outside logged changes:',len(bad))
# 2) decode every patched lea
tx=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
jp=[s for s in pe.sections if s.Name.startswith(b'.jpn')][0]
def cstr(va):
    o=jp.PointerToRawData+va-jp.VirtualAddress
    return new[o:new.index(b'\0',o)].decode('utf8')
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
n=0; out=[]
for fo,ln,d in ch:
    if d.startswith('lea@'):
        a=int(d[4:],16)
        ins=next(md.disasm(new[tx.PointerToRawData+a-tx.VirtualAddress:][:15],IB+a))
        assert ins.mnemonic=='lea'
        m=[o for o in ins.operands if o.type==X86_OP_MEM][0]
        tgt=a+ins.size+m.mem.disp
        assert jp.VirtualAddress<=tgt<jp.VirtualAddress+jp.Misc_VirtualSize
        out.append((a,cstr(tgt))); n+=1
print('decoded patched leas:',n)
# 3) pointer slots
for fo,ln,d in ch:
    if d.startswith('slot@'):
        v=struct.unpack_from('<Q',new,fo)[0]-IB
        print(d,cstr(v))
# 4) all-strings validity: valid utf8, no stray % beyond original specs
import re
bad=[]
spec=importlib.util.spec_from_file_location('trans','tools/trans_ja.py'); tr=importlib.util.module_from_spec(spec); spec.loader.exec_module(tr)
for en,ja in tr.T.items():
    if re.findall(r'%[^%\s]',en)!=re.findall(r'%[^%\s]',ja): bad.append(('pct',en[:40]))
    if '{' in ja or '}' in ja: bad.append(('brace',ja[:30]))
print('format-spec mismatches:',bad)
# 5) duplicate JP values from different EN keys
c=collections.defaultdict(list)
for en,ja in tr.T.items(): c[ja].append(en)
print('dup JP:',{k:v for k,v in c.items() if len(v)>1})
# 6) combos
for fo,ln,d in ch[:0]: pass
