import sys,struct,pefile
from capstone import *
f=sys.argv[1]; lo=int(sys.argv[2],16); hi=int(sys.argv[3],16)
pe=pefile.PE(f); IB=pe.OPTIONAL_HEADER.ImageBase; d=open(f,'rb').read()
S=lambda n:[s for s in pe.sections if s.Name.startswith(n)][0]
tx,pd=S(b'.text'),S(b'.pdata')
fs=[struct.unpack_from('<III',d,pd.PointerToRawData+i)[:2] for i in range(0,pd.Misc_VirtualSize,12)]
F=[x for x in fs if x[0]<=lo<x[1]][0]
md=Cs(CS_ARCH_X86,CS_MODE_64)
off=tx.PointerToRawData+F[0]-tx.VirtualAddress
for i in md.disasm(d[off:off+F[1]-F[0]],IB+F[0]):
    a=i.address-IB
    if lo<=a<=hi: print('%x [%2d] %-44s %s'%(a,i.size,i.mnemonic+' '+i.op_str,i.bytes.hex()))
