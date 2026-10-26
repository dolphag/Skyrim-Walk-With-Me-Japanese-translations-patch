---
name: nexus-check
description: Nexus Mods の mod ページ(Walk With Me 191283、パッチ 194872 など)の版・更新日・ファイル一覧(fileId・MAIN/ARCHIVED・サイズ・公開時刻・changelog)を API で読む。リリース前の「原 MOD の最新版確認」「自分のページの版の確認」に使う。権限(Permissions and credits)と配布 zip のダウンロードは API で取れないので別手段。
---

# Nexus API で確認する

## 方式(houseCARL の `NexusClient.cs` に倣う)
- `POST https://api.nexusmods.com/v2/graphql`、本文は `{query, variables}` の JSON。**API キーは要らない**(2026-10-26 に実測。`docs/nexus-api-notes.md`)。
- 読み取り専用。mutation/subscription は送らない。ユーザー入力は variables で渡す。
- 実行: `python3 -I tools/nexus_query.py mod <modId> [--game skyrimspecialedition]`(概要+ファイル一覧。サイズ・公開時刻の ISO 表記つき)、`raw '<query>'`。

## 手順
1. `mod 191283`(Walk With Me)で `version` / `updatedAt` / `modFiles` を読み、手元の zip の版と照合する。
2. 自分のページは `mod 194872`。Nexus の版と zip 内 README の版の一致確認に使う。
3. 失敗したら(終了コード 1)、出たメッセージをそのまま報告する。**推測で埋めない**。

## 限界(必ず守る)
- **権限(Permissions and credits)は v1/v2 とも取れない**(確認済み)。リリース前の権限確認は、従来どおりブラウザかユーザー確認(CLAUDE.md「Nexus の確認」)。
- **配布 zip のダウンロードはできない**: `download_link` は非プレミアムで 403。原作 zip は従来どおりユーザーが添付する。
- 環境が `api.nexusmods.com` を許可していないと使えない(以前は CONNECT 403)。拒否されたら回避せず報告する。
- 新しいフィールドを使うときは introspection(`raw 'query{ __type(name:"ModFile"){ fields{ name } } }'`)で確認し、結果を `docs/nexus-api-notes.md` に書く。
