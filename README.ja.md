# Walk With Me - Japanese Translations Patch(ソース)

[English](README.md)

[Walk With Me](https://www.nexusmods.com/skyrimspecialedition/mods/191283) **0.3.1**(作者 hashhbbrown)の
日本語化パッチ「Walk With Me - Japanese Translations Patch」のソース、翻訳対応表、ビルドスクリプトです。
文字列が `Wayfarer.dll` 内にあるため、DLLを直接パッチする方式です。

> **状態**: Nexus Mods で公開済み。このリポジトリには **DLLもフォントも含みません**。元のDLLは各自で用意してください。
> 姉妹MOD Fight With Me の日本語化ツールは、専用のリポジトリにあります: <https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch>。

| パッチ | 対象MODの版 | ソース(タグ) | 元DLL SHA-256 → パッチ後DLL SHA-256 |
|---|---|---|---|
| Walk With Me パッチ **0.3.1** | Walk With Me 0.3.1 | リポジトリ直下、タグ [`wwm-0.3.1`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.3.1) | `8b8d398a…3c40` → `577dca9f…88e5` |
| Walk With Me パッチ **0.3.0** | Walk With Me 0.3.0 | リポジトリ直下、タグ [`wwm-0.3.0`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.3.0) | `a0e90379…97b5b4` → `4541381d…969a` |
| Walk With Me パッチ **0.2.5** | Walk With Me 0.2.5 | [`wwm-0.2.5/`](wwm-0.2.5/)、タグ [`wwm-0.2.5`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.2.5/wwm-0.2.5) | `46cde5e6…caca15a` → `a0463f07…1e9ac9` |
| Fight With Me パッチ **0.1.0** | Fight With Me 0.1.0 | このリポジトリのタグ [`fwm-0.1.0`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/fwm-0.1.0/fwm) | `23b99b6b…35bc32d` → `059d0785…aae47` |

Nexusの配布物 `0.3.0-1`・`0.2.5-1`・`0.1.0-1` は、上の各版と梱包だけが違います(FOMOD廃止、ASCIIのみのファイル名、`LICENSES/` を1つに統合)。DLLは同一なので、上のタグがそのまま対応します。

以下の説明は、リポジトリ直下の **0.3.1** 用ツールについてです。0.2.5 は [`wwm-0.2.5/`](wwm-0.2.5/) にあります(コマンドはそのフォルダで実行)。

## 内容
- 設定ページ、命令の説明、命令ホイール/Party Actions の説明文を日本語化(320組、[`translations_en_ja.csv`](translations_en_ja.csv))。
- `SKSE/Plugins/Fonts/WalkWithMeInscription.ttf` を合成フォントに差し替え(英数字は元の Cinzel Decorative、
  かなと訳文に使う漢字は Noto Sans JP のサブセット)。予約名「Cinzel」を避けるため内部名を変更しています。
- Party Actions の新タイル「Battle plan」(別MOD Fight With Me が必要)は、副題と下部の説明を日本語化(タイル名は他のタイルと同様に英語のまま)。Fight With Me 側の画面は別パッチです(別リポジトリ)。
- 日本語だと小さく見えたホイール内の文字を拡大(いずれもDLL内の定数):

  | 文字 | 変更 |
  |---|---|
  | 命令ホイール中央の説明 | サイズ上限 0.02→0.028(約1.4倍)、最大幅 0.33→0.40 |
  | Party Actions 下部の説明 | サイズ上限 0.02→0.028、最大幅 0.88→1.25 |
  | 下端の操作ヒント | サイズ上限 0.017→0.024 |

- 日本語化していないもの: ホイールのモード名・タイル名、HUD、通知、従者制御ウィンドウ、隊列エディタ、ログ、会話文など。

用語は Fandom Wiki「スカイリム公式日本語訳一覧」(ファンによる抽出で、公式サイトではありません)に合わせています。

## 再現手順
英語版 README の "Reproduce" を参照してください。元DLLの SHA-256 は
`8b8d398a146415d17bb659003121871a41566e109ca78c461ea3854e6cff3c40`、出力DLLは
`577dca9fd583d7ff2ddcd1b02e131a4cd8bc2f56de910b626b6fea6a97b188e5` になります。

## ライセンス・謝辞
- パッチ後の `Wayfarer.dll` は、GPL-3.0-or-later(追加の例外つき)の原作DLLの改変版です。スクリプトと対応表も同条件で
  提供します([`LICENSE`](LICENSE)、[`EXCEPTIONS.md`](EXCEPTIONS.md)、[`LICENSING.md`](LICENSING.md))。
  元のソースは、原作者のリポジトリの main ブランチ、コミット `1ccaa82c53e65a2feaca171a6182445df4f03993`("Walk With Me 0.3.1"、2026-10-24)です:
  <https://github.com/fatalCMD/walk-with-me/tree/1ccaa82c53e65a2feaca171a6182445df4f03993>(2026-10-26時点で `v0.3.1` のタグはありません。0.3.0 のソースはタグ `v0.3.0`、コミット `dae2c415a8f6d98b1b1c31c23e454ebf38471cdc`)。
- 原MODの配布権限(Nexus の Permissions and credits)を 2026-10-26 に確認しました。原作者のクレジット表示を条件に、改変と再配布が許可されています。
- フォントは SIL OFL 1.1([`licenses/`](licenses/))。
- 原作者 hashhbbrown さんに感謝します。
- 訳文はAI(Claude, Anthropic)の支援で作成し、ゲーム内で動作確認しています。
