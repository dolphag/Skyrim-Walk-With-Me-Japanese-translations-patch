# -*- coding: utf-8 -*-
"""Fight With Me 0.1.0 (FightWithMe.dll) 日本語化パッチ生成。

使い方: python3 fwm_patch.py <原版FightWithMe.dll> <出力DLL> <レポートJSON>

方針 (WWM向けtools/build_patch.pyと同系統):
  1. 画面表示用の英語文字列を .jpn セクション(新設)の日本語文字列へ付け替える
       - lea reg,[rip+disp] の参照先を付け替え
       - 直後/直前の長さ即値(std::string_view / fmt書式)も同時に更新
       - ポインタ表(.rdata)のスロットと、隣接する長さ(string_view)を更新
       - コンパイラがその場で展開した std::string の組み立て領域は、
         std::string(const char*,size_t) 生成関数の呼び出しに置換 (レジスタ生存を検証)
  2. Label/LabelWidth は文字列を1バイトずつ描画するためUTF-8が壊れる。
       非ASCIIを含む場合のみ Text/TextSize へ振り分けるスタブを .text 末尾の空きに置く。
"""
import sys, os, json, struct, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import *
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fwm_trans1 import T1
from fwm_trans2 import T2
import fwm_cfg as C

SRC, OUT, REP = sys.argv[1:4]
T = {**T1, **T2}
raw = open(SRC, 'rb').read()
data = bytearray(raw)
pe = pefile.PE(SRC)
IB = pe.OPTIONAL_HEADER.ImageBase
FA = pe.OPTIONAL_HEADER.FileAlignment
SA = pe.OPTIONAL_HEADER.SectionAlignment
secs = pe.sections
last = secs[-1]
assert len(raw) == last.PointerToRawData + last.SizeOfRawData, 'overlay/signature present'
S = {s.Name.rstrip(b'\0').decode(): s for s in secs}
tx, rd, dt, pd = S['.text'], S['.rdata'], S['.data'], S['.pdata']
def al(v, a): return (v + a - 1) // a * a
new_va = al(last.VirtualAddress + last.Misc_VirtualSize, SA)
new_raw = last.PointerToRawData + last.SizeOfRawData
def sec_of(va):
    for s in secs:
        if s.VirtualAddress <= va < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData): return s
def off(va):
    s = sec_of(va); return s.PointerToRawData + va - s.VirtualAddress
def u32(o): return struct.unpack_from('<I', data, o)[0]

pool = bytearray(); cache = {}
def add(b):
    if b in cache: return cache[b]
    o = len(pool); pool.extend(b); cache[b] = o; return o
def jva(o): return new_va + o

changes = []     # (file_offset, length, label)
log = []         # 人が読むレポート
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

# ---- .rdata の文字列表 ---------------------------------------------------
rdraw = bytes(raw[rd.PointerToRawData:rd.PointerToRawData + rd.SizeOfRawData])
strs = {}; i = 0
while i < len(rdraw):
    j = rdraw.find(b'\0', i)
    if j < 0: break
    if j > i: strs[rd.VirtualAddress + i] = rdraw[i:j]
    i = j + 1
rev = collections.defaultdict(list)
for va, b in strs.items(): rev[b].append(va)

# ---- 関数(.pdata)と全命令 ----------------------------------------------
pdraw = raw[pd.PointerToRawData:pd.PointerToRawData + pd.Misc_VirtualSize]
funcs = sorted((b, e) for b, e, u in (struct.unpack_from('<III', pdraw, k) for k in range(0, len(pdraw) - 11, 12))
               if tx.VirtualAddress <= b < tx.VirtualAddress + tx.Misc_VirtualSize and e > b)
fins = {}   # func -> (insn list, addr->index)
def decode(f):
    if f not in fins:
        code = raw[off(f[0]):off(f[0]) + f[1] - f[0]]
        ins = list(md.disasm(code, IB + f[0]))
        fins[f] = (ins, {x.address - IB: k for k, x in enumerate(ins)})
    return fins[f]
import bisect
fbeg = [f[0] for f in funcs]
def func_of(a):
    k = bisect.bisect_right(fbeg, a) - 1
    if k >= 0 and funcs[k][0] <= a < funcs[k][1]: return funcs[k]
