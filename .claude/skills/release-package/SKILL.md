---
name: release-package
description: WWM 日本語化パッチのリリース準備(配布 zip、README、Nexus 用テキスト、タグ)。版番号・クレジット・権限確認・ライセンス・作業の順序のチェックリスト。
---

# リリース準備チェックリスト

配布はユーザーが行う(Nexus アップロード、GitHub のタグ/Release)。このスキルは準備と確認。

## 順序(守る)
1. 実機確認が済んでいること(ユーザーの「OK」)。
2. **原 MOD の Nexus ページの権限をその時点で確認**(Permissions and credits)。確認日を README に書く。変更があれば止めてユーザーに報告。
3. 版番号を決める: 原 MOD に連動(WWM 0.3.0-N)。**Nexus の版と zip 内 README の版を一致させる**。
4. リポジトリの README(日本語は `README.ja.md`、英語は `README.md`)、翻訳表 CSV、元 DLL / 出力 DLL の SHA-256 を更新する。
   配布 zip 内の README(日本語・英語)も、**更新履歴(Changelog。最新を先頭に追記)**、変更点、確認日、版を直す。
   README の雛形は `release/README_Japanese.txt` / `README_English.txt`(0.3.0-1 の公開 zip から作成。`{ORIG_SHA}` `{OUT_SHA}` `{VERSION}` を置換)。新しい版では、3 行目付近の改訂の注記と変更点・確認日を雛形で直す。Changelog 欄は現状の雛形にない。必要なら雛形に追加する(0.3.0-1 の再現は崩れる)。
5. zip を作る: `python3 -I tools/make_zip.py release out/Wayfarer.dll font/WalkWithMeInscription.ttf --version <版> --base <前回配布 zip の展開先>`。`--base` から `ThirdParty/` と `LICENSES/Wayfarer-MIT.txt`(原作の配布物の写し。リポジトリには置かない)を取る。LICENSE / EXCEPTIONS.md / LICENSING.md / OFL はリポジトリのもの。
6. Nexus 用テキスト(更新履歴・説明・クレジット欄)を作る。説明の雛形: `release/NEXUS_DESCRIPTION_WWM.bbcode.txt`(2026-10 時点で公開中のもの)。
7. **main へ統合 → main の HEAD を確認 → ユーザーがそのコミットにタグ**(`wwm-<版>` の形式)。タグは GitHub の Release で、ユーザーが付ける。
8. ユーザーが Nexus にアップロードしたら、ブラウザで開いて確認する(版、ファイル名、サイズ、説明、File credits 欄)。

## zip の構成(0.3.0-1 以降の方針)
- FOMOD なし、ASCII のファイル名、ライセンス文書は `LICENSES/` 1 フォルダにまとめる。
- 構成は 0.3.0-1 の公開 zip(34 ファイル)を `make_zip.py release` が全ファイル同一内容で再現することを確認済み(2026-10-25)。ルート: README ×2、LICENSE、EXCEPTIONS.md、LICENSING.md、`LICENSES/`(OFL ×2 + Wayfarer-MIT)、`ThirdParty/`(原作の第三者ライセンス一式)、`SKSE/Plugins/Wayfarer.dll`、`SKSE/Plugins/Fonts/WalkWithMeInscription.ttf`。
- zip は Python の `zipfile` で作る(パス区切りと改行を揃える)。

## README / Nexus 文面に必ず入れること
- 原作者クレジット(hashhbbrown)、原 MOD へのリンク、権限の確認日。
- 元 DLL と出力 DLL の SHA-256。他版には使わないこと。更新時は先にパッチを外すこと。
- ライセンス(GPL-3.0-or-later と例外、フォントは OFL)と、原作のソースへのリンク。
- 「GitHub にはソースのみ、バイナリは Nexus のみ」。AI 利用の開示。非公式で、原作者に問い合わせないこと。
- 特定の外部作品(MTG 等)を強調しない。

## Nexus の File credits 欄
- 原作者(hashhbbrown)を入れる。空のままにしない。
