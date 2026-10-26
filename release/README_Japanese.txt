Walk With Me - Japanese Translations Patch (対象: Walk With Me 0.3.0)
=====================================================================

原作者 hashhbbrown さんへ: 素晴らしいMODを公開してくださり、ありがとうございます。
このパッチは、日本語環境でも Walk With Me を快適に使えるように、感謝を込めて作ったものです。
原MOD: https://www.nexusmods.com/skyrimspecialedition/mods/191283

■ 内容
Walk With Meの各種メッセージを日本語にするパッチです。文字列がDLL内にあるため、これをパッチする形式です。

■ 訳語について
用語は、下記のFandom Wiki「スカイリム公式日本語訳一覧」に合わせています。
https://elderscrolls.fandom.com/ja/wiki/The_Elder_Scrolls_V:_%E3%82%B9%E3%82%AB%E3%82%A4%E3%83%AA%E3%83%A0%E5%85%AC%E5%BC%8F%E6%97%A5%E6%9C%AC%E8%AA%9E%E8%A8%B3%E4%B8%80%E8%A6%A7
(同ページはBethesda/ZeniMax公式のサイトではありません。)

一覧にない用語として、パーティ、隊列、テレポート、サンドボックス、探索(Loot scouting → 戦利品探索)などは一般的なカタカナ/和語です。
モード名(Natural/Lead/Companion/Rear/Relax/Vanilla/Custom)は英語のままです。

■ フォント
SKSE Menu Framework の設定ページが正しく表示されない場合は 2game 様の日本語化ファイルの導入が必要です。
https://skyrimspecialedition.2game.info/detail.php?id=120352
  SKSEMenuFramework.ini: [Fonts] PrimaryFont = NotoSansJP-Medium.ttf / EnableJapanese = true

ホイール/HUDはこのMOD専用の WalkWithMeInscription.ttf(Cinzel Decorative)で描画されますが、日本語の字形が
ないため、SKSE/Plugins/Fonts/WalkWithMeInscription.ttf を差し替えています。内容は次の合成フォントです。
  ・英字・数字 = 元のCinzel Decorative(Natural 等の見た目は変わりません)
  ・かな・記号・訳文で使う漢字(約800字) = Noto Sans JP Medium のサブセット

Noto全体を入れないのは、SMF3が各フォントを日本語グリフ約3000字ぶん読み込むため、重複するとテクスチャが
肥大化するおそれがあるためです。元の見た目に戻す場合は、このファイルを削除して元MODのフォントを復元し、
Wayfarer.dll も差し替え前のものに戻してください(日本語の説明は「?」になります)。
ライセンス: どちらのフォントもSIL OFL 1.1です(LICENSES/ に全文)。合成にあたり、予約フォント名
「Cinzel」を避けて内部名を「Walk With Me Inscription JP」に変更しています。

■ ホイールの文字サイズ
日本語だと小さく見えたため、次の文字を大きくしています(いずれもDLL内の定数。他の文字は変えていません)。
  ・命令ホイール中央の説明: サイズ上限 約1.4倍(0.02→0.028)、最大幅 0.33→0.40
  ・Party Actions 下部の説明: サイズ上限 約1.4倍(0.02→0.028)、最大幅 0.88→1.25
  ・下端の操作ヒント(Click / arrows: ... など): サイズ上限 約1.4倍(0.017→0.024)
Party Actions のタイル副題の大きさは変えていません。

■ 漢字の制限
SKSE Menu Framework は日本語グリフを ImGui 標準の約3000字(GetGlyphRangesJapanese)に限定しており、範囲外の漢字
(祠・壷・梱・繋など)は「?」になります。訳文は範囲内の漢字だけを使っています。

■ 導入
1. 元の Walk With Me 0.3.0 を導入した状態で、このMODを元より下(後勝ち)に置いて有効化。
2. Wayfarer.ini とセーブには影響しません。無効化すれば元に戻ります。
3. 対象は 0.3.0 のみ(アドレス固定のパッチ)です。
元DLL SHA-256 : {ORIG_SHA}
パッチ後DLL   : {OUT_SHA}

