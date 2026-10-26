# -*- coding: utf-8 -*-
"""Nexus Mods の公開 v2 GraphQL API を読み取り専用で引く。標準ライブラリのみ。API キーは使わない。

方式は houseCARL(Avick3110/houseCARL、GPL-3.0)の NexusClient.cs を参考にした(自分の言葉で書き直したもの)。
エンドポイント https://api.nexusmods.com/v2/graphql に {query, variables} を POST するだけ。
クエリは houseCARL が使っているフィールドに限る。ここでの実機確認の状況は docs/nexus-api-notes.md を参照。

使い方(リポジトリのルートから):
  python3 -I tools/nexus_query.py mod 194766              # 概要+ファイル一覧(版・更新日・changelog)
  python3 -I tools/nexus_query.py mod 194874 --game skyrimspecialedition
  python3 -I tools/nexus_query.py raw 'query{ game(domainName:"skyrimspecialedition"){ id name } }'

mutation / subscription は送らない。失敗は終了コード 1 とメッセージで返す(例外のまま落とさない)。"""
import argparse, datetime, json, os, re, sys, urllib.parse, urllib.request, urllib.error

ENDPOINT = 'https://api.nexusmods.com/v2/graphql'
GAMES = {'skyrimspecialedition': 1704}   # houseCARL の固定表のうち、このリポジトリで使うもの
UA = 'fwm-ja-patch-tools (read-only)'
V1 = 'https://api.nexusmods.com/v1'
KEY_ENV = 'NEXUS_API_KEY'   # 任意。環境の secrets に置く。出力・ログ・コミットに出さない

MOD_QUERY = """query ModDetail($modId: ID!, $gameId: ID!) {
  mod(modId: $modId, gameId: $gameId) {
    modId name version summary author category endorsements downloads
    updatedAt createdAt adultContent status fileSize
  }
  modFiles(modId: $modId, gameId: $gameId) {
    fileId name version category date description changelogText
    size sizeInBytes primary uri
  }
}"""


def is_mutating(query):
    # 文書の先頭、または直前の操作の閉じ括弧の後に mutation/subscription がある場合だけ拒否する(フィールド名への誤検出を避ける)
    return re.search(r'(^|\})\s*(mutation|subscription)\b', query, re.I) is not None


def key_headers():
    k = os.environ.get(KEY_ENV)
    return {'apikey': k} if k else {}


def post(query, variables=None, timeout=30):
    """(data, None) か (None, エラー文) を返す。"""
    if is_mutating(query):
        return None, 'mutation / subscription は送らない(読み取り専用)'
    body = json.dumps({'query': query, 'variables': variables or {}}).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=body, method='POST',
                                 headers={'Content-Type': 'application/json', 'User-Agent': UA, **key_headers()})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return None, 'HTTP %d %s%s' % (e.code, e.reason, '(レート制限)' if e.code == 429 else '')
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, '接続できない: %s(環境のネットワーク許可に api.nexusmods.com があるか確認)' % e
    try:
        doc = json.loads(raw)
    except ValueError as e:
        return None, '応答が JSON でない: %s' % e
    if doc.get('errors'):
        return None, 'GraphQL エラー: ' + '; '.join(str(x.get('message')) for x in doc['errors'])
    if not isinstance(doc.get('data'), dict):
        return None, '応答に data が無い'
    return doc['data'], None


def game_id(value):
    if value.isdigit():
        return value
    if value.lower() in GAMES:
        return str(GAMES[value.lower()])
    data, err = post('query($d: String!){ game(domainName:$d){ id } }', {'d': value})
    if err or not data.get('game'):
        sys.exit('ゲームを解決できない: %s (%s)' % (value, err or '該当なし'))
    return str(data['game']['id'])


def v1_get(path, timeout=30):
    """v1 REST(要 API キー)。(json, None) か (None, エラー文)。"""
    if not key_headers():
        return None, '%s が未設定(v1 REST は API キーが必要)' % KEY_ENV
    req = urllib.request.Request(V1 + path, headers={'User-Agent': UA, **key_headers()})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        hint = {401: 'キーが無効', 403: 'この操作には権限が足りない(Premium 限定の可能性。未確認)', 429: 'レート制限'}.get(e.code, '')
        return None, 'HTTP %d %s %s' % (e.code, e.reason, hint)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        return None, '接続できない/不正な応答: %s' % e


def download(game, mod_id, file_id, out_dir):
    data, err = v1_get('/games/%s/mods/%s/files/%s/download_link.json' % (game, mod_id, file_id))
    if err:
        return err
    if not data or not isinstance(data, list) or 'URI' not in data[0]:
        return '応答にダウンロード URL が無い'
    url = data[0]['URI']
    host = urllib.parse.urlparse(url).hostname or ''
    if not url.startswith('https://'):
        return 'https でない URL は取得しない'
    os.makedirs(out_dir, exist_ok=True)
    name = os.path.basename(urllib.parse.urlparse(url).path) or '%s-%s.bin' % (mod_id, file_id)
    dest = os.path.join(out_dir, name)
    try:   # CDN には API キーを送らない
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120) as r, open(dest, 'wb') as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 'ダウンロード失敗(%s): %s(CDN ホストの許可が要る可能性)' % (host, e)
    print('保存: %s (%d bytes)' % (dest, os.path.getsize(dest)))
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    m = sub.add_parser('mod', help='mod の概要とファイル一覧')
    m.add_argument('mod_id')
    m.add_argument('--game', default='skyrimspecialedition', help='ドメイン名か数値 ID(既定: skyrimspecialedition)')
    d = sub.add_parser('download', help='ファイルを取得(要 NEXUS_API_KEY。Premium が要る可能性。未検証)')
    d.add_argument('mod_id')
    d.add_argument('file_id')
    d.add_argument('--game', default='skyrimspecialedition')
    d.add_argument('--out', default='out/nexus', help='保存先(既定 out/nexus。git 管理外)')
    r = sub.add_parser('raw', help='任意の読み取りクエリ')
    r.add_argument('query')
    r.add_argument('--vars', default='{}', help='変数の JSON')
    a = ap.parse_args()

    if a.cmd == 'download':
        err = download(a.game, a.mod_id, a.file_id, a.out)
        if err:
            print(err, file=sys.stderr)
        return 1 if err else 0
    if a.cmd == 'mod':
        data, err = post(MOD_QUERY, {'modId': a.mod_id, 'gameId': game_id(a.game)})
        for f in (data or {}).get('modFiles') or []:   # 読みやすいよう公開時刻を ISO にする
            if isinstance(f.get('date'), int):
                f['date_iso'] = datetime.datetime.fromtimestamp(f['date'], datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        data, err = post(a.query, json.loads(a.vars))
    if err:
        print(err, file=sys.stderr)
        return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
