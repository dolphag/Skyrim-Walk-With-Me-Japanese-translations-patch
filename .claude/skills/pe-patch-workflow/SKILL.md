---
name: pe-patch-workflow
description: Wayfarer.dll(Walk With Me)の日本語化パッチを作る・直す・検証するときの手順。訳文の変更、拡大定数の調整、フォントのビルド、新しい版への移行、ビルドと検証の流れ、既知の落とし穴。
---

# WWM DLL パッチの作業手順

対象: `Wayfarer.dll`(Walk With Me 0.3.1。0.3.0 の記録は `docs/` とタグ `wwm-0.3.0`)。静的な PE パッチ。アドレスは版固定。

## 前提
- 元 DLL はユーザーが添付し、`wwm/SKSE/Plugins/Wayfarer.dll` に置く(git 管理外)。SHA-256 は `8b8d398a146415d17bb659003121871a41566e109ca78c461ea3854e6cff3c40`(0.3.1)。`tools/build_patch.py` は一致しなければ失敗する。
- 出力は `out/`(git 管理外)。依存は `pip install -r requirements-dev.txt`。実行はリポジトリのルートから `python3 -I`。

## 通常の変更(翻訳・表示の調整)
1. 訳文・パッチ箇所(アドレス)・定数は `tools/trans_ja.py`。文字列の分類は `tools/tier1.py` / `tier1.json`。
2. 生成: `mkdir -p out && python3 -I tools/build_patch.py wwm/SKSE/Plugins/Wayfarer.dll out/Wayfarer.dll`(`changes.json` も出る)
3. 検証: `python3 -I tools/verify.py`(変更バイトがすべて記録されているか、参照が新セクション `.jpn` に届くか)
4. 期待する出力 SHA-256(0.3.1 テスト版 4): `577dca9fd583d7ff2ddcd1b02e131a4cd8bc2f56de910b626b6fea6a97b188e5`。訳文を変えたら変わるので、README の値も更新する。
5. 翻訳表: `translations_en_ja.csv`(UTF-8 BOM、ヘッダ行あり)を更新する。
6. フォント: `python3 -I tools/build_font.py NotoSansJP-Medium.ttf <Cinzel ttf> font/`(OFL。Cinzel のファミリー名は変更する)。訳文に使う漢字が増えたら再ビルド。
7. テスト版 zip を作ってユーザーに渡す(経路は CLAUDE.md の「最初のセッションで確認すること」)。
   - メモを `release/TEST_MEMO_TEMPLATE.txt` の形で書く(前回からの変更、確認してほしい点、補足)。
   - `python3 -I tools/make_zip.py test out/Wayfarer.dll <N> --memo <メモ> [--font font/WalkWithMeInscription.ttf]` → `out/WWM_test<N>.zip`。
   - ユーザーのスクリーンショットと所見で直す。

## 拡大定数
- 日本語は英字より小さく見えるため、ホイール中央の説明、Party Actions のフッター、下部の操作ヒントは、サイズ上限と最大幅の定数を書き換えている(値は README の表)。追加するときは、どの呼び出しアドレスの定数かを特定してから書き換える。全体の倍率は変えない。

## 既知の落とし穴
- 文字列を使う側が NUL 終端か、長さ即値(fmt の string_view)かで、置換方法が違う。長さを持つ箇所は即値も書き換える。
- インライン展開された `std::string` の構築は、既存のコンストラクタ呼び出しへ置き換える(レジスタの生存を確認する)。
- ポインタ表(`.rdata`)を書き換えるときは、再配置エントリがあることを確認する。
- 署名・オーバーレイがある DLL は扱えない(`build_patch.py` が検査する)。

## 新しい版へ移行するとき
1. 新しい元 DLL を受け取り、SHA-256 を記録する。
2. 旧版のパッチ箇所を、新版の対応アドレスへ移す(旧 DLL が無くても、英語原文と命令の形で探せる。0.3.1 の例は `docs/ADDRESSES-0.3.1.md`、メニュー関数の洗い出しは `tools/tier1.py`)(`tools/dis.py` / `dis2.py` で確認)。命令列(アドレスをマスク)で探す方法は、FWM リポジトリの `tools/dev/sigfind.py` が使用例。
3. 文字列の増減を洗い出し、翻訳表と `tools/trans_ja.py` を更新する。
4. 版ごとの調査結果を `docs/ADDRESSES-<版>.md` に残す。前の版のセッションの文脈を引き継がない。
