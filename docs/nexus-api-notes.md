# Nexus API メモ

出典: houseCARL(Avick3110/houseCARL、GPL-3.0、`1037f7f`)の `src/housecarl-mcp/NexusClient.cs`、`docs/architecture/nexus.md`。コードはコピーしていない。実測は 2026-10-26 のこのリポジトリのセッション(`tools/nexus_query.py`)。

## 実測で確認済み(キーなし)
- `POST https://api.nexusmods.com/v2/graphql` は匿名で読める。`mod 194766` で版 0.5.0、更新 2026-10-25、`modFiles` 全件(fileId・name・version・category・date・description・changelogText)が返った。
- `ModFile` 型のフィールド: `size`(KB)、`sizeInBytes`、`primary`(MAIN なら 1)、`uri`(CDN 内パスで、ダウンロード URL ではない)、`totalDownloads`、`uniqueDownloads`、`scannedV2`(ウイルス検査)ほか。category の値: MAIN / UPDATE / OPTIONAL / OLD_VERSION / MISCELLANEOUS / REMOVED / ARCHIVED。`date` は UNIX 秒。
- `Mod` 型にはファイルサイズ(`fileSize`)、`directDownloadEnabled`、`uploader`、`modRequirements` などがある。introspection(`__type` / `__schema`)は許可されている。

## 確認した結果、無かったもの
- **権限(Permissions and credits)に当たるフィールドは `Mod` 型に無い**(347 型の名前を `permission|credit|licen|download|link` で検索。`Permission` 型は `global`/`key` だけで、ユーザー権限の型と思われる)。権限の確認は従来どおりブラウザかユーザー確認。v1 REST にあるかは未確認。
- **ダウンロード URL を返すクエリは GraphQL に無い**(mutation にも `download` 系は `updateModDirectDownloadEnabled` のみ)。

## 未確認
- `modFileContents`(zip 内のファイル一覧)は動くが、FWM 0.5.0 MAIN(fileId 825644)では 0 件だった。索引されていないのか、フィルタの指定が違うのか不明。
- v1 REST の `download_link.json`(要 API キー)。`NEXUS_API_KEY` が無いので未実行。Premium 限定かどうか、CDN ホストがこの環境で許可されているかも未確認。Premium でない場合、Nexus は nxm リンク由来の `key`/`expires` を要求するはず(要確認。キー単体では取れない可能性が高い)。
- キーを付けた GraphQL で増えるもの(`viewer*` 系フィールドなど)。
