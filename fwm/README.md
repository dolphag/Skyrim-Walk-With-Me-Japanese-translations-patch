# Fight With Me - Japanese Translations Patch (tools and translation table)

[日本語は下](#日本語)

Scripts and the translation table for the Japanese translation patch for
[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.1.0** (by hashhbbrown).
The patched `FightWithMe.dll` is distributed **only on Nexus Mods** (as a translation of the original page),
following the permissions on the original page. **This repository contains no DLL and no code of Fight With Me**:
only the scripts that patch a DLL you own, and the English → Japanese table (377 pairs).

- Original DLL SHA-256: `23b99b6b446ce84b49175e9fab7d68fa81d8b2f8f18c8e451d9d5f87d35bc32d`
- Expected output SHA-256: `059d0785c0fe8b52cdb0fdc7c1116f1cdb5bb114ca0fa1295972e66ad05aae47`
- Original source (for reference): <https://github.com/fatalCMD/fight-with-me> (commit `383c26892183b4a0e6b71a937802003287d28480`)

## How it works (short)
A new section (`.jpn`, read+execute) holds the Japanese strings and a few stubs. `lea reg,[rip+disp]` references,
`.rdata` pointer slots (relocation-checked) and fmt length immediates are retargeted; inline-expanded
`std::string` constructions are replaced by a call to the string constructor (register liveness is checked).
Label/LabelWidth draw one byte at a time and break UTF-8, so calls are redirected to stubs that use Text/TextSize
when the string contains non-ASCII bytes; Japanese text is enlarged by `FONT_SCALE` (1.2) except for the title,
and the tooltip's size/width constants are scaled together so its box fits.

## Reproduce (Python 3.11+, `pip install pefile capstone unicorn`)
```
python3 -I tools/fwm_fmtcheck.py                                  # format-string field check
python3 -I tools/fwm_patch.py FightWithMe.dll out.dll report.json   # original DLL -> patched DLL
python3 -I tools/fwm_verify.py FightWithMe.dll out.dll              # independent static verification
python3 -I tools/fwm_emu_stub.py out.dll report.json                # dispatch/scale check of the stubs (unicorn)
```

## Notes
- For 0.1.0 only (addresses are fixed).
- Translations were produced with AI assistance (Claude, Anthropic) and checked in game.
- The scripts and the table are provided under GPL-3.0-or-later, like the rest of this repository.

## 日本語
[Fight With Me](https://www.nexusmods.com/skyrimspecialedition/mods/194766) **0.1.0** の日本語化パッチのスクリプトと翻訳表です。
パッチ済みの `FightWithMe.dll` は、原MODページの権限表示に従い、**Nexus Mods(原MODの翻訳ページ)でのみ**配布します。
**このリポジトリには、DLLも Fight With Me のコードも含みません**。手元のDLLにパッチを当てるスクリプトと、英日対応表(377組)だけです。
再現手順は上の英語の節を参照してください。元DLLの SHA-256 は `23b99b6b446ce84b49175e9fab7d68fa81d8b2f8f18c8e451d9d5f87d35bc32d`、
出力DLLは `059d0785c0fe8b52cdb0fdc7c1116f1cdb5bb114ca0fa1295972e66ad05aae47` になります。
