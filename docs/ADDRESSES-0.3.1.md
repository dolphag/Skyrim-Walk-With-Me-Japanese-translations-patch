# Walk With Me 0.3.1 のアドレス移行メモ

元 DLL: `Wayfarer.dll` 0.3.1(2,931,200 バイト)SHA-256 `8b8d398a146415d17bb659003121871a41566e109ca78c461ea3854e6cff3c40`
(0.3.0 は `a0e90379…97b5b4`)。出力 DLL(テスト版 1): `4857f0de7d601e02303daa3443b515ec1dd62b98fc0ddb676f49f15eedaf422f`。

## 方法
0.3.0 の DLL は手元になかったので、旧アドレスからの差分ではなく、**英語原文と命令の形で新 DLL から探し直した**。
- 旧版 `tier1.json` の文字列 350 件のうち、新 DLL に無いのは `^w)`(ゴミ)だけ。翻訳キー 253 件はすべて残っている。
- 0.3.1 でメニュー側に増えた文字列は `None - choose one` の 1 件だけ(ホイール側は下記)。
- `tools/tier1.py` は DLL から直接 `tier1.json` を作るようにした(旧版は xrefs.json など保存されていない中間ファイルが必要だった)。

## 対応表(0.3.0 → 0.3.1)
| 種類 | 0.3.0 | 0.3.1 |
|---|---|---|
| メニュー描画関数(T1) | c9ee0 ccc30 cdd30 ce390 cf9b0 d0910 bb750 d3430 d34f4 d36c7 d40d0 d4e70 d56a0 (+ f6ea0) | caa00 cd750 ce850 ceeb0 d04d0 d1430 bc1e0 d3f60 d4024 d41f7 d4c00 d59a0 d61d0 |
| ポインタ表(SLOTS / DESC / HINT) | 0x214280… 0x213d08… 0x2195a0… | すべて +0x1060 |
| エンブレム表 | 0x214068 | 0x2150c8 |
| ホイールの命令説明(WHEEL_LEA) | c8ac4…c8b18, c8d69 | c95c9…c961d, c9879 |
| Party Actions(ACTION_LEA) | c73b7 c73c0 c73c7 c769a c76a1 c7e30 c7e37 | c7e35 c7e3e c7e45 c814a c8151 c8925 c892c |
| fmt `{} companion{} ready` | lea c7208 / 長さ c7216 | lea c7c9a / 長さ c7ca8 |
| 拡大定数 | c8b45 c8b4e b9052 b9035 c999b | c964a c9653 b9ae2 b9ac5 ca4b9 |
| `std::string` コンストラクタ(CTOR) | 0x6000 | 0x6060 |

`tools/trans_ja.py` の INLINE(命令列を CTOR 呼び出しに置換): 領域は「`movdqa`(短い文字列)または `mov ecx,0x20`(32 バイト確保の文字列)から、次の `lea rax,[rbp+X]` の直前まで」。
結合先(`mov rdx,rax` から始まる共通部)で rdx / r8 / rcx は再設定されるので、CTOR 呼び出しで壊れても影響しない(目視確認)。

## 0.3.1 での文字列・挙動の変化(翻訳に関係するもの)
- Party Actions 下部の Hold hands の説明: `Walk hand in hand with your chosen partner in Companion mode.` →
  `Walk hand in hand in Companion style with your partner, or the nearest companion.`(訳を更新)
- Travel 設定の手をつなぐ従者のコンボ: 未選択かつ有効のとき `None - choose one`(新規。訳を追加)。
- Hold hands タイルの副表示: `Choose a partner` は消え、`Nearest companion`(訳を追加)/ `With ` + 名前 / `your partner` / `In Companion` に変わった。
  - `With ` + 名前は fmt 系の関数(0xb33f0)に前置詞と長さ 5 を渡して作る。日本語では語順が変わるので、**今回は未訳**。
  - `your partner`、`In Companion` も、出る場面を実機で見てから決める。
- 0.3.1 の Hold hands は「相手未選択なら、見ている従者、いなければ最寄りの従者」を選ぶ。設定画面の長い説明(`Only this companion is eligible...` など)は
  原文のまま変わっていないが、内容が実態とずれている可能性がある(原作側の説明の問題)。

## 触ってはいけないもの
- `0x1061d0`(Settings::Load)など INI を読む関数にも `Pathfinder` / `Loot` / `Sandbox` などの文字列がある。**T1 に入れると INI のキーが日本語になって壊れる**。
