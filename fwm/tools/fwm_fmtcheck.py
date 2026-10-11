# -*- coding: utf-8 -*-
"""書式文字列の検査: 原文と訳文の {} 置換フィールド(型指定・引数番号)が整合しているか。"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fwm_trans1 import T1
from fwm_trans2 import T2
T = {**T1, **T2}
F = re.compile(r'\{\{|\}\}|\{([0-9]*)(:[^{}]*)?\}')
def fields(s):
    out = []
    for m in F.finditer(s):
        if m.group(0) in ('{{', '}}'): continue
        out.append((m.group(1), m.group(2) or ''))
    return out
bad = 0; n = 0
for en, ja in T.items():
    fe, fj = fields(en), fields(ja)
    stray = re.sub(F, '', ja)
    if '{' in stray.replace('{{', '') or '}' in stray.replace('}}', ''):
        print('NG 対応しない波括弧', repr(ja[:60])); bad += 1
    if not fe and not fj: continue
    n += 1
    if any(i != '' for i, _ in fe): print('? 原文が番号指定', en[:50])
    specs_en = [s for _, s in fe]
    if any(i != '' for i, _ in fj):
        if not all(i != '' for i, _ in fj): print('NG 自動と番号の混在', ja[:60]); bad += 1; continue
        used = set()
        for i, s in fj:
            k = int(i)
            if k >= len(specs_en) or specs_en[k] != s:
                print('NG 番号%s の型指定が原文と不一致' % i, repr(s), en[:70]); bad += 1
            used.add(k)
        if used != set(range(len(specs_en))): print('NG 未使用/過不足の引数', sorted(used), len(specs_en), ja[:50]); bad += 1
    else:
        if [s for _, s in fj] != specs_en:
            print('NG 型指定の並びが不一致', [s for _, s in fe], [s for _, s in fj], '\n   ', en[:90], '\n   ', ja[:90]); bad += 1
print('書式付き文字列:', n, ' NG:', bad)
