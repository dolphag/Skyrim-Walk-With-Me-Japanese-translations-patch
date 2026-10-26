Walk With Me - Japanese Translations Patch (for Walk With Me 0.3.1)
===================================================================

Thanks to hashhbbrown for Walk With Me. Original mod:
https://www.nexusmods.com/skyrimspecialedition/mods/191283

[What it is]
A patch that translates the messages of Walk With Me into Japanese. The strings live inside the DLL, so the
patch works by modifying Wayfarer.dll directly.

[What is translated]
Settings pages (Party / Travel / Rest / Roles / Interface / Controls), the order descriptions, and the
descriptions on the order wheel and Party Actions. Mode names (Natural/Lead/Companion/Rear/Relax/Vanilla/Custom)
stay in English. Not translated: the separate mod "Fight With Me" (it has its own patch, "Fight With Me - Japanese Translations Patch"), wheel mode/tile names, HUD, notifications, companion-control window, formation
editor, logs, dialogue.

[Changes to the mod (revision points)]
1. Wayfarer.dll: strings and some text-size constants are patched (modified on 2026-10-26).
2. SKSE/Plugins/Fonts/WalkWithMeInscription.ttf is replaced by a merged font: the original Cinzel Decorative
   for Latin letters/digits and a Noto Sans JP subset (kana and the kanji used) for Japanese.
3. Wheel text sizes are enlarged because Japanese looked small there:
     order wheel center description: size cap 0.02 -> 0.028, max width 0.33 -> 0.40
     Party Actions footer description: size cap 0.02 -> 0.028, max width 0.88 -> 1.25
     bottom control hint: size cap 0.017 -> 0.024
   (Even in the original, the wheel text can look small depending on resolution/UI scale.)

[Fonts]
If the SKSE Menu Framework settings page is not displayed correctly, install the Japanese localization of SKSE Menu
Framework by 2game: https://skyrimspecialedition.2game.info/detail.php?id=120352
  SKSEMenuFramework.ini: [Fonts] PrimaryFont = NotoSansJP-Medium.ttf / EnableJapanese = true
SKSE Menu Framework only loads about 3000 common kanji; others (e.g. 祠, 壷) show as "?", so translations use
only kanji within that range.

[Install]
1. Install the original Walk With Me 0.3.1, then place this patch BELOW it (so it overwrites) and enable it.
2. Wayfarer.ini and saves are untouched. Disabling the patch restores the original.
3. For 0.3.1 only (fixed addresses). Before updating Walk With Me, DISABLE/REMOVE this patch first; otherwise its
   old Wayfarer.dll overwrites the new one and can cause errors or crashes.
Original DLL SHA-256: {ORIG_SHA}
Patched DLL SHA-256 : {OUT_SHA}

[License]
GPL-3.0-or-later (with the original exceptions): see LICENSE, EXCEPTIONS.md, LICENSING.md, ThirdParty/.
The DLL is a modified version of the original; corresponding source = this patch's source
(the GitHub repository, tag wwm-0.3.1:
https://github.com/dolphag/Skyrim-Walk-With-Me-Japanese-translations-patch/tree/wwm-0.3.1) plus the original source: the author's GitHub
https://github.com/fatalCMD/walk-with-me, main branch, commit 1ccaa82c53e65a2feaca171a6182445df4f03993 ("Walk With Me 0.3.1", 2026-10-24; the author has no 0.3.1 tag as of 2026-10-26). Fonts: SIL OFL 1.1 (LICENSES/).
Translations were produced with AI assistance (Claude, Anthropic) and checked in game. No warranty; please do
not ask the original author for support for this patch.

[Changelog] (newest first; for a new release add a "Version <version>" entry here)
* Version 0.3.1
   * Updated for Walk With Me 0.3.1 (the DLL was rebuilt; the 0.3.0 DLL does not work with 0.3.1).
   * The Hold hands description now matches 0.3.1 (with no partner chosen it picks the companion you look at, or the nearest one).
   * Translated the Hold hands tile subtitles (nearest companion / with <name> / works in Companion) and the partner list entry "None - choose one".
   * Translated the bottom control hints on the order wheel and Party Actions screens.
* Version 0.3.0-1
   * Packaging fix only. Removed the FOMOD installer, renamed README_日本語化.txt to README_Japanese.txt (ASCII-only file names) and merged the license folders, to avoid installer problems reported with Mod Organizer 2. The DLL and the translation are unchanged.
