# -*- coding: utf-8 -*-
# Fight With Me 0.1.0 パッチ設定 (DLLアドレスは FightWithMe.dll 0.1.0 専用)

# 翻訳しないキー（表にはあるが、このDLLでは別用途と衝突するなど）
SKIP_KEYS = set()

# (キー, 参照アドレス) を個別に除外 (ImGuiのID・tween名など表示文字列ではない用途)
SKIP_SITES = {
    ('enemy', 0x9ea6d),   # tween名 "enemy" (表示ではない)
}

# 画面に出ない/対象外としてあえて訳さないキー（DLL内に存在しても無視）
NOT_TRANSLATED = {
    'No arrows': 'インライン展開(movsd)の箇所のみで、安全な置換方式が無いため原文のまま',
}

# Label/LabelWidth の1バイトずつ描画する不具合を回避するスタブ
LABEL = 0xa3b10        # Label(draw,pos,color,size,string_view*,tracking)
LABELWIDTH = 0xa38c0   # LabelWidth(size,string_view*,tracking) -> float
TEXT = 0xa40f0         # Text(draw,pos,color,size,string_view*)
TEXTSIZE = 0xa4230     # TextSize(size,string_view*) -> ImVec2 (rax)
STRCTOR = 0x1bf00      # std::string(const char*, size_t) コンストラクタ

# 近傍探索で見つからない長さ即値を手動指定: (キー, lea アドレス, 長さ即値(mov qword [m],imm32) のアドレス)
# 0xa6ba0 の関数は、4つの Why() 文字列のポインタを先にレジスタへ載せ、長さは switch の各分岐で設定する
MANUAL_LEN = [
    ('Knows no spell that heals others.',           0xa6cec, 0xa6d2e),
    ('Knows no attack spell and carries no staff.', 0xa6cf3, 0xa6d3c),
    ('Carries no bow or crossbow.',                 0xa6d01, 0xa6d4a),
    ('Carries no melee weapon.',                    0xa6cfa, 0xa6d58),
]

# 文字列長が imm8/disp8/imm32 のまま命令に埋め込まれている箇所(インライン展開された std::string::append)。
# 新しい長さが127以下なら命令長を変えずにバイトだけ書き換えられる。(キー, 命令アドレス, 種別)
EXTRA_LEN = [
    ('\nClick to send someone after them.', 0x9fb56, 'byte'),   # cmp rax, imm8
    ('\nClick to send someone after them.', 0x9fb5c, 'byte'),   # lea rax,[rcx+disp8]
    ('\nClick to send someone after them.', 0x9fb89, 'byte'),   # mov byte [rbx+disp8],0
    ('\nClick to send someone after them.', 0x9fb94, 'imm32'),  # mov qword [rsp+0x20], imm32 (増量関数の引数)
]

# 長文(16バイト超)のstd::stringがヒープ確保+コピーで展開されている領域: サイトアドレス -> (領域開始, 領域終了, 基準レジスタ, 変位)
HEAP_REGIONS = {
    0x95525: (0x95503, 0x9558a, 'rbp', -0x30),   # On: they taunt by themselves ...
    0x955c2: (0x95599, 0x95611, 'rsp', 0x50),    # On: they heal by themselves ...
    0x8e8c2: (0x8e8a3, 0x8e8da, 'rbp', 8),       # Call everyone off
}
# 領域置換後に、破壊される揮発レジスタを元の値に戻す命令 (サイトの領域開始アドレス -> 機械語, 想定する元命令)
POSTFIX = {
    0x953cb: (bytes.fromhex('488b4f10'), 'mov rcx, qword ptr [rdi + 0x10]', 0x9538d),   # 領域前で読み込んだ rcx を再読込
}

PARAGRAPH = 0xa3c70    # Paragraph(draw,pos,color,size,string_view*,width)

# 日本語の文字だけ拡大する倍率(題字は除く)。日本語は同じpxでも英字より小さく見えるため。
FONT_SCALE = 1.2
# 題字を描く Label/LabelWidth 呼び出し(YOUR PARTY / BATTLE PLAN)。拡大しない。
TITLE_CALLS = {0x8c9bb, 0x8cb88}

# DrawTip(ツールチップ)は ImGui の CalcTextSize で枠を測るため、文字だけ拡大すると枠からはみ出す。
# そこで DrawTip 内の size(15.0*s) と width(300.0*s) の係数を同じ倍率で拡大する(命令アドレス, 元の係数)。
TIP_CONSTS = [(0x8dc1f, 15.0), (0x8dc28, 300.0)]
