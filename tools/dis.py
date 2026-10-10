import sys,re,struct,pefile
from capstone import *
f=sys.argv[1]; addr=int(sys.argv[2],16); maxn=int(sys.argv[3]) if len(sys.argv)>3 else 400
pe=pefile.PE(f); IB=pe.OPTIONAL_HEADER.ImageBase
d=open(f,'rb').read()
S=lambda n:[s for s in pe.sections if s.Name.startswith(n)][0]
tx,rd,pd=S(b'.text'),S(b'.rdata'),S(b'.pdata')
fs=[struct.unpack_from('<III',d,pd.PointerToRawData+i)[:2] for i in range(0,pd.Misc_VirtualSize,12)]
F=[x for x in fs if x[0]<=addr<x[1]][0]
print('func %x-%x'%F)
md=Cs(CS_ARCH_X86,CS_MODE_64)
def cs(va):
    for s in pe.sections:
        if s.VirtualAddress<=va<s.VirtualAddress+s.Misc_VirtualSize:
            o=s.PointerToRawData+va-s.VirtualAddress
            try:
                z=d[o:d.index(b'\0',o)][:60]
                return z.decode('utf8') if z and all(c>=32 or c>127 for c in z) else ''
            except: return ''
    return ''
off=tx.PointerToRawData+F[0]-tx.VirtualAddress
n=0
for ins in md.disasm(d[off:off+F[1]-F[0]],IB+F[0]):
    s=''
    m=re.search(r'rip ([+-]) (0x[0-9a-f]+)',ins.op_str)
    if m:
        t=ins.address+ins.size+int(m.group(2),16)*(1 if m.group(1)=='+' else -1)-IB
        s='  ; %x %s'%(t,cs(t))
    print('%x: %s %s%s'%(ins.address-IB,ins.mnemonic,ins.op_str,s)); n+=1
    if n>maxn: break
