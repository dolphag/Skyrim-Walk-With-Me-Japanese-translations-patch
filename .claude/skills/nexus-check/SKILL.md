---
name: nexus-check
description: Nexus Mods の mod ページ(Walk With Me 191283、パッチ 194872 など)の版・更新日・ファイル一覧(fileId・MAIN/ARCHIVED・サイズ・公開時刻・changelog)を API で読む。リリース前の「原 MOD の最新版確認」「自分のページの版の確認」に使う。権限(Permissions and credits)は API に無いので別手段。
---

# Nexus API で確認する

## 方式(houseCARL の `NexusClient.cs` に倣う)
- `POST https://api.nexusmods.com/v2/graphql`、本文は `{query, variables}` の JSON。**API キーなしで動く**(2026-10-26 に実測。詳細は `docs/nexus-api-notes.md`)。`NEXUS_API_KEY` が環境にあれば `apikey` ヘッダに付ける(任意)。
- 読み取り専用。mutation/subscription は送らない。ユーザー入力は variables で渡す。
- 実行: `python3 -I tools/nexus_query.py mod <modId> [--game skyrimspecialedition]`(概要+ファイル一覧)、`raw '<query>'`。

## 手順
1. `mod 191283`(Walk With Me)で `version` / `updatedAt` / `modFiles` を読み、手元の zip の版と照合する。
2. 自分のページは `mod 194872`。Nexus の版と zip 内 README の版の一致確認に使う。
3. 失敗したら(終了コード 1)、出たメッセージをそのまま報告する。**推測で埋めない**。

## ファイルの取得(任意・未検証)
`python3 -I tools/nexus_query.py download <modId> <fileId>`(v1 REST、`NEXUS_API_KEY` 必須、保存先 `out/nexus`)。Premium が要る可能性と CDN ホストの許可が未確認。失敗したら従来どおりユーザーが zip を添付する。取得した zip は編集せず、コミットしない。

## 限界(必ず守る)
- **権限(Permissions and credits)は GraphQL に無い**。ブラウザかユーザー確認(CLAUDE.md「Nexus の確認」)。API で取れた値だけを事実として書く。
- 環境が `api.nexusmods.com` を許可していないと使えない(許可前は CONNECT 403)。拒否されたら回避せず報告する。
- 新しいフィールドを使うときは introspection(`raw 'query{ __type(name:"ModFile"){ fields{ name } } }'`)で確認し、`docs/nexus-api-notes.md` に書く。
