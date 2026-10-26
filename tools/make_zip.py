# -*- coding: utf-8 -*-
"""テスト版 zip を作る(Python の zipfile 使用。パス区切りと改行を揃える)。
使い方(リポジトリのルートから):
  python3 -I tools/make_zip.py test out/Wayfarer.dll <N> --memo memo.txt [--font font/WalkWithMeInscription.ttf]
    -> out/WWM_test<N>.zip  (SKSE/Plugins/Wayfarer.dll, [SKSE/Plugins/Fonts/WalkWithMeInscription.ttf], テスト用メモ.txt)
  python3 -I tools/make_zip.py release out/Wayfarer.dll font/WalkWithMeInscription.ttf --version 0.3.0-1 --base <前回配布 zip を展開したディレクトリ> [--out out]
    -> out/Walk With Me - Japanese Translations Patch <版>.zip  (Nexus 配布用。構成は 0.3.0-1 の公開 zip と同じ)
    README は release/README_{Japanese,English}.txt の {ORIG_SHA} {OUT_SHA} を置換して作る。更新履歴に "Version <版>" の項がなければ失敗する。
    LICENSE / EXCEPTIONS.md / LICENSING.md / LICENSES/OFL_*.txt はリポジトリのもの。
    LICENSES/Wayfarer-MIT.txt と ThirdParty/ は原作の配布物の写しなのでリポジトリに置かず、--base から取る。"""
import argparse, hashlib, os, re, zipfile

def put(z, arcname, data):
    zi = zipfile.ZipInfo(arcname, (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
    z.writestr(zi, data)

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest='mode', required=True)
t = sub.add_parser('test'); t.add_argument('dll'); t.add_argument('n'); t.add_argument('--memo', required=True); t.add_argument('--font'); t.add_argument('--out', default='out')
r = sub.add_parser('release'); r.add_argument('dll'); r.add_argument('font'); r.add_argument('--version', required=True); r.add_argument('--base', required=True); r.add_argument('--out', default='out')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
if a.mode == 'release':
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    orig = re.search(r"ORIG_SHA256 = '([0-9a-f]{64})'", open(os.path.join(root, 'tools/build_patch.py'), encoding='utf-8').read()).group(1)
    dll = open(a.dll, 'rb').read(); out_sha = hashlib.sha256(dll).hexdigest()
    entries = {}
    for n in ('Japanese', 'English'):
        t = open(os.path.join(root, 'release/README_%s.txt' % n), encoding='utf-8').read().replace('\r\n', '\n')
        t = t.replace('{ORIG_SHA}', orig).replace('{OUT_SHA}', out_sha)
        if re.search(r'\{(ORIG_SHA|OUT_SHA)\}', t): raise SystemExit('README に未置換のプレースホルダがあります')
        if 'Version ' + a.version not in t: raise SystemExit('README の更新履歴に "Version %s" の項がありません(雛形に追記してください): %s' % (a.version, n))
        entries['README_%s.txt' % n] = t.encode('utf-8')
    for f in ('LICENSE', 'EXCEPTIONS.md', 'LICENSING.md'): entries[f] = open(os.path.join(root, f), 'rb').read()
    for f in ('OFL_CinzelDecorative.txt', 'OFL_NotoSansJP.txt'): entries['LICENSES/' + f] = open(os.path.join(root, 'licenses', f), 'rb').read()
    entries['LICENSES/Wayfarer-MIT.txt'] = open(os.path.join(a.base, 'LICENSES/Wayfarer-MIT.txt'), 'rb').read()
    tp = os.path.join(a.base, 'ThirdParty')
    for d, _, fs in os.walk(tp):
        for f in fs:
            full = os.path.join(d, f); entries['ThirdParty/' + os.path.relpath(full, tp).replace(os.sep, '/')] = open(full, 'rb').read()
    entries['SKSE/Plugins/Wayfarer.dll'] = dll
    entries['SKSE/Plugins/Fonts/WalkWithMeInscription.ttf'] = open(a.font, 'rb').read()
    path = os.path.join(a.out, 'Walk With Me - Japanese Translations Patch %s.zip' % a.version)
    with zipfile.ZipFile(path, 'w') as z:
        for k in sorted(entries): put(z, k, entries[k])
    print(path, 'out_sha', out_sha)
    raise SystemExit(0)
path = os.path.join(a.out, 'WWM_test%s.zip' % a.n)
memo = open(a.memo, encoding='utf-8').read().replace('\r\n', '\n')
with zipfile.ZipFile(path, 'w') as z:
    put(z, 'SKSE/Plugins/Wayfarer.dll', open(a.dll, 'rb').read())
    if a.font: put(z, 'SKSE/Plugins/Fonts/WalkWithMeInscription.ttf', open(a.font, 'rb').read())
    put(z, 'テスト用メモ.txt', memo.encode('utf-8'))
print(path)