def ripref(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return x.address + x.size + op.mem.disp - IB
rd_lo, rd_hi = rd.VirtualAddress, rd.VirtualAddress + rd.Misc_VirtualSize

# rdata を指す全参照 (target -> [(addr, insn)])
refs = collections.defaultdict(list)
for f in funcs:
    for x in decode(f)[0]:
        t = ripref(x)
        if t is not None and rd_lo <= t < rd_hi: refs[t].append((x.address - IB, x, f))

# ---- 再配置 ---------------------------------------------------------------
reloc = set()
for blk in pe.DIRECTORY_ENTRY_BASERELOC:
    for e in blk.entries:
        if e.type: reloc.add(e.rva)

# ---- 長さ即値の検出 -------------------------------------------------------
REG32 = {X86_REG_EAX, X86_REG_ECX, X86_REG_EDX, X86_REG_R8D, X86_REG_R9D, X86_REG_R10D, X86_REG_R11D}
def imm32_form(x, L):
    """この命令が『長さLを32bit即値(命令末尾4バイト)で持つ mov』なら True"""
    if x.mnemonic != 'mov' or len(x.operands) != 2: return False
    d, s = x.operands
    if s.type != X86_OP_IMM or s.imm != L: return False
    if len(x.bytes) < 5 or int.from_bytes(x.bytes[-4:], 'little') != L: return False
    if d.type == X86_OP_MEM and d.size == 8 and d.mem.base != X86_REG_RIP: return True    # mov qword [m], imm32
    if d.type == X86_OP_REG and d.reg in REG32: return True                                # mov r32, imm32
    return False
def find_len(f, k, L):
    """lea(索引k)に対応する長さ即値を探す: 近傍の前方→後方。次のrdata参照leaの手前まで。"""
    ins, idx = decode(f)
    best = None
    for j in range(k + 1, min(len(ins), k + 9)):
        x = ins[j]
        if x.mnemonic in ('call', 'ret', 'jmp'): break
        t = ripref(x)
        if x.mnemonic == 'lea' and t is not None and rd_lo <= t < rd_hi and t in strs: break
        if imm32_form(x, L): best = (j - k, x); break
    if best is None and ins[k].op_str.startswith('rdx,'):      # std::string::append/assign(this, rdx=ptr, r8=len): 長さは先に設定される
        for j in range(k - 1, max(-1, k - 4), -1):
            x = ins[j]
            if x.mnemonic in ('call', 'ret', 'jmp'): break
            if imm32_form(x, L) and x.operands[0].type == X86_OP_REG and x.operands[0].reg == X86_REG_R8D:
                best = (j - k, x); break
    return best

# ---- 翻訳対象の VA を決める -----------------------------------------------
targets = []   # (en, ja, va)
for en, ja in T.items():
    if en in C.SKIP_KEYS: continue
    vas = rev.get(en.encode('utf-8'))
    if not vas:
        raise SystemExit('rdataに無いキー: %r' % en[:60])
    for va in vas: targets.append((en, ja, va))

claimed = {}          # 長さ即値アドレス -> lea アドレス
sites = []            # dict
slotsl = []
inline_sites = []
for en, ja, va in targets:
    L = len(en.encode()); JL = len(ja.encode('utf-8'))
    for a, x, f in refs.get(va, []):
        if (en, a) in C.SKIP_SITES: log.append(('skip-site', en, hex(a))); continue
        if x.mnemonic == 'lea' and x.size == 7 and x.disp_offset == 3:
            ins, idx = decode(f); k = idx[a]
            hit = find_len(f, k, L)
            rec = dict(kind='lea', en=en, ja=ja, va=va, addr=a, len_at=None)
            if hit:
                d, lx = hit; la = lx.address - IB
                assert la not in claimed, ('長さ即値の二重取り', hex(la), hex(a), hex(claimed[la]))
                claimed[la] = a; rec['len_at'] = la; rec['len_d'] = d
            elif '{' in en:
                raise SystemExit('書式文字列なのに長さ即値が無い: %r @%x' % (en[:40], a))
            sites.append(rec)
        else:
            inline_sites.append(dict(en=en, ja=ja, va=va, addr=a, mn=x.mnemonic))

# ---- ポインタ表スロット -----------------------------------------------------
want = {IB + va: (en, ja, va) for en, ja, va in targets}
slot_recs = []
for s in (rd, dt):
    base = s.PointerToRawData
    for o in range(0, s.SizeOfRawData - 7, 8):
        v = struct.unpack_from('<Q', raw, base + o)[0]
        if v in want:
            en, ja, va = want[v]
            rva = s.VirtualAddress + o
            assert rva in reloc, ('スロットに再配置が無い', hex(rva), en)
            nxt = struct.unpack_from('<Q', raw, base + o + 8)[0] if o + 16 <= s.SizeOfRawData else None
            slot_recs.append(dict(en=en, ja=ja, va=va, slot=rva, file=base + o, has_len=(nxt == len(en.encode()))))

print('lea sites:', len(sites), ' slots:', len(slot_recs), ' inline-candidates:', len(inline_sites))
json.dump(dict(inline=[{**i, 'addr': hex(i['addr'])} for i in inline_sites]), open(REP + '.pre', 'w'), ensure_ascii=False, indent=1)

# ---- 手動指定の長さ即値 ----------------------------------------------------
for en, la, lenaddr in C.MANUAL_LEN:
    r = next(s for s in sites if s['en'] == en and s['addr'] == la)
    assert r['len_at'] is None, ('手動指定が自動検出と二重', en)
    assert lenaddr not in claimed
    claimed[lenaddr] = la; r['len_at'] = lenaddr; r['len_d'] = 'manual'

# ---- lea 付け替え + 長さ即値 -------------------------------------------------
def patch_len_imm32(la, L, JL, label):
    o = off(la)
    ins = next(md.disasm(raw[o:o + 15], IB + la))
    assert imm32_form(ins, L), (hex(la), ins.op_str)
    fo = o + ins.size - 4
    assert u32(fo) == L
    data[fo:fo + 4] = struct.pack('<I', JL); changes.append((fo, 4, label + '@%x' % la))

n_lea = 0
for r in sites:
    a = r['addr']; en, ja = r['en'], r['ja']; JL = len(ja.encode('utf-8'))
    o = off(a); ins = next(md.disasm(raw[o:o + 15], IB + a))
    assert ins.mnemonic == 'lea' and ins.size == 7 and ins.disp_offset == 3
    tgt = a + 7 + [op for op in ins.operands if op.type == X86_OP_MEM][0].mem.disp
    assert tgt == r['va'] and strs[tgt] == en.encode('utf-8'), (hex(a), en)
    po = add(ja.encode('utf-8') + b'\0')
    disp = jva(po) - (a + 7)
    assert -2**31 <= disp < 2**31
    data[o + 3:o + 7] = struct.pack('<i', disp); changes.append((o + 3, 4, 'lea@%x' % a)); n_lea += 1
    if r.get('len_at'): patch_len_imm32(r['len_at'], len(en.encode()), JL, 'len')

for en, a, kind in C.EXTRA_LEN:
    ja = T[en]; L = len(en.encode()); JL = len(ja.encode('utf-8'))
    if kind == 'imm32':
        patch_len_imm32(a, L, JL, 'xlen')
    else:
        assert JL <= 127, ('8bit即値に収まらない', en, JL)
        o = off(a); ins = next(md.disasm(raw[o:o + 15], IB + a))
        pos = [i for i in range(ins.size) if raw[o + i] == L]
        assert len(pos) >= 1, (hex(a), ins.op_str)
        p = pos[-1] if ins.mnemonic == 'cmp' else pos[0]
        assert ins.mnemonic in ('cmp', 'lea', 'mov')
        data[o + p] = JL; changes.append((o + p, 1, 'xlen8@%x' % a))

# ---- ポインタ表スロット --------------------------------------------------------
n_slot = 0
for s in slot_recs:
    po = add(s['ja'].encode('utf-8') + b'\0')
    struct.pack_into('<Q', data, s['file'], IB + jva(po)); changes.append((s['file'], 8, 'slot@%x' % s['slot']))
    if s['has_len']:
        struct.pack_into('<Q', data, s['file'] + 8, len(s['ja'].encode('utf-8'))); changes.append((s['file'] + 8, 8, 'slotlen@%x' % s['slot']))
    n_slot += 1

# ---- インライン展開された std::string の組み立てを生成関数の呼び出しへ置換 --------
tx_slack_start = al(tx.Misc_VirtualSize, 16)                 # スタブ置き場(.text末尾の空き)
tx_end = tx.SizeOfRawData
stub_off = tx_slack_start                                    # .text 内オフセット
assert all(b == 0 for b in raw[tx.PointerToRawData + tx.Misc_VirtualSize:tx.PointerToRawData + tx_end]), '.text末尾が空きでない'
stub_buf = bytearray()
def stub_va(): return tx.VirtualAddress + stub_off + len(stub_buf)

REGS = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
def enc_lea_rcx(base, disp):
    b = REGS.index(base); rex = 0x48 | (1 if b >= 8 else 0)
    d8 = -128 <= disp <= 127
    code = bytes([rex, 0x8d, (0x40 if d8 else 0x80) | (1 << 3) | (b & 7)])
    if (b & 7) == 4: code += b'\x24'                          # SIB (rsp/r12)
    return code + (struct.pack('<b', disp) if d8 else struct.pack('<i', disp))

FAM = {}
for n, fam_ in {'rax': ['rax', 'eax', 'ax', 'al', 'ah'], 'rcx': ['rcx', 'ecx', 'cx', 'cl', 'ch'], 'rdx': ['rdx', 'edx', 'dx', 'dl', 'dh'],
                'r8': ['r8', 'r8d', 'r8w', 'r8b'], 'r9': ['r9', 'r9d', 'r9w', 'r9b'], 'r10': ['r10', 'r10d', 'r10w', 'r10b'], 'r11': ['r11', 'r11d', 'r11w', 'r11b']}.items():
    for q in fam_: FAM[q] = n
for i_ in range(6): FAM['xmm%d' % i_] = 'xmm%d' % i_
FAM['eflags'] = 'flags'
def rw(x):
    r, w = x.regs_access()
    f = lambda s: {FAM.get(md.reg_name(q)) for q in s} - {None}
    return f(r), f(w)
CLOB = {'rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11', 'xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4', 'xmm5', 'flags'}
def live_out(f, re_, regs):
    ins, idx = decode(f); res = {}
    for R in regs:
        seen = set(); stack = [idx[re_]]; steps = 0
        while stack and steps < 4000:
            i = stack.pop()
            if i in seen or i >= len(ins): continue
            seen.add(i); steps += 1
            x = ins[i]; r, w = rw(x)
            if x.mnemonic in ('xor', 'xorps', 'pxor') and len(x.operands) == 2 and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_REG and x.operands[0].reg == x.operands[1].reg:
                r = set()
            if R in r:
                res[R] = hex(x.address - IB) + ' ' + x.mnemonic + ' ' + x.op_str; break
            if R in w: continue
            if x.mnemonic == 'call': continue        # 呼び出しで揮発レジスタは破壊される (引数読み出しは保守的に無視しない→下で別扱い)
            if x.mnemonic in ('ret',): continue
            if x.mnemonic == 'jmp':
                if x.operands[0].type == X86_OP_IMM:
                    t = x.operands[0].imm - IB
                    if t in idx: stack.append(idx[t])
                    else: res[R] = 'jump out of function'; 
                continue
            if x.mnemonic.startswith('j') and x.operands[0].type == X86_OP_IMM:
                t = x.operands[0].imm - IB
                if t in idx: stack.append(idx[t])
            stack.append(i + 1)
    return res

def branch_targets(f):
    ins, idx = decode(f); T_ = set()
    for x in ins:
        if (x.mnemonic == 'jmp' or x.mnemonic.startswith('j')) and x.operands and x.operands[0].type == X86_OP_IMM:
            T_.add(x.operands[0].imm - IB)
    return T_

INL = []   # 結果
def sso_region(site):
    en, ja, va, a = site['en'], site['ja'], site['va'], site['addr']
    L = len(en.encode()); f = func_of(a); ins, idx = decode(f); k = idx[a]; bt = branch_targets(f)
    assert L <= 15, ('SSO以外', en)
    # 先頭ロード直後のストアから格納先ウィンドウを決める
    dest = None
    for j in range(k + 1, k + 4):
        x = ins[j]
        if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.base not in (0, X86_REG_RIP) and x.mnemonic in ('mov', 'movsd', 'movups', 'movdqu'):
            dest = (md.reg_name(x.operands[0].mem.base), x.operands[0].mem.disp); break
    assert dest, ('格納先不明', en, hex(a))
    base, d0 = dest
    def in_win(x):
        if not x.operands or x.operands[0].type != X86_OP_MEM: return False
        m = x.operands[0].mem
        return md.reg_name(m.base) == base and m.index == 0 and d0 <= m.disp < d0 + 0x20
    def is_strload(x):
        t = ripref(x)
        return t is not None and va <= t <= va + L and x.mnemonic in ('mov', 'movzx', 'movsd')
    # 後方へ
    rs_i = k; j = k - 1
    while j >= 0 and ins[j].address - IB not in bt:
        x = ins[j]
        if in_win(x) and x.mnemonic in ('movups', 'movdqu', 'mov'):
            rs_i = j
        elif x.mnemonic == 'movdqa' and ripref(x) is not None: pass
        elif x.mnemonic == 'xorps' and x.operands[0].reg == x.operands[1].reg: pass
        else: break
        j -= 1
    # 前方へ
    re_i = k; j = k
    while j < len(ins) and ins[j].address - IB not in (bt - {ins[k].address - IB} if j == k else bt):
        x = ins[j]
        if in_win(x) or is_strload(x): re_i = j
        elif j > k and x.mnemonic in ('lea', 'mov', 'jmp', 'or', 'movabs') or j > k: break
        j += 1
    # 領域内訳チェック
    rs = ins[rs_i].address - IB; re_ = ins[re_i + 1].address - IB
    assert not any(rs < t < re_ for t in bt), ('領域内へ分岐', en, hex(rs))
    wrote_xmm = set(); vec_xmm = {}
    for x in ins[rs_i:re_i + 1]:
        if in_win(x) or is_strload(x): continue
        if x.mnemonic == 'movdqa' and ripref(x) is not None:
            t = ripref(x); q = struct.unpack_from('<QQ', raw, off(t))
            vec_xmm[md.reg_name(x.operands[0].reg)] = q; continue
        if x.mnemonic == 'xorps': continue
        raise AssertionError(('領域内に想定外の命令', en, hex(x.address - IB), x.op_str))
    # NUL終端と size/cap の確認
    stores = [x for x in ins[rs_i:re_i + 1] if in_win(x)]
    assert any(x.operands[0].mem.disp == d0 + L and x.operands[0].size == 1 for x in stores), ('NUL終端ストアが無い', en)
    return dict(en=en, ja=ja, rs=rs, re=re_, base=base, d0=d0, vec=vec_xmm, f=f, L=L)

# 対象サイトを領域単位にまとめる
regions = {}
for s in inline_sites:
    if s['en'] in C.NOT_TRANSLATED: continue
    if s['en'] in getattr(C, 'HEAP_REGIONS_KEYS', ()): continue
    regions.setdefault((s['en'], s['va']), []).append(s)
REG_LIST = []
for (en, va), ss in regions.items():
    for s in ss:
        if s['mn'] not in ('mov', 'movsd', 'movups', 'movaps', 'movzx'): raise SystemExit('未知の参照形態 %s %r' % (s['mn'], en))
        L = len(en.encode())
        if L <= 15:
            REG_LIST.append(sso_region(s))
        else:
            REG_LIST.append(dict(en=en, ja=s['ja'], heap=True, addr=s['addr']))
print('inline regions:', len(inline_sites))
# ---- 領域の確定 -----------------------------------------------------------------
regions = {}
for s in inline_sites:
    if s['en'] in C.NOT_TRANSLATED: continue
    regions.setdefault((s['en'], s['va']), []).append(s)
REG_LIST = []
for (en, va), ss in regions.items():
    for s in ss:
        L = len(en.encode())
        if s['addr'] in C.HEAP_REGIONS:
            rs, re_, base, d0 = C.HEAP_REGIONS[s['addr']]
            f = func_of(rs); ins, idx = decode(f); bt = branch_targets(f)
            assert not any(rs < t < re_ for t in bt), ('領域内へ分岐', hex(rs))
            vec = {}
            for x in ins[idx[rs]:idx[re_]]:
                ok = x.mnemonic in ('movups', 'movaps', 'movdqu', 'movdqa', 'movzx', 'mov', 'xorps', 'movsd') or (x.mnemonic == 'call' and x.op_str == '0x%x' % (IB + 0x1be90))
                assert ok, ('ヒープ領域内に想定外の命令', hex(x.address - IB), x.mnemonic, x.op_str)
                if x.mnemonic == 'movdqa' and ripref(x) is not None:
                    vec[md.reg_name(x.operands[0].reg)] = struct.unpack_from('<QQ', raw, off(ripref(x)))
            REG_LIST.append(dict(en=en, ja=s['ja'], rs=rs, re=re_, base=base, d0=d0, vec=vec, f=f, L=L, heap=True))
        else:
            assert s['mn'] in ('mov', 'movsd', 'movups', 'movaps', 'movzx'), (s['mn'], en)
            assert L <= 15, ('SSO以外でHEAP_REGIONS未指定', en, hex(s['addr']))
            g = sso_region(s); g['heap'] = False; REG_LIST.append(g)

# ---- 領域置換コードの生成 -----------------------------------------------------------
n_reg = 0
for g in REG_LIST:
    en, ja, rs, re_, base, d0 = g['en'], g['ja'], g['rs'], g['re'], g['base'], g['d0']
    jb = ja.encode('utf-8'); po = add(jb + b'\0')
    lo = live_out(g['f'], re_, sorted(CLOB))
    code = enc_lea_rcx(base, d0)
    code += b'\x48\x8d\x15' + struct.pack('<i', jva(po) - (rs + len(code) + 7))
    code += b'\x41\xb8' + struct.pack('<I', len(jb))
    code += b'\xe8' + struct.pack('<i', C.STRCTOR - (rs + len(code) + 5))
    # 領域内で書かれ、領域後に読まれるレジスタの復元
    for R, why in sorted(lo.items()):
        if R in g['vec'] and R.startswith('xmm'):
            q = g['vec'][R]
            assert q[0] == g['L'] and q[1] >= 15 and (g.get('heap') or q[1] == 15), ('size/cap定数が想定外', R, q)
            n = int(R[3:]); assert n < 8
            code += bytes([0x0f, 0x10, 0x40 | (n << 3) | 1 if False else 0]) if False else b''
            # movups xmmN,[rcx+0x10]  (rcx は領域置換直後は壊れているので dest から再計算)
            code += enc_lea_rcx(base, d0 + 0x10) + bytes([0x0f, 0x10, (n << 3) | 1])
            log.append(('restore', R, hex(rs)))
        elif rs in C.POSTFIX and R == 'rcx':
            pass
        else:
            raise SystemExit('領域後に生きているレジスタ %s (%s) を復元できない: %r @%x' % (R, why, en, rs))
    if rs in C.POSTFIX:
        pb, text, src = C.POSTFIX[rs]
        o_ = off(src); x_ = next(md.disasm(raw[o_:o_ + 15], IB + src))
        assert x_.mnemonic + ' ' + x_.op_str == text and bytes(x_.bytes) == pb, ('POSTFIX元命令が一致しない', hex(src))
        code += pb
    size = re_ - rs
    assert len(code) <= size, ('置換コードが領域に収まらない', en, len(code), size)
    code += b'\x90' * (size - len(code))
    fo = off(rs); data[fo:fo + size] = code; changes.append((fo, size, 'inline@%x' % rs)); n_reg += 1
    log.append(('inline', en, hex(rs), hex(re_), base, hex(d0) if d0 >= 0 else '-' + hex(-d0), 'live-out=' + ','.join(sorted(lo))))
print('inline replaced:', n_reg)

# ---- ツールチップ(DrawTip)の拡大: 係数 15.0 / 300.0 を FONT_SCALE 倍した定数へ付け替える ----------
for a_, v_ in C.TIP_CONSTS:
    o_ = off(a_); x_ = next(md.disasm(raw[o_:o_ + 15], IB + a_))
    assert x_.mnemonic == 'mulss' and x_.size == 9 and x_.disp_offset == 5, (hex(a_), x_.op_str)
    t_ = a_ + 9 + [op for op in x_.operands if op.type == X86_OP_MEM][0].mem.disp
    assert struct.unpack_from('<f', raw, off(t_))[0] == v_, ('DrawTip係数が想定と違う', hex(a_))
    assert sec_of(a_) is tx and func_of(a_) is not None
    po_ = add(struct.pack('<f', v_ * C.FONT_SCALE))
    data[o_ + 5:o_ + 9] = struct.pack('<i', jva(po_) - (a_ + 9)); changes.append((o_ + 5, 4, 'tip@%x' % a_))
    log.append(('tip', hex(a_), v_, round(v_ * C.FONT_SCALE, 3)))

# ---- Label / LabelWidth / Text / TextSize / Paragraph スタブ ---------------------------------
# 非ASCIIを含む文字列のときだけ Text / TextSize へ振り分け(Label/LabelWidth)、
# 日本語のときだけ文字サイズを C.FONT_SCALE 倍する(題字を除く)。ASCIIのみなら原関数へそのまま飛ぶ。
# スタブは新設の .jpn セクション(読み取り+実行)の末尾に置く。
def rel32(src_end, dst): return struct.pack('<i', dst - src_end)
while len(pool) % 16: pool.append(0)
stub_base = new_va + len(pool)
sb = bytearray()                                    # スタブ領域(.jpn内オフセット = len(pool) + len(sb))
def sva(): return stub_base + len(sb)
# 共通ヘルパ: r9=ptr, r10=len -> CF=1 なら非ASCIIを含む。破壊: r9, r10, flags
helper_va = sva()
sb += b'\x4d\x85\xd2'                               # test r10, r10
sb += b'\x74\x0e'                                   # jz  -> clc; ret
sb += b'\x41\x80\x39\x80'                           # cmp byte ptr [r9], 0x80
sb += b'\x73\x0a'                                   # jae -> stc; ret
sb += b'\x49\xff\xc1\x49\xff\xca'                   # inc r9; dec r10
sb += b'\xeb\xed'                                   # jmp top
sb += b'\xf8\xc3'                                   # clc; ret
sb += b'\xf9\xc3'                                   # stc; ret
# 注: jz は 'clc;ret'(+0x0c相当)へ、jae は 'stc;ret' へ飛ぶ。位置を検証する
assert len(sb) == 23 and sb[19:23] == b'\xf8\xc3\xf9\xc3'
while len(sb) % 4: sb.append(0xcc)
factor_va = sva(); sb += struct.pack('<f', C.FONT_SCALE)
while len(sb) % 16: sb.append(0xcc)
LOAD_STACK5 = b'\x48\x8b\x44\x24\x28' b'\x4c\x8b\x08' b'\x4c\x8b\x50\x08'   # mov rax,[rsp+28h]; mov r9,[rax]; mov r10,[rax+8]
LOAD_RDX = b'\x4c\x8b\x0a' b'\x4c\x8b\x52\x08'                              # mov r9,[rdx]; mov r10,[rdx+8]
def mulss_xmm(n):          # mulss xmmN, [rip+factor]  (N=0 or 3)
    modrm = {0: 0x05, 3: 0x1d}[n]
    c = bytes([0xf3, 0x0f, 0x59, modrm]); return c + rel32(sva_now + len(c) + 4, factor_va)
def make_stub(load, ascii_to, non, scale_xmm=None):
    """non: ('jmp', 目的アドレス) または ('ts',)  = TextSize を呼んで幅(x)を xmm0 に返す"""
    global sva_now
    start = sva(); code = bytearray(load)
    code += b'\xe8' + rel32(start + len(code) + 5, helper_va)    # call helper
    jc_at = len(code); code += b'\x72\x00'                       # jc nonascii
    code += b'\xe9' + rel32(start + len(code) + 5, ascii_to)      # jmp ascii target
    code[jc_at + 1] = len(code) - (jc_at + 2)
    if scale_xmm is not None:
        sva_now = start + len(code); code += mulss_xmm(scale_xmm)
    if non[0] == 'jmp':
        code += b'\xe9' + rel32(start + len(code) + 5, non[1])
    else:
        code += b'\x48\x83\xec\x28'                                       # sub rsp,28h
        code += b'\xe8' + rel32(start + len(code) + 5, C.TEXTSIZE_VA)     # call TextSize (xmm0=size, rdx=string_view*)
        code += b'\x66\x0f\x6e\xc0'                                       # movd xmm0, eax
        code += b'\x48\x83\xc4\x28\xc3'                                   # add rsp,28h; ret
    sb.extend(code)
    while len(sb) % 16: sb.append(0xcc)
    return start
sva_now = 0
IBR = lambda a: new_va  # placeholder (未使用)
C.TEXTSIZE_VA = C.TEXTSIZE
def T_(a): return a
st_label_plain = make_stub(LOAD_STACK5, T_(C.LABEL), ('jmp', T_(C.TEXT)))
st_label_s = make_stub(LOAD_STACK5, T_(C.LABEL), ('jmp', T_(C.TEXT)), 3)
st_lw_plain = make_stub(LOAD_RDX, T_(C.LABELWIDTH), ('ts',))
st_lw_s = make_stub(LOAD_RDX, T_(C.LABELWIDTH), ('ts',), 0)
st_text_s = make_stub(LOAD_STACK5, T_(C.TEXT), ('jmp', T_(C.TEXT)), 3)
st_para_s = 0
st_ts_s = make_stub(LOAD_RDX, T_(C.TEXTSIZE), ('jmp', T_(C.TEXTSIZE)), 0)
pool.extend(sb)

# 題字(YOUR PARTY / BATTLE PLAN)を描く Label/LabelWidth 呼び出しは拡大しない。題字を持つ関数であることを確認する。
title_fn = {func_of(a_) for a_ in C.TITLE_CALLS}
assert len(title_fn) == 1, '題字呼び出しが複数の関数にまたがる'
tf = next(iter(title_fn))
title_leas = {a for k in ('YOUR PARTY', 'BATTLE PLAN') for v in rev[k.encode()] for a, x, f in refs.get(v, []) if f == tf}
assert len(title_leas) == 2, ('題字の参照が見つからない', title_leas)

def retarget_calls(target, plain, scaled, label):
    n = 0
    for f in funcs:
        for x in decode(f)[0]:
            if x.mnemonic == 'call' and x.operands[0].type == X86_OP_IMM and x.operands[0].imm - IB == target:
                a_ = x.address - IB
                dst = plain if (a_ in C.TITLE_CALLS and plain) else scaled
                o = off(a_)
                assert raw[o] == 0xe8
                data[o + 1:o + 5] = rel32(a_ + 5, dst); changes.append((o + 1, 4, label + '@%x' % a_)); n += 1
    return n
n_cl = retarget_calls(C.LABEL, st_label_plain, st_label_s, 'callLabel')
n_cw = retarget_calls(C.LABELWIDTH, st_lw_plain, st_lw_s, 'callLabelWidth')
n_ct = retarget_calls(C.TEXT, None, st_text_s, 'callText')
n_cs = retarget_calls(C.TEXTSIZE, None, st_ts_s, 'callTextSize')
n_cp = 0   # Paragraph は DrawTip からのみ呼ばれ、DrawTip の係数側で拡大済み
print('calls retargeted: Label %d LabelWidth %d Text %d TextSize %d Paragraph %d' % (n_cl, n_cw, n_ct, n_cs, n_cp))
stub_label_va, stub_lw_va = st_label_plain, st_lw_plain

# ---- .jpn セクション追加 --------------------------------------------------------------
while len(pool) % 16: pool.append(0)
pool_raw = al(len(pool), FA)
elf = pe.DOS_HEADER.e_lfanew
nsec_o = elf + 6
nsec = struct.unpack_from('<H', data, nsec_o)[0]
soh = struct.unpack_from('<H', data, elf + 20)[0]
tbl = elf + 24 + soh
hdr_end = tbl + nsec * 40
assert hdr_end + 40 <= min(s.PointerToRawData for s in secs), 'セクションヘッダの空きが無い'
assert all(b == 0 for b in data[hdr_end:hdr_end + 40])
hdr = b'.jpn\0\0\0\0' + struct.pack('<IIIIIIHHI', len(pool), new_va, pool_raw, new_raw, 0, 0, 0, 0, 0x60000060)
data[hdr_end:hdr_end + 40] = hdr; changes.append((hdr_end, 40, 'section-header'))
struct.pack_into('<H', data, nsec_o, nsec + 1); changes.append((nsec_o, 2, 'NumberOfSections'))
soi = elf + 24 + 56
struct.pack_into('<I', data, soi, al(new_va + len(pool), SA)); changes.append((soi, 4, 'SizeOfImage'))
struct.pack_into('<I', data, elf + 24 + 64, 0); changes.append((elf + 24 + 64, 4, 'CheckSum'))
assert len(data) == new_raw
data.extend(pool + b'\0' * (pool_raw - len(pool)))
open(OUT, 'wb').write(data)
print('出力:', OUT, len(data), 'bytes; .jpn VA=0x%x size=0x%x; stubs at 0x%x/0x%x' % (new_va, len(pool), stub_label_va, stub_lw_va))
json.dump(dict(src=SRC, jpn_va=new_va, jpn_size=len(pool), stub_label=stub_label_va, stub_labelwidth=stub_lw_va, font_scale=C.FONT_SCALE,
               stubs=dict(label_plain=st_label_plain, label_s=st_label_s, lw_plain=st_lw_plain, lw_s=st_lw_s, text_s=st_text_s, para_s=st_para_s, ts_s=st_ts_s),
               n_lea=n_lea, n_slot=n_slot, n_region=n_reg, n_label_calls=n_cl, n_labelwidth_calls=n_cw,
               changes=[(hex(a), n, l) for a, n, l in changes], log=[list(map(str, x)) for x in log]),
          open(REP, 'w'), ensure_ascii=False, indent=1)
