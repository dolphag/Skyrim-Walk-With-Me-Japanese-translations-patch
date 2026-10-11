# Walk With Me – Japanese Translations Patch (source)

[日本語版 / Japanese](README.ja.md)

Source, translation table and build scripts for **Walk With Me - Japanese Translations Patch**, a Japanese
translation patch for [Walk With Me](https://www.nexusmods.com/skyrimspecialedition/mods/191283) **0.3.0**
(Skyrim SE/AE mod by hashhbbrown). The mod keeps its UI strings inside `Wayfarer.dll`, so the patch
works by modifying the DLL directly.

> **Status:** for Walk With Me **0.3.0 only** (addresses are fixed). It is not released yet.
> The 0.2.5 version of these scripts is in the first commit of this repository.
> This repository contains **no DLL and no font files**: you need your own copy of the original 0.3.0 DLL.
> The companion mod Fight With Me has its own patch tools in [`fwm/`](fwm/).

## What the patch does
- Translates the settings pages (Party / Travel / Rest / Roles / Interface / Controls), the order
  descriptions, and the descriptions on the order wheel and Party Actions (312 English → Japanese pairs,
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

- The new Party Actions tile "Battle plan" (needs the separate Fight With Me mod): its subtitle and footer description
  are translated (the Fight With Me screens themselves are patched separately, see [`fwm/`](fwm/)); the tile name stays English like the other tile names.
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
Run from the repository root. Put the **original** 0.3.0 DLL at `wwm/SKSE/Plugins/Wayfarer.dll`
(SHA-256 `a0e90379aa6a5ef952a7cf129f53ff92652758b430bb1a4cd438f9246a97b5b4`).

```
mkdir -p out
python3 -I tools/build_patch.py wwm/SKSE/Plugins/Wayfarer.dll out/Wayfarer.dll
python3 -I tools/verify.py
```

Expected output SHA-256: `4541381daed0533aa4a6ac088bfbce75de8072a8ac61b143487167a59cfa969a`

Font (needs `NotoSansJP-Medium.ttf` and the original Cinzel Decorative TTF, both SIL OFL 1.1):

```
python3 -I tools/build_font.py NotoSansJP-Medium.ttf <Cinzel ttf> font/
```

## License and credits
- The patched `Wayfarer.dll` is a modified version of Walk With Me's DLL, which is **GPL-3.0-or-later with
  additional exceptions** (see [`LICENSE`](LICENSE), [`EXCEPTIONS.md`](EXCEPTIONS.md), [`LICENSING.md`](LICENSING.md)).
  The scripts and the translation table in this repository are provided under the same terms.
  The original program source is the author's repository, tag `v0.3.0` (commit `dae2c415a8f6d98b1b1c31c23e454ebf38471cdc`):
  <https://github.com/fatalCMD/walk-with-me/tree/v0.3.0> (the author also mentions a `Walk-With-Me-0.3.0-Source.zip`, which was not
  found on the Nexus Files tab on 2026-10-11).
- Fonts: SIL OFL 1.1 (Noto Sans JP, Cinzel Decorative), full texts in [`licenses/`](licenses/).
- Many thanks to **hashhbbrown** for Walk With Me.
- The Japanese translations were produced with AI assistance (Claude, Anthropic) and checked in game.