■ 日本語化していないもの
- ホイールのモード名・タイル、HUD、Party actions、従者制御ウィンドウ、隊列エディタの文字列
  (コード内に埋め込みのため安全に差し替えられない)、通知メッセージ、ログ、ESP、会話文。
  ホイールで日本語化したのは「説明文」のみです(命令ホイール中央の説明7種、Party Actions のタイルの副題と
  下部の説明)。タイル名・見出し・モード名は英語のままです。
  Party Actions のうち次は英語のままです: "With <相手の名前>"、"In Companion"、"Available in game"、
  "Walk With Me is disabled"、"ACTIVE ORDER / ..."、操作ヒント(Click / 1-7: order ... など)。
- 別MOD「Fight With Me」の画面は本パッチの対象外です。日本語化は別ページ「Fight With Me - Japanese Translations Patch」で提供します(Party Actions の「Battle plan」タイルの副題と説明は、本パッチで日本語になります)。
- 英語のまま: ページ名、Classic/TETHER/Nearest、"Unbound"(キー割り当て欄)、"Press a key or chord..."、
  "Selected companion"、" at "、" (not nearby)"。

■ ライセンスと改変の告知(GPL-3.0-or-later)
- 本パッチの Wayfarer.dll は、Walk With Me 0.3.0 の Wayfarer.dll(GPL-3.0-or-later、追加の例外つき)を
  2026-10-11 に改変した派生物です。改変内容: 文字列と一部の描画定数のバイナリパッチ、および
  SKSE/Plugins/Fonts/WalkWithMeInscription.ttf の差し替え(日本語グリフの追加)。
- 本パッチ全体も GPL-3.0-or-later で提供します。全文は LICENSE、原作者が付した例外は EXCEPTIONS.md と
  LICENSING.md、第三者の通知は ThirdParty/ にあります(原MOD同梱のものをそのまま収録)。
- 無保証です。本パッチの不具合を原作者に問い合わせないでください。
- 対応ソース(Corresponding Source)は次の2つです。
  1. 本パッチのソース: GitHub のタグ wwm-0.3.0
     https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.3.0
     翻訳表、パッチ生成スクリプト、フォント生成スクリプト、検証スクリプト、再現手順(README.md)を含みます。
  2. 元DLLのソース: 原作者のGitHub https://github.com/fatalCMD/walk-with-me のタグ v0.3.0
     (コミット dae2c415a8f6d98b1b1c31c23e454ebf38471cdc)。元DLL SHA-256 が上記と一致するものが対象です。
     (原作者は同梱の Walk-With-Me-0.3.0-Source.zip の提供を述べていますが、2026-10-11時点で原MODのFilesタブには
     見当たらないため、GitHubを参照先としています。)
- 同梱フォントは SIL OFL 1.1(LICENSES/)。Noto Sans JP と Cinzel Decorative の派生で、予約名「Cinzel」は
  使っていません。

■ 翻訳について
訳文はAI(Claude, Anthropic)の支援で作成し、ゲーム内で作者が動作確認し、修正を重ねています。
誤訳や不自然な表現があれば、Nexusのコメントでお知らせください。

■ 注意
- 対象は Walk With Me 0.3.0 のみです。他のバージョンには使わないでください。
- Walk With Me を更新するときは、先に本パッチを無効化(削除)してください。古い Wayfarer.dll が新しい版を上書きし、不具合やクラッシュの原因になります。
- 設定ページの表示には、SKSE Menu Framework 側で日本語フォント(Noto Sans JP)の設定が必要です(上記「フォント」)。

■ 更新履歴(最新を先頭に。新しい版では、ここに「Version <版>」の項を追加する)
* Version 0.3.0-1
   * 梱包のみの修正です。MO2でのインストール時の不具合報告を受け、FOMODを廃止し、ファイル名をASCIIのみにし、ライセンスのフォルダを1つにまとめました。DLLと訳文は変更していません。
