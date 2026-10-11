# -*- coding: utf-8 -*-
"""fwm_patch.py の出力検証: 原版/パッチ版DLLと翻訳表だけから独立に確認する。
使い方: python3 -I fwm_verify.py <原版DLL> <パッチ版DLL>"""
import sys, os, struct, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import *
from fwm_trans1 import T1
from fwm_trans2 import T2
T = {**T1, **T2}
O, N = sys.argv[1:3]
a, b = open(O, 'rb').read(), open(N, 'rb').read()
pe = pefile.PE(N); IB = pe.OPTIONAL_HEADER.ImageBase
S = {s.Name.rstrip(b'\0').decode(): s for s in pe.sections}
j, tx = S['.jpn'], S['.text']
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
ok = True
def fail(*m):
    global ok; ok = False; print('NG', *m)
jb = b[j.PointerToRawData:j.PointerToRawData + j.Misc_VirtualSize]
ja2en = collections.defaultdict(list)
for en, ja in T.items(): ja2en[ja.encode()].append(en)
code = b[tx.PointerToRawData:tx.PointerToRawData + tx.Misc_VirtualSize]
ins = []; p = 0
while p < len(code):
    got = False
    for x in md.disasm(code[p:], IB + tx.VirtualAddress + p):
        ins.append(x); p = x.address - IB - tx.VirtualAddress + x.size; got = True
    if not got or p < len(code) and not got: p += 1
    elif p < len(code): p += 1
cnt = 0
for k, x in enumerate(ins):
    if x.mnemonic != 'lea' or x.size != 7: continue
    op = [o for o in x.operands if o.type == X86_OP_MEM]
    if not op or op[0].mem.base != X86_REG_RIP: continue
    t = x.address + 7 + op[0].mem.disp - IB
    if not (j.VirtualAddress <= t < j.VirtualAddress + len(jb)): continue
    o = t - j.VirtualAddress; e = jb.index(b'\0', o); s = jb[o:e]
    cnt += 1
    if s not in ja2en: fail('未知の.jpn文字列', hex(x.address - IB)); continue
    try: s.decode('utf-8')
    except Exception: fail('UTF-8不正', hex(x.address - IB))
    L, Lold = len(s), {len(en.encode()) for en in ja2en[s]}
    near = []
    for y in ins[max(0, k - 4):k + 9]:
        if y.mnemonic == 'mov' and len(y.operands) == 2 and y.operands[1].type == X86_OP_IMM and len(y.bytes) >= 5:
            near.append(y.operands[1].imm)
    if (Lold - {L}) & set(near):
        # 旧長さが近傍に残っている: 別用途の同値かもしれないので報告
        print('? 旧長さ即値が近傍に残存', hex(x.address - IB), s.decode()[:20], sorted(Lold), L)
print('.jpn参照lea:', cnt)
# 全ポインタスロット: .jpn を指す
sl = 0
for s in (S['.rdata'], S['.data']):
    d = b[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
    for o in range(0, len(d) - 7, 8):
        v = struct.unpack_from('<Q', d, o)[0] - IB
        if j.VirtualAddress <= v < j.VirtualAddress + len(jb):
            sl += 1
            e = jb.index(b'\0', v - j.VirtualAddress); s_ = jb[v - j.VirtualAddress:e]
            n = struct.unpack_from('<Q', d, o + 8)[0] if o + 16 <= len(d) else None
            if n is not None and n < 4096 and n != len(s_) and n in {len(en.encode()) for en in ja2en.get(s_, [])}:
                fail('スロット長が旧値', hex(s.VirtualAddress + o))
print('.jpn参照スロット:', sl)
# 再配置: スロットが再配置対象か
reloc = {e.rva for blk in pe.DIRECTORY_ENTRY_BASERELOC for e in blk.entries if e.type}
for s in (S['.rdata'], S['.data']):
    d = b[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
    for o in range(0, len(d) - 7, 8):
        v = struct.unpack_from('<Q', d, o)[0] - IB
        if j.VirtualAddress <= v < j.VirtualAddress + len(jb) and (s.VirtualAddress + o) not in reloc:
            fail('再配置なしのスロット', hex(s.VirtualAddress + o))
# 全訳語が.jpnに存在するか
miss = [en for en, ja in T.items() if ja.encode() + b'\0' not in jb]
print('翻訳表に対し.jpnに無い語:', len(miss), miss[:5])
print('結果:', 'OK' if ok else 'NG')
