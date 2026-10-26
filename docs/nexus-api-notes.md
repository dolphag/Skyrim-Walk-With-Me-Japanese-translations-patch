# Nexus API メモ

2026-10-26 調査。出典: houseCARL(Avick3110/houseCARL、GPL-3.0、`1037f7f`)の `src/housecarl-mcp/NexusClient.cs` と `docs/architecture/nexus.md`。コードはコピーしていない。

## 実接続の確認結果(2026-10-26、NEXUS_API_KEY 設定後に測定)
- `api.nexusmods.com` に接続できる(以前はプロキシが CONNECT 403 で拒否していた。環境の許可後は通る)。
- キーは環境変数 `NEXUS_API_KEY`(v1 の `apikey` ヘッダで使う)。**キーの値は出力・保存しない**。
- 制限: 1 時間 2000 回、1 日 20000 回(`x-rl-*` ヘッダ)。アカウントは非プレミアム。

### キーの要否(キーなしで再測定、同日)
- **v2 GraphQL はキーなしで、自分の MOD(194874)も含め、版・更新時刻・DL 数・endorse 数・説明文(BBCode)・ファイル一覧(`fileId`/`category`/`version`/`date`/`changelogText`)まで取れる**。v1 で見えた情報の大半は v2 だけで足りる。
- v1 REST はキーなしだと 401(`Please provide an authentication method`)。v1 だけで得られる利点は、キー検証、レート制限ヘッダ、追跡 MOD 一覧、`file_name`(zip 名)程度。
- 接続できるようになった原因がキーなのか、ネットワーク許可の変更なのかは**切り分けていない**(以前は CONNECT 403 だったが、いつ・何が変わったかは未確認)。「キー設定で使えるようになった」とは言えない。

### v1 REST(キー必須)で取れたもの
- `GET /v1/users/validate.json`: キーの検証(名前、プレミアムか)。
- `GET /v1/games/skyrimspecialedition/mods/{id}.json`: 名前、版、作者、更新時刻、`status`、`description`(HTML)、DL 数など。**権限(Permissions)のフィールドは無い**。FWM 194766 の `description`(8812 文字)にも権限の文言は無かった。
- `.../mods/{id}/files.json`: ファイル一覧(`category_name`: MAIN/OLD_VERSION/ARCHIVED、版、`uploaded_time`、`file_name`)。
- `.../mods/{id}/changelogs.json`: 版ごとの changelog。
- `GET /v1/user/tracked_mods.json`: アカウントの追跡 MOD(読み取り)。
- **取れなかった**: `.../files/{id}/download_link.json` は 403(プレミアム専用)。配布 zip を API で取得して中身を照合することはできない。

### v2 GraphQL(`tools/nexus_query.py`)
- 匿名で読める(houseCARL の主張どおり)。`tools/nexus_query.py mod 194766` は動作した。
- `Mod` 型のフィールド: `description, summary, version, updatedAt, createdAt, downloads, endorsements, fileSize, modRequirements, tags, uploader, status` など。**権限・ライセンスに当たるフィールドは無い**。`Permission` 型は `Collection` 用のみ。

### v2 の型の詳細(introspection、2026-10-26)
- `ModFile` のフィールド: `fileId` `name` `version` `category` `date`(UNIX 秒)`description` `changelogText` `size`(KB)`sizeInBytes` `primary`(MAIN なら 1)`uri`(CDN 内パスで、ダウンロード URL ではない)`totalDownloads` `uniqueDownloads` `scannedV2` ほか。`category` の値: MAIN / UPDATE / OPTIONAL / OLD_VERSION / MISCELLANEOUS / REMOVED / ARCHIVED。
- GraphQL にダウンロード URL を返すクエリは無い(mutation にも `updateModDirectDownloadEnabled` のみ)。
- `modFileContents`(zip 内のファイル一覧)は動くが、FWM 0.5.0 MAIN(fileId 825644)では 0 件だった。索引されていないのか、フィルタの指定(`fileId`/`modId`/`gameId` は `{value: Int, op: EQUALS}` の配列)が違うのかは不明。

## 結論
- **原 MOD の Nexus 権限(Permissions and credits)は API で取れない**。リリース前の権限確認は、従来どおりブラウザかユーザー確認。
- API で確認できる: 原 MOD の版・更新時刻・changelog、自分のページの版・ファイル一覧(Nexus の版と zip 内 README の版の一致確認)。

## 観察した事実(2026-10-26 時点)
- FWM 194766: 版 0.5.0、更新 2026-10-25T04:43:07Z。0.5.0 は ARCHIVED(2026-10-24)と MAIN(2026-10-25)の 2 件がある。
- パッチ 194874: 版 0.5.0-1、更新 2026-10-26T06:41:41Z、MAIN は `Fight With Me - Japanese Translations` 0.5.0-1。

## 未確認
- v1 に権限を返すエンドポイントがあるか(公開ドキュメントで確認していない)。
- `description` が本文を含む MOD で、権限が本文に書かれている場合の扱い。
