# -*- coding: utf-8 -*-
import sys, json, struct, importlib.util, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

SRC, OUT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('trans', 'tools/trans_ja.py')
tr = importlib.util.module_from_spec(spec); spec.loader.exec_module(tr)

raw = open(SRC, 'rb').read()
data = bytearray(raw)
pe = pefile.PE(SRC)
IB = pe.OPTIONAL_HEADER.ImageBase
FA = pe.OPTIONAL_HEADER.FileAlignment
SA = pe.OPTIONAL_HEADER.SectionAlignment
secs = pe.sections
last = secs[-1]
assert len(raw) == last.PointerToRawData + last.SizeOfRawData, 'overlay/signature present'
tx = [s for s in secs if s.Name.startswith(b'.text')][0]
rd = [s for s in secs if s.Name.startswith(b'.rdata')][0]

def al(v, a): return (v + a - 1) // a * a
new_va = al(last.VirtualAddress + last.Misc_VirtualSize, SA)
new_raw = last.PointerToRawData + last.SizeOfRawData

def rd_off(va): return rd.PointerToRawData + va - rd.VirtualAddress
def tx_off(va): return tx.PointerToRawData + va - tx.VirtualAddress
def cstr_at(va):
    o = rd_off(va); return bytes(raw[o:raw.index(b'\0', o)])

pool = bytearray()
cache = {}
def add(b):
    if b in cache: return cache[b]
    off = len(pool); pool.extend(b); cache[b] = off; return off

md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
tier1 = json.load(open('tier1.json'))
changes = []   # (file_offset, length, description)
log = []

def patch_lea(site, old_va, new_str_off):
    a = site['addr']
    ins = next(md.disasm(raw[tx_off(a):tx_off(a)+15], IB + a))
    assert ins.mnemonic == 'lea', (hex(a), ins.mnemonic)
    mem = [o for o in ins.operands if o.type == X86_OP_MEM][0]
    assert mem.mem.base == X86_REG_RIP
    tgt = a + ins.size + mem.mem.disp
    assert tgt == old_va, (hex(a), hex(tgt), hex(old_va))
    assert ins.disp_offset == site['dispoff']
    nva = new_va + new_str_off
    disp = nva - (a + ins.size)
    assert -2**31 <= disp < 2**31
    fo = tx_off(a) + ins.disp_offset
    data[fo:fo+4] = struct.pack('<i', disp)
    changes.append((fo, 4, 'lea@%x' % a))

# 1) 通常の文字列（Tier1関数内のlea参照のみ付け替え）
used = set(); n_sites = 0
byS = {u['s']: u for u in tier1}
units_by_s = collections.defaultdict(list)
for u in tier1: units_by_s[u['s']].append(u)
for en, ja in tr.T.items():
    us = units_by_s.get(en)
    if not us: continue
    for u in us:
        if not u['sites']: continue
        off = add(ja.encode('utf-8') + b'\0')
        for s in u['sites']:
            patch_lea(s, u['va'], off); n_sites += 1
        used.add(en)
missing = [k for k in tr.T if k not in used]
# 2) コンボ（\0区切り連結）
combo_done = 0
for items, jitems in tr.COMBOS.items():
    blob = b'\0'.join(i.encode() for i in items) + b'\0\0'
    # 原文がrdataに連続して存在することを確認
    o = bytes(raw[rd.PointerToRawData:rd.PointerToRawData+rd.SizeOfRawData]).find(blob)
    assert o >= 0, items
    va0 = rd.VirtualAddress + o
    cands = [u for u in tier1 if u['va'] == va0 and u['sites']]
    assert cands, ('no site for combo', items)
    off = add(b'\0'.join(i.encode('utf-8') for i in jitems) + b'\0\0')
    for u in cands:
        for s in u['sites']: patch_lea(s, u['va'], off); n_sites += 1
    combo_done += 1
# 3) ポインタ表スロット
reloc_rvas = set()
for blk in pe.DIRECTORY_ENTRY_BASERELOC:
    for e in blk.entries:
        if e.type: reloc_rvas.add(e.rva)
