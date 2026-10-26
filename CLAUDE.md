# Walk With Me 日本語化パッチ(このリポジトリ)

Walk With Me(Nexus 191283)の日本語化パッチ。対象は `Wayfarer.dll`(静的な PE パッチ)と、置き換え用フォント。配布は Nexus(パッチ用ページ 194872)。原作者は hashhbbrown(GitHub: fatalCMD)。
Fight With Me / Paths のパッチは**別リポジトリ**(<https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch>)。そちらの `CLAUDE.md` と `docs/GLOSSARY.md` と揃える点が多い。
常時読み込まれるので短く保つ。手順は `.claude/skills/`、版ごとの調査は `docs/` に置く。

## 最初のセッションで確認すること(未確認の事項)
- [x] **テスト版の受け渡し経路**: `SendUserFile` でユーザーの手元に届く(2026-10-26、0.3.1 で確認)。テスト版 zip・配布 zip ともこれで渡す。DLL・フォントを GitHub に載せる方法は不可。
- [ ] 元 DLL(`Wayfarer.dll`)は毎回ユーザーが添付する(新版の原作 zip でよい)。SHA-256 が `8b8d398a…3c40`(0.3.1。0.3.0 は `a0e90379…97b5b4`)であることを確認する(`tools/build_patch.py` も検査する)。
- [ ] フォントのビルドには `NotoSansJP-Medium.ttf` と Cinzel Decorative の原 TTF が必要(どちらも OFL)。ユーザーに添付してもらう。訳文に新しい漢字が増えない版は、前版の公開 zip のフォントをそのまま使える(0.3.1 はこの方法。前版の公開 zip を添付してもらう)。

## 応答のしかた
- 日本語。率直・技術的に正確に。褒めない・慰めない。誤りは、どの前提が誤りだったかを示して認める。
- 事実が不確かなら推測せず確認する(Nexus の権限・版・更新時刻、上流の状態など)。確認できなかったことは「未確認」と書く。
- 作業の最後に、やったこと/やっていないこと/ユーザーが判断すること、を分けて報告する。

## 権利・配布(絶対に守る)
- **GitHub はソースのみ。DLL・フォント・zip・出力物はコミットしない**(`.gitignore` で除外)。バイナリは Nexus のみ。
- 逆アセンブル結果や文字列ダンプ(原 DLL の写し)も保存しない。必要なら再生成する。
- **ライセンスは FWM と違う**: Walk With Me は GPL-3.0-or-later(例外付き)。`LICENSE` / `EXCEPTIONS.md` / `LICENSING.md` に従い、勝手に解釈を変えない。フォントは SIL OFL 1.1(`licenses/`、Cinzel の予約フォント名のためファミリー名を変更している)。
- リリースごとに、原 MOD の Nexus ページの権限(Permissions and credits)をその時点で確認し、確認日を README に書く。変わっていたら止めてユーザーに報告。
- 原作者クレジット(hashhbbrown)を、README・Nexus 説明・Nexus の **File credits 欄**に入れる。
- **ユーザーの許可なしにしない**: main への push、タグ、Nexus 投稿、原作者への連絡、削除。作業ブランチへの push は可。Nexus へのアップロードとタグ付け(GitHub Release)はユーザーが行う。
- ユーザーが添付した元ファイルは編集しない。コピーで作業する。

## 版番号
- 原 MOD に連動する(WWM 0.3.0 → パッチ 0.3.0-N)。パッチだけの修正は枝番(Nexus の配布は FOMOD なし、ASCII のファイル名、`LICENSES/` 1 フォルダ)。
- **Nexus の版と、zip 内 README の版を必ず一致させる**。
- 0.3.1 の初回リリースは、ユーザーの指定で **0.3.1-1**(DLL を作り直した版でも枝番 `-1` から始める)。配布 zip のファイル名は `Walk With Me - Japanese Translations Patch <版>.zip`(`make_zip.py release` が付ける)。GitHub のタグは `wwm-<版>`(例: `wwm-0.3.1-1`)。
- 版ごとに新しいセッションで始める。フォークで前の版の文脈を引き継がない(アドレスが版ごとに違うため、古い前提が混ざる)。過去の版は `wwm-0.2.5/` とタグに残っている。持ち越す知識は `docs/` に書いてあるものだけ。

## 翻訳・表示のルール
- 用語は公式日本語訳(Fandom wiki の一覧。ファンによる抽出であり公式サイトではない)に従う。
- 使える漢字は、置き換えフォント(Noto Sans JP のサブセット)に入れたものだけ。翻訳に使う漢字は、フォントのビルドで取り込まれる。
- 訳しないもの: ホイールのモード名・タイル名(Natural/Lead など)、HUD、通知、ログ、コード内に埋め込まれていて安全に置換できないもの。
- 日本語は英字より小さく見える。拡大が必要な箇所は、DLL 内の定数を書き換える(README の表)。
- 利用者は FWM / Paths と WWM の関係を意識していない前提で説明を書く。特定の外部作品(MTG 等)を強調しない。

## 作業の進め方
- 手順の詳細は skill `pe-patch-workflow`(ビルド・検証・テスト版 zip)、`release-package`(README・Changelog・配布 zip・Nexus 文面・タグ)。テスト版 zip は `tools/make_zip.py`、メモの雛形は `release/`。配布用 zip は `tools/make_zip.py release`(README 雛形・Nexus 説明の雛形は `release/`、手順は release-package)。
- **実機(ゲーム内)確認なしにリリースしない**。テスト版は `out/` に作り(git 管理外)、ユーザーのスクリーンショットと所見で直す。
- 逆アセンブル・アドレス調査の結果は必ずファイルに残す(`docs/` またはコード内コメント)。会話には残らない前提で作業する。
- 大きいファイルは全文を読まず、必要な範囲だけ読む。
- 依存: `pip install -r requirements-dev.txt`(`python3 -I` で実行)。

## 外部の参照(試用中)
- FWM リポジトリの `CLAUDE.md` にある houseCARL 参照の運用と同じ。ここでは SKSE プラグインの構造調査が必要になったときだけ使い、`docs/houseCARL-reference-log.md` に記録する。リポジトリはセッションに追加しない。

## Nexus の確認
- WebFetch は Nexus で失敗しやすい(PROVENANCE_REQUIRED)。ブラウザ(Claude in Chrome 等)が使える場合はそれで開く。使えない場合は、ユーザーに確認を依頼する。
- API で引く手段: skill `nexus-check`(`tools/nexus_query.py`、キー不要、版・ファイル一覧は実測済み)。環境が api.nexusmods.com を許可している必要がある。**権限(Permissions)と配布 zip のダウンロードは API で取れない**(後者は非プレミアムで 403)→ ブラウザかユーザー確認、zip はユーザーが添付。詳細は `docs/nexus-api-notes.md`。
- ページの権限・版・ファイル名・更新時刻は、実際に読み取ったものだけを事実として扱う。
