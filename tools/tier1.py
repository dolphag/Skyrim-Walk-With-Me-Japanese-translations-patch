import json,struct,re,collections,pefile,bisect
from capstone import *
from capstone.x86 import *
path='wwm/SKSE/Plugins/Wayfarer.dll'
data=open(path,'rb').read(); pe=pefile.PE(path); IB=pe.OPTIONAL_HEADER.ImageBase
tx=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
pd=[s for s in pe.sections if s.Name.startswith(b'.pdata')][0]
pdata=data[pd.PointerToRawData:pd.PointerToRawData+pd.Misc_VirtualSize]
fs=sorted((struct.unpack_from('<II',pdata,i)) for i in range(0,len(pdata)-11,12))
begins=[f[0] for f in fs]
def func_of(va):
    i=bisect.bisect_right(begins,va)-1
    if i>=0 and fs[i][0]<=va<fs[i][1]: return fs[i]
T1=[0xc9aa0,0xcc7f0,0xcd8f0,0xcdf50,0xcf570,0xd04d0,0xbb280,0xd2fd0,0xd3094,0xd3267,0xd3c70,0xd4a10,0xd5240,0xf6970]
xr={int(k):v for k,v in json.load(open('xrefs.json')).items()}
S=json.load(open('all_strings.json'))['strings']
sv={va:s for va,s in S}
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
def toff(va): return tx.PointerToRawData+va-tx.VirtualAddress
units=collections.OrderedDict()
for tgt,refs in sorted(xr.items()):
    if tgt not in sv: continue
    s=sv[tgt]
    if not re.fullmatch(r"[\x20-\x7e]+",s): continue
    for r in refs:
        f=func_of(r[0])
        if f and f[0] in T1:
            u=units.setdefault(tgt,dict(va=tgt,s=s,sites=[],inline=[]))
            if r[1]=='lea':
                # sized detection
                o=toff(r[0]); n=0; sized=None
                for ins in md.disasm(data[o:o+90],IB+r[0]):
                    n+=1
                    if n==1: continue
                    if n>9: break
                    if ins.mnemonic in('mov',) and len(ins.operands)==2 and ins.operands[1].type==X86_OP_IMM and ins.operands[0].type==X86_OP_REG:
                        if ins.operands[1].imm in (len(s),len(s)+1) and ins.operands[1].imm>=3:
                            sized=(ins.address-IB,ins.size,ins.op_str)
                u['sites'].append(dict(addr=r[0],size=r[2],dispoff=r[3],sized=sized))
            else:
                u['inline'].append((r[0],r[1]))
json.dump(list(units.values()),open('tier1.json','w'))
print(len(units))
for u in units.values():
    flag=('INLINE ' if u['inline'] else '')+('SIZED ' if any(x['sized'] for x in u['sites']) else '')
    print(f"{u['va']:x}\t{len(u['sites'])}\t{flag}\t{u['s']}")