def patch_slot(slot, en, ja):
    fo = rd_off(slot)
    v = struct.unpack_from('<Q', raw, fo)[0]
    assert IB <= v < IB + 0x400000, hex(slot)
    assert cstr_at(v - IB) == en.encode(), (hex(slot), cstr_at(v - IB), en)
    assert slot in reloc_rvas, 'slot not relocated %x' % slot
    off = add(ja.encode('utf-8') + b'\0')
    data[fo:fo+8] = struct.pack('<Q', IB + new_va + off)
    changes.append((fo, 8, 'slot@%x' % slot))
for slot, en, ja in tr.SLOTS + tr.DESC_SLOTS: patch_slot(slot, en, ja)
for i, (en, ja) in enumerate(tr.EMBLEMS.items()):
    patch_slot(0x214068 + 16 * i, en, ja)

# 3b) ホイールの命令説明(関数内leaを直接付け替え)
for a, en, ja in tr.WHEEL_LEA + tr.ACTION_LEA:
    ins = next(md.disasm(raw[tx_off(a):tx_off(a)+15], IB + a))
    assert ins.mnemonic == 'lea' and ins.size == 7 and ins.disp_offset == 3, hex(a)  # lea r64,[rip+disp32]
    mem = [o for o in ins.operands if o.type == X86_OP_MEM][0]
    assert mem.mem.base == X86_REG_RIP
    old_va = a + ins.size + mem.mem.disp
    assert cstr_at(old_va) == en.encode(), (hex(a), cstr_at(old_va))
    patch_lea({'addr': a, 'dispoff': 3}, old_va, add(ja.encode('utf-8') + b'\0')); n_sites += 1

# 3c) Party Actions: 下部の説明(ポインタ表)
for slot, en, ja in tr.HINT_SLOTS: patch_slot(slot, en, ja)

# 3d) インライン文字列コピーを std::string(const char*, n) コンストラクタ(0x6000)呼び出しに置換
CTOR = 0x6000
assert bytes(raw[tx_off(CTOR):tx_off(CTOR)+5]) == bytes.fromhex('48896c2410'), 'ctor prologue'
pdsec = [s for s in secs if s.Name.startswith(b'.pdata')][0]
funcs = [struct.unpack_from('<III', raw, pdsec.PointerToRawData + i)[:2] for i in range(0, pdsec.Misc_VirtualSize, 12)]
from capstone import CS_GRP_JUMP
def patch_inline(rs, re_, dest, en, ja):
    f = [x for x in funcs if x[0] <= rs < x[1]][0]
    assert re_ <= f[1]
    ins = list(md.disasm(raw[tx_off(f[0]):tx_off(f[1])], IB + f[0]))
    st = {i.address - IB: i for i in ins}
    assert rs in st and re_ in st, (hex(rs), hex(re_))
    # 領域の途中へ飛んでくる分岐が無いこと
    for i in ins:
        if i.group(CS_GRP_JUMP) and i.operands and i.operands[0].type == 2:  # X86_OP_IMM
            t = i.operands[0].imm - IB
            assert not (rs < t < re_), ('branch into region', hex(i.address - IB), hex(t))
    nx = st[re_]
    assert nx.mnemonic == 'lea' and nx.op_str == 'rax, [rbp + 0x%x]' % dest, (hex(re_), nx.op_str)
    refs = []
    for i in ins:
        a = i.address - IB
        if rs <= a < re_:
            for o in i.operands:
                if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP:
                    t = a + i.size + o.mem.disp
                    if rd.VirtualAddress <= t < rd.VirtualAddress + rd.Misc_VirtualSize: refs.append(t)
    assert any(cstr_at(t) == en.encode() for t in refs), ('english not found', hex(rs))
    jb = ja.encode('utf-8')
    off = add(jb + b'\0')
    c = b'\x48\x8d\x8d' + struct.pack('<i', dest)                       # lea rcx,[rbp+dest]
    c += b'\x48\x8d\x15' + struct.pack('<i', new_va + off - (rs + len(c) + 7))  # lea rdx,[rip+ja]
    c += b'\x41\xb8' + struct.pack('<I', len(jb))                       # mov r8d,len
    c += b'\xe8' + struct.pack('<i', CTOR - (rs + len(c) + 5))          # call ctor
    assert len(c) <= re_ - rs, (hex(rs), len(c), re_ - rs)
    c += b'\x90' * (re_ - rs - len(c))
    fo = tx_off(rs); data[fo:fo + len(c)] = c
    changes.append((fo, len(c), 'inline@%x' % rs))
