# -*- coding: utf-8 -*-
"""テスト版 zip を作る(Python の zipfile 使用。パス区切りと改行を揃える)。
使い方(リポジトリのルートから):
  python3 -I tools/make_zip.py test out/Wayfarer.dll <N> --memo memo.txt [--font font/WalkWithMeInscription.ttf]
    -> out/WWM_test<N>.zip  (SKSE/Plugins/Wayfarer.dll, [SKSE/Plugins/Fonts/WalkWithMeInscription.ttf], テスト用メモ.txt)
Nexus 配布用 zip は、前回の配布 zip の構成が必要なため、まだこのスクリプトでは作らない(.claude/skills/release-package を参照)。"""
import argparse, os, zipfile

def put(z, arcname, data):
    zi = zipfile.ZipInfo(arcname, (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
    z.writestr(zi, data)

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest='mode', required=True)
t = sub.add_parser('test'); t.add_argument('dll'); t.add_argument('n'); t.add_argument('--memo', required=True); t.add_argument('--font'); t.add_argument('--out', default='out')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
path = os.path.join(a.out, 'WWM_test%s.zip' % a.n)
memo = open(a.memo, encoding='utf-8').read().replace('\r\n', '\n')
with zipfile.ZipFile(path, 'w') as z:
    put(z, 'SKSE/Plugins/Wayfarer.dll', open(a.dll, 'rb').read())
    if a.font: put(z, 'SKSE/Plugins/Fonts/WalkWithMeInscription.ttf', open(a.font, 'rb').read())
    put(z, 'テスト用メモ.txt', memo.encode('utf-8'))
print(path)
