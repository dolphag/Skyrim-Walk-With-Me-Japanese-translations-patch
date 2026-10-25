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
4. README(日本語は `README.ja.md`、英語は `README.md`)、翻訳表 CSV、元 DLL / 出力 DLL の SHA-256 を更新する。
5. zip を作る(構成は下記)。
6. Nexus 用テキスト(更新履歴・説明・クレジット欄)を作る。
7. **main へ統合 → main の HEAD を確認 → ユーザーがそのコミットにタグ**(`wwm-<版>` の形式)。タグは GitHub の Release で、ユーザーが付ける。
8. ユーザーが Nexus にアップロードしたら、ブラウザで開いて確認する(版、ファイル名、サイズ、説明、File credits 欄)。

## zip の構成(0.3.0-1 以降の方針)
- FOMOD なし、ASCII のファイル名、ライセンス文書は `LICENSES/` 1 フォルダにまとめる。
- 構成は**前回の配布 zip(0.3.0-1)を実物で確認して踏襲する**(この節は要確認)。含まれるもの: パッチ済み `Wayfarer.dll`、置き換えフォント(`SKSE/Plugins/Fonts/WalkWithMeInscription.ttf`)、README(日本語・英語)、ライセンス文書(原作の配布物のものをそのまま + フォントの OFL)。0.3.0 の元の作業 zip には `ThirdParty/` の依存ライブラリのライセンス一式も含まれていた。
- zip は Python の `zipfile` で作る(パス区切りと改行を揃える)。

## README / Nexus 文面に必ず入れること
- 原作者クレジット(hashhbbrown)、原 MOD へのリンク、権限の確認日。
- 元 DLL と出力 DLL の SHA-256。他版には使わないこと。更新時は先にパッチを外すこと。
- ライセンス(GPL-3.0-or-later と例外、フォントは OFL)と、原作のソースへのリンク。
- 「GitHub にはソースのみ、バイナリは Nexus のみ」。AI 利用の開示。非公式で、原作者に問い合わせないこと。
- 特定の外部作品(MTG 等)を強調しない。

## Nexus の File credits 欄
- 原作者(hashhbbrown)を入れる。空のままにしない。
