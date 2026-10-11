# -*- coding: utf-8 -*-
"""スタブをunicornで動かして、振り分け先と文字サイズ倍率を確認する。 使い方: python3 -I fwm_emu_stub.py <パッチ版DLL> <report.json>"""
import sys, json, struct
import pefile
from unicorn import *
from unicorn.x86_const import *
N, R = sys.argv[1:3]
r = json.load(open(R)); pe = pefile.PE(N); IB = pe.OPTIONAL_HEADER.ImageBase; raw = open(N, 'rb').read()
LABEL, LW, TEXT, TS, PARA = 0xa3b10, 0xa38c0, 0xa40f0, 0xa4230, 0xa3c70
SC = r['font_scale']
def f32(x): return struct.unpack('<I', struct.pack('<f', x))[0]
def run(stub, kind, sv):
    u = Uc(UC_ARCH_X86, UC_MODE_64)
    u.mem_map(IB, 0x200000)
    for s in pe.sections:
        u.mem_write(IB + s.VirtualAddress, raw[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData])
    u.mem_map(0x10000000, 0x10000); sp = 0x10008000; ret = 0x10009000
    u.mem_write(sp, struct.pack('<Q', ret)); u.reg_write(UC_X86_REG_RSP, sp)
    u.mem_write(0x10002000, b'LEVEL\0'); u.mem_write(0x10002100, 'レベル'.encode() + b'\0')
    u.mem_write(0x10002200, struct.pack('<QQ', *sv))
    u.mem_write(sp + 0x28, struct.pack('<Q', 0x10002200)); u.reg_write(UC_X86_REG_RDX, 0x10002200)
    u.reg_write(UC_X86_REG_XMM3, 16); u.reg_write(UC_X86_REG_XMM0, f32(10.0))
    u.reg_write(UC_X86_REG_XMM3, f32(10.0))
    hit = {}
    def h(uc, addr, size, ud):
        a = addr - IB
        if a in (LABEL, LW, TEXT, TS, PARA) and 'at' not in hit:
            hit['at'] = a
            hit['x0'] = struct.unpack('<f', (uc.reg_read(UC_X86_REG_XMM0) & 0xffffffff).to_bytes(4, 'little'))[0]
            hit['x3'] = struct.unpack('<f', (uc.reg_read(UC_X86_REG_XMM3) & 0xffffffff).to_bytes(4, 'little'))[0]
            if a == TS and kind == 'ts':      # LabelWidth(JP) は TextSize を call するので戻りを模擬
                uc.reg_write(UC_X86_REG_RAX, struct.unpack('<Q', struct.pack('<ff', 42.5, 9.0))[0])
                rsp = uc.reg_read(UC_X86_REG_RSP); ra = struct.unpack('<Q', bytes(uc.mem_read(rsp, 8)))[0]
                uc.reg_write(UC_X86_REG_RSP, rsp + 8); uc.reg_write(UC_X86_REG_RIP, ra); hit['viaCall'] = True
            else: uc.emu_stop()
    u.hook_add(UC_HOOK_CODE, h)
    try: u.emu_start(IB + stub, ret, count=500)
    except UcError as e: hit['err'] = str(e)
    return u, hit
ok = True
ASC, JP, EMP = (0x10002000, 5), (0x10002100, 9), (0x10002000, 0)
cases = [  # 名前, スタブ, 種別, 引数, 期待される到達先, xmm3倍率, xmm0倍率
    ('label_plain', 'stack', JP, TEXT, 1, 1), ('label_plain', 'stack', ASC, LABEL, 1, 1), ('label_plain', 'stack', EMP, LABEL, 1, 1),
    ('label_s', 'stack', JP, TEXT, SC, 1), ('label_s', 'stack', ASC, LABEL, 1, 1),
    ('text_s', 'stack', JP, TEXT, SC, 1), ('text_s', 'stack', ASC, TEXT, 1, 1),
    ('lw_plain', 'ts', JP, TS, 1, 1), ('lw_plain', 'ts', ASC, LW, 1, 1),
    ('lw_s', 'ts', JP, TS, 1, SC), ('lw_s', 'ts', ASC, LW, 1, 1),
    ('ts_s', 'jmp', JP, TS, 1, SC), ('ts_s', 'jmp', ASC, TS, 1, 1),
]
for name, kind, sv, want, k3, k0 in cases:
    u, hit = run(r['stubs'][name], kind, sv)
    good = hit.get('at') == want and abs(hit.get('x3', 0) - 10.0 * k3) < 1e-3 and abs(hit.get('x0', 0) - 10.0 * k0) < 1e-3 and 'err' not in hit
    if name.startswith('lw') and sv == JP:
        x0 = struct.unpack('<f', (u.reg_read(UC_X86_REG_XMM0) & 0xffffffff).to_bytes(4, 'little'))[0]
        good = good and abs(x0 - 42.5) < 1e-6 and u.reg_read(UC_X86_REG_RIP) == 0x10009000 and u.reg_read(UC_X86_REG_RSP) == 0x10008008
    print('%-12s %-4s -> %s  x3=%.2f x0=%.2f %s %s' % (name, 'JP' if sv == JP else ('ASCII' if sv == ASC else 'empty'), hex(hit.get('at', 0)), hit.get('x3', -1), hit.get('x0', -1), 'OK' if good else 'NG', hit.get('err', '')))
    ok &= good
print('結果:', 'OK' if ok else 'NG')
