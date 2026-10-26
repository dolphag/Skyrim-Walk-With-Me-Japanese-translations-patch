# -*- coding: utf-8 -*-
# 設定メニュー(ImGui)を描く関数の中から、.rdata の ASCII 文字列を参照する箇所(lea)を洗い出し、tier1.json に書く。
# build_patch.py が、この表にある参照だけを付け替える(ログや設定キーなど、メニュー外の同じ文字列には触れない)。
# 使い方(リポジトリのルートから): python3 -I tools/tier1.py [元DLL] [出力JSON]
#
# T1 は「メニューを描く関数」の先頭アドレス。版ごとに違うので、新しい版では
# 翻訳済みの長い文(例: "Nearby recruited followers appear here...")を参照する関数を探して置き換える。
import sys, json, struct, re, bisect, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_JUMP
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP

path = sys.argv[1] if len(sys.argv) > 1 else 'wwm/SKSE/Plugins/Wayfarer.dll'
out = sys.argv[2] if len(sys.argv) > 2 else 'tier1.json'

# Walk With Me 0.3.1 (SHA-256 8b8d398a...3c40)
# (0.3.0 では 0xc9ee0 0xccc30 0xcdd30 0xce390 0xcf9b0 0xd0910 0xbb750 0xd3430 0xd34f4 0xd36c7 0xd40d0 0xd4e70 0xd56a0 0xf6ea0。0xf6ea0 に相当する 0x1061d0 は設定ファイル(INI)の読み込みで、文字列を置き換えると INI のキーが壊れるため含めない)
T1 = [0xbc1e0, 0xcaa00, 0xcd750, 0xce850, 0xceeb0, 0xd04d0, 0xd1430,
      0xd3f60, 0xd4024, 0xd41f7, 0xd4c00, 0xd59a0, 0xd61d0]

pe = pefile.PE(path)
data = open(path, 'rb').read()
IB = pe.OPTIONAL_HEADER.ImageBase
S = lambda n: [s for s in pe.sections if s.Name.startswith(n)][0]
tx, rd, pd = S(b'.text'), S(b'.rdata'), S(b'.pdata')
rdb = data[rd.PointerToRawData:rd.PointerToRawData + rd.SizeOfRawData]
# .rdata 内の「直前が NUL、直後が NUL」の ASCII 文字列
strs = {rd.VirtualAddress + m.start(): m.group().decode()
        for m in re.finditer(rb'(?<=\x00)[\x20-\x7e]+(?=\x00)', rdb)}
pdata = data[pd.PointerToRawData:pd.PointerToRawData + pd.Misc_VirtualSize]
fs = sorted(struct.unpack_from('<II', pdata, i) for i in range(0, len(pdata) - 11, 12))
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

units = collections.OrderedDict()
for b, e in fs:
    if b not in T1: continue
    off = tx.PointerToRawData + b - tx.VirtualAddress
    ins_list = list(md.disasm(data[off:off + e - b], IB + b))
    for k, ins in enumerate(ins_list):
        a = ins.address - IB
        for o in ins.operands:
            if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
                t = a + ins.size + o.mem.disp
                if t not in strs: continue
                s = strs[t]
                u = units.setdefault(t, dict(va=t, s=s, sites=[], inline=[]))
                if ins.mnemonic != 'lea':
                    u['inline'].append((a, ins.mnemonic)); continue
                # 長さ即値(string_view など)を直後に持つか
                sized = None
                for nx in ins_list[k + 1:k + 8]:
                    if nx.mnemonic == 'mov' and len(nx.operands) == 2 and nx.operands[1].type == X86_OP_IMM \
                            and nx.operands[0].type == X86_OP_REG and nx.operands[1].imm in (len(s), len(s) + 1) \
                            and nx.operands[1].imm >= 3:
                        sized = (nx.address - IB, nx.size, nx.op_str)
                u['sites'].append(dict(addr=a, size=ins.size, dispoff=ins.disp_offset, sized=sized))
json.dump(list(units.values()), open(out, 'w'))
print(len(units), 'units,', sum(len(u['sites']) for u in units.values()), 'lea sites')
for u in units.values():
    flag = ('INLINE ' if u['inline'] else '') + ('SIZED ' if any(x['sized'] for x in u['sites']) else '')
    if flag: print('%x\t%d\t%s\t%s' % (u['va'], len(u['sites']), flag, u['s'][:70]))
