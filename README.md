# Walk With Me – Japanese Translations Patch (source)

[日本語版 / Japanese](README.ja.md)

Source, translation table and build scripts for **Walk With Me - Japanese Translations Patch**, a Japanese
translation patch for [Walk With Me](https://www.nexusmods.com/skyrimspecialedition/mods/191283) **0.2.5**
(Skyrim SE/AE mod by hashhbbrown). The mod keeps its UI strings inside `Wayfarer.dll`, so the patch
works by modifying the DLL directly.

> **Status:** for Walk With Me **0.2.5 only** (addresses are fixed). It is not released yet.
> This repository contains **no DLL and no font files**: you need your own copy of the original 0.2.5 DLL.

## What the patch does
- Translates the settings pages (Party / Travel / Rest / Roles / Interface / Controls), the order
  descriptions, and the descriptions on the order wheel and Party Actions (309 English → Japanese pairs,
  see [`translations_en_ja.csv`](translations_en_ja.csv)).
- Replaces `SKSE/Plugins/Fonts/WalkWithMeInscription.ttf` with a merged font: the original Cinzel Decorative
  for Latin letters/digits (so mode names such as "Natural" keep their look) plus a Noto Sans JP subset for
  kana and the kanji used by the translation. The family is renamed to avoid the Reserved Font Name "Cinzel".
- Enlarges a few wheel texts, because Japanese looked small there (all are constants inside the DLL):

  | Text | Change |
  |---|---|
  | Order wheel center description | size cap 0.02 → 0.028 (×1.4), max width 0.33 → 0.40 |
  | Party Actions footer description | size cap 0.02 → 0.028, max width 0.88 → 1.25 |
  | Bottom control hint (Click / arrows …) | size cap 0.017 → 0.024 |

- Not translated: wheel mode/tile names, HUD, notifications, companion-control window, formation editor,
  logs, dialogue (embedded in code or not safely replaceable). Mode names (Natural/Lead/…) stay English.

Terms follow the Fandom wiki list of the official Japanese Skyrim translation
([link](https://elderscrolls.fandom.com/ja/wiki/The_Elder_Scrolls_V:_%E3%82%B9%E3%82%AB%E3%82%A4%E3%83%AA%E3%83%A0%E5%85%AC%E5%BC%8F%E6%97%A5%E6%9C%AC%E8%AA%9E%E8%A8%B3%E4%B8%80%E8%A6%A7);
a fan-made extraction, not an official site).

## Repository layout
| Path | Purpose |
|---|---|
| `tools/trans_ja.py` | translation tables, patch sites (addresses) and constants |
| `tools/build_patch.py` | applies the patch to the original DLL; writes `changes.json` and the output DLL |
| `tools/verify.py` | checks every changed byte is logged and every retargeted reference lands in the new section |
| `tools/build_font.py` | builds the merged font |
| `tools/tier1.py`, `tier1.json` | string classification used by the builder |
| `tools/dis.py`, `tools/dis2.py` | disassembly helpers (analysis only) |
| `translations_en_ja.csv` | English → Japanese pairs (UTF-8 with BOM, header row) |

## How the patch works (short)
A new data-only section (`.jpn`) holds the Japanese strings and some float constants. Then, per kind of site:
`lea reg,[rip+disp]` string references are retargeted; pointer tables in `.rdata` are rewritten
(relocation-checked); inline-copied `std::string` constructions are replaced by a call to the existing string
constructor; `fmt` string_view length immediates are patched; `movss/mulss` constants are retargeted for text size.
Only NUL-terminated or length-patched consumers are touched.

## Reproduce (Python 3.11+, `pip install pefile capstone fonttools`)
Run from the repository root. Put the **original** 0.2.5 DLL at `wwm/SKSE/Plugins/Wayfarer.dll`
(SHA-256 `46cde5e6dc3df778c356e8de493ec6c22720444e8f16ee79516a6d12dcaca15a`).

```
mkdir -p out
python3 -I tools/build_patch.py wwm/SKSE/Plugins/Wayfarer.dll out/Wayfarer.dll
python3 -I tools/verify.py
```

Expected output SHA-256: `a0463f07879c888d48be3e93f6ddfc4cb7cfe5be4695900dc47c84903d1e9ac9`

Font (needs `NotoSansJP-Medium.ttf` and the original Cinzel Decorative TTF, both SIL OFL 1.1):

```
python3 -I tools/build_font.py NotoSansJP-Medium.ttf <Cinzel ttf> font/
```

## License and credits
- The patched `Wayfarer.dll` is a modified version of Walk With Me's DLL, which is **GPL-3.0-or-later with
  additional exceptions** (see [`LICENSE`](LICENSE), [`EXCEPTIONS.md`](EXCEPTIONS.md), [`LICENSING.md`](LICENSING.md)).
  The scripts and the translation table in this repository are provided under the same terms.
  The original program source is the author's `Walk-With-Me-0.2.5-Source.zip` on the mod's Files tab.
- Fonts: SIL OFL 1.1 (Noto Sans JP, Cinzel Decorative), full texts in [`licenses/`](licenses/).
- Many thanks to **hashhbbrown** for Walk With Me.
- The Japanese translations were produced with AI assistance (Claude, Anthropic) and checked in game.
