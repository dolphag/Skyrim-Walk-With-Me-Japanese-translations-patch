# Walk With Me – Japanese Translations Patch (source)

[日本語版 / Japanese](README.ja.md)

Source, translation table and build scripts for **Walk With Me - Japanese Translations Patch**, a Japanese
translation patch for [Walk With Me](https://www.nexusmods.com/skyrimspecialedition/mods/191283) **0.3.1**
(Skyrim SE/AE mod by hashhbbrown). The mod keeps its UI strings inside `Wayfarer.dll`, so the patch
works by modifying the DLL directly.

> **Status:** released on Nexus Mods. This repository contains **no DLL and no font files**: you need your own copy of the original DLL.
> The companion mod Fight With Me has its own repository: <https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch>.

| Patch | For mod version | Source (tag) | Original DLL SHA-256 → patched DLL SHA-256 |
|---|---|---|---|
| Walk With Me patch **0.3.1** | Walk With Me 0.3.1 | repository root, tag [`wwm-0.3.1`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.3.1) | `8b8d398a…3c40` → `577dca9f…88e5` |
| Walk With Me patch **0.3.0** | Walk With Me 0.3.0 | repository root, tag [`wwm-0.3.0`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.3.0) | `a0e90379…97b5b4` → `4541381d…969a` |
| Walk With Me patch **0.2.5** | Walk With Me 0.2.5 | [`wwm-0.2.5/`](wwm-0.2.5/), tag [`wwm-0.2.5`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.2.5/wwm-0.2.5) | `46cde5e6…caca15a` → `a0463f07…1e9ac9` |
| Fight With Me patch **0.1.0** | Fight With Me 0.1.0 | this repository's tag [`fwm-0.1.0`](https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/fwm-0.1.0/fwm) | `23b99b6b…35bc32d` → `059d0785…aae47` |

The Nexus packages `0.3.0-1`, `0.2.5-1` and `0.1.0-1` differ from the versions above only in packaging (no FOMOD, ASCII-only file names, one `LICENSES/` folder); the DLLs are byte-identical, so the tags above still apply.

The text below describes the **0.3.1** tools in the repository root. The 0.2.5 snapshot lives in [`wwm-0.2.5/`](wwm-0.2.5/) (run its commands from that folder).

## What the patch does
- Translates the settings pages (Party / Travel / Rest / Roles / Interface / Controls), the order
  descriptions, and the descriptions on the order wheel and Party Actions (320 English → Japanese pairs,
  see [`translations_en_ja.csv`](translations_en_ja.csv)).
- Replaces `SKSE/Plugins/Fonts/WalkWithMeInscription.ttf` with a merged font: the original Cinzel Decorative
  for Latin letters/digits (so mode names such as "Natural" keep their look) plus a Noto Sans JP subset for
  kana and the kanji used by the translation. The family is renamed to avoid the Reserved Font Name "Cinzel".
- Enlarges a few wheel texts, because Japanese looked small there (all are constants inside the DLL):

  | Text | Change |
  |---|---|
  | Order wheel center description | size cap 0.02 → 0.028 (×1.4), max width 0.33 → 0.40 |
  | Party Actions footer description | size cap 0.02 → 0.028, max width 0.88 → 1.25 |
  | Bottom control hint | size cap 0.017 → 0.024 |

- The new Party Actions tile "Battle plan" (needs the separate Fight With Me mod): its subtitle and footer description
  are translated (the Fight With Me screens themselves are patched separately, see the Fight With Me repository); the tile name stays English like the other tile names.
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
Run from the repository root. Put the **original** 0.3.1 DLL at `wwm/SKSE/Plugins/Wayfarer.dll`
(SHA-256 `8b8d398a146415d17bb659003121871a41566e109ca78c461ea3854e6cff3c40`).

```
mkdir -p out
python3 -I tools/build_patch.py wwm/SKSE/Plugins/Wayfarer.dll out/Wayfarer.dll
python3 -I tools/verify.py
```

Expected output SHA-256: `577dca9fd583d7ff2ddcd1b02e131a4cd8bc2f56de910b626b6fea6a97b188e5`

Font (needs `NotoSansJP-Medium.ttf` and the original Cinzel Decorative TTF, both SIL OFL 1.1):

```
python3 -I tools/build_font.py NotoSansJP-Medium.ttf <Cinzel ttf> font/
```

## License and credits
- The patched `Wayfarer.dll` is a modified version of Walk With Me's DLL, which is **GPL-3.0-or-later with
  additional exceptions** (see [`LICENSE`](LICENSE), [`EXCEPTIONS.md`](EXCEPTIONS.md), [`LICENSING.md`](LICENSING.md)).
  The scripts and the translation table in this repository are provided under the same terms.
  The original program source is the author's repository, `main` branch, commit `1ccaa82c53e65a2feaca171a6182445df4f03993` ("Walk With Me 0.3.1", 2026-10-24):
  <https://github.com/fatalCMD/walk-with-me/tree/1ccaa82c53e65a2feaca171a6182445df4f03993> (the author has no `v0.3.1` tag as of 2026-10-26; the 0.3.0 source is the tag `v0.3.0`, commit `dae2c415a8f6d98b1b1c31c23e454ebf38471cdc`).
- Fonts: SIL OFL 1.1 (Noto Sans JP, Cinzel Decorative), full texts in [`licenses/`](licenses/).
- Many thanks to **hashhbbrown** for Walk With Me.
- The Japanese translations were produced with AI assistance (Claude, Anthropic) and checked in game.