for rs, re_, dest, en, ja in tr.INLINE: patch_inline(rs, re_, dest, en, ja)

# 3e) fmt 書式 (ポインタ+長さ)
for la, ia, en, ja in tr.FMT_SITES:
    ins = next(md.disasm(raw[tx_off(la):tx_off(la)+15], IB + la))
    assert ins.mnemonic == 'lea' and ins.size == 7
    mem = [o for o in ins.operands if o.type == X86_OP_MEM][0]
    old_va = la + 7 + mem.mem.disp
    assert cstr_at(old_va) == en.encode()
    jb = ja.encode('utf-8')
    patch_lea({'addr': la, 'dispoff': 3}, old_va, add(jb + b'\0')); n_sites += 1
    fo = tx_off(ia) + 7
    assert bytes(raw[tx_off(ia):tx_off(ia)+7]) == bytes.fromhex('48c785a8080000') and struct.unpack_from('<I', raw, fo)[0] == len(en)
    data[fo:fo+4] = struct.pack('<I', len(jb)); changes.append((fo, 4, 'fmtlen@%x' % ia))

# 3f) 定数の付け替え (movss xmm,[rip+disp])
for a, oldv, newv in tr.CONST_SITES:
    ins = next(md.disasm(raw[tx_off(a):tx_off(a)+15], IB + a))
    assert ins.mnemonic in ('movss', 'mulss'), hex(a)
    mem = [o for o in ins.operands if o.type == X86_OP_MEM][0]
    assert mem.mem.base == X86_REG_RIP
    tgt = a + ins.size + mem.mem.disp
    cur = struct.unpack_from('<f', raw, rd_off(tgt))[0]
    assert abs(cur - oldv) < 1e-4, (hex(a), cur)
    off = add(struct.pack('<f', newv))
    fo = tx_off(a) + ins.disp_offset
    data[fo:fo+4] = struct.pack('<i', new_va + off - (a + ins.size)); changes.append((fo, 4, 'cst@%x' % a))

# 4) 新セクション追加
assert len(pool) > 0
raw_size = al(len(pool), FA)
vsize = len(pool)
e_lfanew = struct.unpack_from('<I', raw, 0x3c)[0]
nsec = struct.unpack_from('<H', raw, e_lfanew + 6)[0]
optsz = struct.unpack_from('<H', raw, e_lfanew + 20)[0]
sec_tab = e_lfanew + 24 + optsz
hdr_end = sec_tab + 40 * nsec
first_raw = min(s.PointerToRawData for s in secs)
assert hdr_end + 40 <= first_raw, 'no room for section header'
assert bytes(raw[hdr_end:hdr_end+40]) == b'\0' * 40
sh = struct.pack('<8sIIIIIIHHI', b'.jpn\0\0\0\0', vsize, new_va, raw_size, new_raw, 0, 0, 0, 0, 0x40000040)
data[hdr_end:hdr_end+40] = sh
struct.pack_into('<H', data, e_lfanew + 6, nsec + 1)
opt = e_lfanew + 24
old_soi = struct.unpack_from('<I', raw, opt + 56)[0]
struct.pack_into('<I', data, opt + 56, al(new_va + vsize, SA))                  # SizeOfImage
sid = struct.unpack_from('<I', raw, opt + 8)[0]
struct.pack_into('<I', data, opt + 8, sid + raw_size)                           # SizeOfInitializedData
struct.pack_into('<I', data, opt + 64, 0)                                       # CheckSum
changes += [(hdr_end, 40, 'secthdr'), (e_lfanew + 6, 2, 'nsec'), (opt + 56, 4, 'soi'), (opt + 8, 4, 'sid'), (opt + 64, 4, 'chk')]
data += pool + b'\0' * (raw_size - len(pool))
open(OUT, 'wb').write(data)
print('sites patched:', n_sites, 'combos:', combo_done, 'pool bytes:', len(pool), 'new_va: %x' % new_va)
print('translations without a Tier1 site (not applied):', len(missing))
for m in missing: print('  -', m[:80])
json.dump(changes, open('changes.json', 'w'))
