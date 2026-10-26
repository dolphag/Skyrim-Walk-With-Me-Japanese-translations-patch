# -*- coding: utf-8 -*-
# Walk With Me 0.3.1 設定メニュー日本語訳（英語原文 -> 日本語）
# 方針: ページ名(Party/Travel/Roles/...)、モード名(Natural/Lead/Companion/Rear/Relax/Vanilla/Custom)、
#       Classic/TETHER/Nearest、NFF/OAR/FPI などの固有名はホイール・ツリー側が英語のままなので原文を保つ。
T = {
# ---- Party ----
"Nearby recruited followers appear here. Add companions here or through dialogue.":
 "近くにいる従者がここに表示されます。従者はここ、または会話から追加できます。",
"No recruited followers detected nearby.": "近くに従者は見つかりません。",
"Companion": "従者",
"Status": "状態",
"Personality": "性格",
"Manage": "管理",
"Travel control imported": "移動制御を取り込み済み",
"Added manually": "手動で追加",
"Managed by integration": "連携MODが管理",
"Added automatically": "自動で追加",
"Not added": "未追加",
"Control": "制御",
"Remove": "除外",
"Add": "追加",
"Open this companion's travel control popup.": "この従者の移動制御ポップアップを開きます。",
"This registration is owned by another integration.": "この登録は別の連携MODが管理しています。",
"Release Walk With Me's control and prevent automatic re-addition. This does not dismiss the follower.":
 "Walk With Meの制御を解除し、自動での再追加を防ぎます。従者を解散させるわけではありません。",
"Allow Walk With Me to direct this companion's travel and relaxation. Works for any follower, whatever recruited them, and in any travel style. The choice is saved and can be removed here or in dialogue.":
 "この従者の移動と休憩をWalk With Meが制御するようにします。誰が仲間にした従者でも、どの移動スタイルでも有効です。選択は保存され、ここまたは会話から解除できます。",
"Setting": "設定項目",
"Value": "値",
"Allow Walk With Me to manage the party.": "Walk With Meにパーティの管理を任せます。",
"Enable Walk With Me": "Walk With Meを有効にする",
"COMPANIONS": "従者一覧",
"Companion control...": "従者の制御...",
"Open a separate window to explicitly manage a nearby custom companion's travel or release a previous import.":
 "別ウィンドウを開き、近くのカスタム従者の移動を明示的に管理するか、以前の取り込みを解除します。",
"Enrollment": "登録",
"Maximum managed companions.": "管理する従者の最大数。",
"Companion limit": "従者の上限",
"Add recruited followers as they load nearby. Removed companions remain excluded. Manual Add still works.":
 "従者が近くでロードされたときに自動で追加します。除外した従者は対象外のままです。手動の追加も引き続き使えます。",
"Automatically add followers": "従者を自動で追加",
"Include active NFF followers in automatic enrollment.": "有効なNFF従者を自動登録の対象に含めます。",
"Include NFF followers": "NFF従者を含める",
"Include recruited custom teammates in automatic enrollment. Detection is not a compatibility guarantee.":
 "仲間にしたカスタム従者を自動登録の対象に含めます。検出はMODとの互換性を保証するものではありません。",
"Include custom followers": "カスタム従者を含める",
# ---- Travel ----
"Formation": "隊列",
"Default travel style": "既定の移動スタイル",
"Distance between travelling companions. Larger values spread them out; interiors and narrow paths still constrain space. Changes take effect immediately.":
 "移動中の従者どうしの間隔。大きいほど広がります。屋内や狭い道では引き続き空間の制約を受けます。変更は即座に反映されます。",
"Spacing": "間隔",
"Adjust spacing": "間隔を調整",
"Tighten": "狭める",
"Spread out": "広げる",
"Extra setback for one or two Natural-mode companions. Their mutual spacing stays normal. The choice stays stable while travelling; zero disables stragglers.":
 "Naturalモードの従者1〜2人に追加で与える後方へのずれ。互いの間隔は通常のままです。移動中は同じ選択が維持されます。0にすると遅れがちな従者は出ません。",
"%.0f units": "%.0f ユニット",
"Straggler distance": "遅れ距離",
"Custom formation": "カスタム隊列",
"Name": "名前",
"What the formation is called on the party wheel, the orders HUD and here.":
 "パーティホイール、命令HUD、およびここで表示される隊列の名前。",
"Emblem": "エンブレム",
"The icon shown for the formation on the party wheel and the orders HUD.":
 "パーティホイールと命令HUDで隊列に表示されるアイコン。",
"Places": "配置",
"Draw where each companion walks, and optionally who stands where. It appears on the party wheel once saved.":
 "各従者が歩く位置を描き、必要なら誰がどこに立つかも指定します。保存するとパーティホイールに表示されます。",
" place": " か所",
" places": " か所",
"None yet": "まだありません",
"Edit formation": "隊列を編集",
"Create formation": "隊列を作成",
"Open the formation editor.": "隊列エディタを開きます。",
"Load a save first; the editor lists your party.": "先にセーブをロードしてください。エディタにはパーティが一覧表示されます。",
"Catch-up & teleport": "追いつきとテレポート",
"Lower values close gaps more quickly.": "小さいほど早く距離を詰めます。",
"%.1f s": "%.1f 秒",
"%.2f s": "%.2f 秒",
"%.0f s": "%.0f 秒",
"Catch-up response": "追いつきの反応",
"Normal catch-up limit. Distant companions use twice this value, then ease back to your pace.":
 "通常時の追いつき速度の上限。離れた従者はこの2倍まで出し、その後あなたのペースに戻ります。",
"Catch-up speed cap": "追いつき速度の上限",
"Beyond this player distance, catch-up uses twice your selected speed cap.":
 "プレイヤーからこの距離を超えると、追いつき速度の上限が設定値の2倍になります。",
"Distant boost starts": "遠距離ブースト開始",
"The boost ends inside this distance. Separate thresholds prevent repeated speed switching.":
 "この距離の内側に入るとブーストが終わります。しきい値を分けることで、速度の切り替えが繰り返されるのを防ぎます。",
"Normal pace within": "通常ペースに戻る距離",
"Bring companions back after two seconds far away, or three seconds left in another cell. Works while you ride, sneak, fight, sit, craft or stand still, and pulls a companion out of a chair or bed if need be. Lands them behind you, then on your trail, then anywhere reachable nearby. Waiting, fighting, riding and scripted companions stay put, and so does everyone in Sovngarde, Skuldafn, Apocrypha, the Soul Cairn and the Underforge.":
 "遠く離れて2秒、または別のセルに置き去りにして3秒たつと、従者を呼び戻します。騎乗、隠密、戦闘、着席、クラフト、立ち止まりのいずれの最中でも動作し、必要なら椅子やベッドから従者を引き離します。着地先は、あなたの背後、次に通ってきた道筋、それも無理なら近くの到達可能な場所の順です。待機中・戦闘中・騎乗中・スクリプト制御中の従者はその場に残り、ソブンガルデ、スクルダフン、アポクリファ、ソウル・ケルン、アンダーフォージにいる全員も同様です。",
"Teleport distant companions": "離れた従者をテレポート",
"Distance from you before teleport catch-up. Each companion has an 8-second cooldown.":
 "テレポートで追いつく前の、あなたからの距離。従者ごとに8秒のクールダウンがあります。",
"Teleport beyond": "テレポートする距離",
"During a Relax order, companions keep their camp however far you go: nothing teleports them, NFF included. Off: they catch up like everyone else and relax wherever they land. Temporary rest never holds anyone back.":
 "Relax命令の間、あなたがどれだけ離れても従者は野営地に留まります。NFFを含め、誰もテレポートされません。オフ：他の従者と同様に追いつき、着いた先で休憩します。一時休憩では誰も引き止められません。",
"Leave relaxing companions in place": "休憩中の従者を置いていく",
"While Walk With Me teleports, it also teleports NFF's own followers and parks NFF's Catch Up timer, so the two never race and a Relax camp stays put. NFF's value is put back before every save, while the journal is open, and whenever this is off. Nothing changes if NFF's Catch Up is off.":
 "Walk With Meがテレポートを行うとき、NFF自身の従者もテレポートし、NFFのCatch Upタイマーを停止します。これにより両者が競合せず、Relaxの野営地も保たれます。NFFの値は、セーブの前、日記を開いている間、およびこの設定がオフのときは元に戻されます。NFFのCatch Upがオフなら何も変わりません。",
"Take over NFF's catch-up": "NFFの追いつきを引き継ぐ",
"Movement tuning": "移動の調整",
"How far ahead the party predicts your route.": "パーティがあなたの進路をどれだけ先まで予測するか。",
"Anticipation": "先読み",
"Take short, bounded detours around rocks while traveling nearby in the wilderness. Towns, interiors and distant catch-up use normal pathfinding. If a local detour fails, keep the native travel route. Hand-holding uses its own collision checks.":
 "荒野を近距離で移動するとき、岩などを避ける短い迂回をします。街、屋内、遠距離の追いつきには通常の経路探索を使います。迂回に失敗した場合は標準の移動ルートを維持します。手つなぎは独自の衝突判定を使います。",
"Avoid obstacles ahead": "前方の障害物を避ける",
"Wait briefly before following a new direction, ignoring little zigzags and softening side steps. Real reversals respond sooner. Zero restores immediate steering. Does not affect Vanilla mode.":
 "新しい方向に従う前に少し待ち、細かいジグザグを無視して横歩きを和らげます。本当の方向転換にはより早く反応します。0で即時の操舵に戻ります。Vanillaモードには影響しません。",
"Turn response delay": "方向転換の反応遅延",
"Each companion has their own reaction time, turn response and comfortable pace. They let a small gap grow, then catch up. Higher values make the party less synchronized; zero restores shared movement. Large gaps still recover promptly. Does not affect Vanilla or sandboxing.":
 "従者ごとに反応時間、方向転換の反応、心地よいペースが異なります。少しの距離は開くに任せ、そのあと追いつきます。大きいほどパーティの動きが揃わなくなり、0にすると全員が同じ動きに戻ります。大きく離れた場合はすぐに復帰します。Vanillaやサンドボックスには影響しません。",
"Companion individuality": "従者の個性",
"Swap left and right.": "左右を入れ替えます。",
"Swap preferred side": "優先側を入れ替える",
"Release formation control inside buildings.": "建物内では隊列制御を解除します。",
"Outdoors only": "屋外のみ",
"Hand holding (experimental)": "手つなぎ（実験的）",
"Hand-holding method": "手つなぎの方式",
"Classic restores the earlier procedural hand holding and needs no generated clasp animations. TETHER uses a physics grip and requires generated OAR clasp clips. Changing methods releases the current grip before reconnecting.":
 "Classicは以前のプロシージャル方式の手つなぎで、生成された握りアニメーションは不要です。TETHERは物理ベースの握りを使い、生成されたOARの握りクリップが必要です。方式を変えると、再接続の前に現在の握りが解除されます。",
"Work in progress: hands and wrists can still twist, and approach/turn animations may look awkward. Disabled by default. Choose one companion to hold hands in third-person Companion mode while walking, jogging or running. Sprinting, weapons, combat, jumping, swimming, scenes and rest release the grip.":
 "開発中：手や手首がねじれることがあり、接近・方向転換のアニメーションが不自然に見える場合があります。既定では無効です。三人称のCompanionモードで、歩き・小走り・走りの間に手をつなぐ従者を1人選びます。ダッシュ、武器の構え、戦闘、ジャンプ、水泳、シーン、休憩で手が離れます。",
"Hold hands (experimental)": "手をつなぐ（実験的）",
"Hand-holding companion": "手をつなぐ従者",
"None": "なし",
"None - choose one": "なし - 選んでください",
"This temporary actor has no persistent reference to remember. Choose a placed companion.":
 "この一時的なアクターには記憶できる永続参照がありません。配置済みの従者を選んでください。",
"Include this companion on the Party page first.": "先にPartyページでこの従者を含めてください。",
"Only this companion is eligible. They approach your side using normal pathfinding. Pause to let them arrive, turn and connect before walking together. After a failed attempt, step away before trying again. Selection saves automatically.":
 "対象はこの従者だけです。通常の経路探索であなたの横に近づきます。一緒に歩き出す前に、立ち止まって相手が到着し、向きを変え、つなぐのを待ってください。失敗したら、いったん離れてからやり直してください。選択は自動で保存されます。",
"Time in eligible Companion mode before looking for the selected follower. Paused menus do not count. Releasing the grip restarts this delay.":
 "選択した従者を探し始めるまでの、対象のCompanionモードでの経過時間。メニューによる一時停止は含まれません。手を離すとこの遅延が最初からやり直しになります。",
"Lead-in delay": "開始までの遅延",
"Pause and let the selected companion approach your side. Classic connects when the arms can reach; TETHER waits for aligned, close hands before its physics grip.":
 "立ち止まって、選んだ従者があなたの横に来るのを待ちます。Classicは腕が届いた時点でつなぎ、TETHERは手が揃って近づくのを待ってから物理ベースで握ります。",
"Connect within": "つなぐ距離",
"Release when the pair separates beyond this distance. TETHER allows a brief grace period. Reconnection waits through the lead-in again.":
 "二人の距離がこの値を超えて離れると手を離します。TETHERには短い猶予があります。再接続は、もう一度開始までの遅延を待ってから行われます。",
"Release beyond": "手を離す距離",
"Classic: distance between you and your companion while holding hands. Around 40 puts your shoulders together; wider leaves room between you. A change releases the grip, which then re-forms at the new spacing.":
 "Classic：手をつないでいる間の、あなたと従者の間隔。40前後で肩が触れ合い、大きくすると間が空きます。変更すると手が離れ、新しい間隔でつなぎ直されます。",
"Hand spacing": "手つなぎの間隔",
"Companion side": "従者の側",
"Classic: which of your hands the companion takes. Nearest uses whichever side they arrive on. If your camera sits over one shoulder and the companion fades out while holding hands, choose the other side. A change releases the grip.":
 "Classic：従者がどちらの手を取るか。Nearestは、相手が到着した側を使います。カメラが片方の肩越しにあり、手をつないでいる間に従者が透けて消える場合は、反対側を選んでください。変更すると手が離れます。",
"Restore travel defaults": "移動の設定を初期値に戻す",
# ---- Rest ----
"Rest & exploration": "休憩と探索",
"Automatically rest after you stand still, then resume following when you leave the rest area. Turn off to disable automatic rest; the Relax command remains available. Saves immediately.":
 "立ち止まると自動で休憩し、休憩エリアを離れると追従を再開します。オフにすると自動休憩が無効になります（Relaxコマンドは引き続き使えます）。すぐに保存されます。",
"Temporary rest": "一時休憩",
"Time standing still before automatic sandboxing. Travel resumes when you leave the resume area.":
 "自動サンドボックスが始まるまでの、立ち止まっている時間。再開エリアから出ると移動が再開します。",
"Begin after": "開始までの時間",
"Automatic stops only, until free roam opens. Companions head for activities inside it straight away; very small areas can leave them standing idle.":
 "自動で立ち止まった場合のみ、自由行動に切り替わるまでの範囲。従者はこの範囲内の活動へすぐ向かいます。ごく狭い場所では、立ったまま何もしないことがあります。",
"Nearby rest radius": "近場の休憩半径",
"Activity area used immediately by a Relax order, or after the automatic nearby phase ends. Companions set out for seats, idle markers or open ground across it at once.":
 "Relax命令ですぐに、または自動の近場フェーズが終わった後に使われる活動エリア。従者は範囲全体の座席、アイドルマーカー、開けた地面へ一斉に向かいます。",
"Free-roam radius": "自由行動の半径",
"Use nearby seats and activity markers from the start in homes, inns, other safe interiors and towns. Capped by Free-roam radius. Wilderness and dungeons keep the nearby phase; temporary rest keeps its resume distance.":
 "家、宿屋、その他の安全な屋内や街では、最初から近くの座席や活動マーカーを使います。上限は「自由行動の半径」です。荒野やダンジョンでは近場フェーズのままで、一時休憩は再開距離を維持します。",
"Indoor & town range": "屋内・街での範囲",
"Rest timing & limits": "休憩のタイミングと制限",
"How far above or below the fixed rest anchor to seek activities. Connected stairs or ramps are required; low values keep searches near the current floor. Does not change Skyrim's global sandbox settings.":
 "固定された休憩の基準点から、上下どこまで活動を探すか。階段やスロープでつながっている必要があります。小さい値だと現在の階の近くだけを探します。Skyrim全体のサンドボックス設定は変更しません。",
"Activity height": "活動の高さ範囲",
"Automatic stops only. One transition to the larger radius, after which companions head out across it. A direct Relax order skips this wait.":
 "自動で立ち止まった場合のみ。大きい半径へ一度だけ切り替わり、その後は従者が範囲全体へ散らばります。Relax命令を直接出した場合は、この待ち時間を飛ばします。",
"Free roam after": "自由行動に移るまで",
"Temporary rest continues while you stay within this distance of where you stopped, including dialogue. Relax ignores player distance.":
 "止まった場所からこの距離以内にいる間は、会話中も含めて一時休憩が続きます。Relaxはプレイヤーとの距離を無視します。",
"Resume following beyond": "追従を再開する距離",
"After sustained inactivity, allow a short walk inside the rest area. Personality adjusts this delay; staggered by up to 15 seconds, one companion at a time. Zero disables recovery.":
 "しばらく動きがない場合、休憩エリア内で少し歩くことを許可します。性格によってこの遅延が変わり、最大15秒ずつずらして1人ずつ行われます。0で無効になります。",
"Idle recovery delay": "待機からの復帰遅延",
"Activities": "活動",
"From time to time two resting companions pair up and talk for two to three minutes, with silent gestures. If they are apart, one walks over first. With Area activities the place shapes it: hushed in caves and ruins, over a drink at an inn.":
 "ときどき、休憩中の従者2人が組になり、声を出さない身ぶりで2〜3分ほど話します。離れている場合は、どちらかが先に歩み寄ります。「場所に応じた活動」をオンにすると場所が雰囲気を決め、洞窟や遺跡では声をひそめ、宿屋では酒を片手に話します。",
"Companion conversations": "従者どうしの会話",
"Resting fits the place: warming hands at fires, praying at shrines, the water's edge and lookouts outdoors, sweeping at home, nervous glances in caves and ruins. At an inn they share a table, call a server for drinks and applaud the bard.":
 "休憩の仕方が場所に合わせて変わります：焚き火で手を温める、祭壇で祈る、屋外では水辺や見晴らし場所で過ごす、家では掃除をする、洞窟や遺跡では不安げに辺りを見回す。宿屋では同じテーブルを囲み、給仕に飲み物を頼み、吟遊詩人に拍手を送ります。",
"Area activities": "場所に応じた活動",
"Optional scripted poses. Off by default: Skyrim chooses its normal furniture, idles and activities.":
 "任意のスクリプトによるポーズ。既定ではオフで、Skyrimが通常の家具、アイドル、活動を選びます。",
"Extra rest poses": "追加の休憩ポーズ",
"Sit on suitable outdoor wilderness ground. Never used inside buildings or dungeons.":
 "屋外の荒野の適した地面に座ります。建物内やダンジョンでは使われません。",
"Ground sitting": "地面に座る",
"Native meals plus occasional refreshments for idle companions in safe interiors and towns. Inns favor drinking; other places favor food. Does not require Extra rest poses. Disabled in caves and dungeons.":
 "安全な屋内や街で待機中の従者に、標準の食事に加えて、ときどき軽い飲食をさせます。宿屋では飲み物、それ以外の場所では食べ物が選ばれやすくなります。「追加の休憩ポーズ」は不要です。洞窟やダンジョンでは無効です。",
"Eating & drinking": "飲食",
"Read during quiet rests in safe locations.": "安全な場所での静かな休憩中に読書をします。",
"Reading": "読書",
"Occasional brief stretches between longer rests.": "長い休憩の合間に、ときどき短いストレッチをします。",
"Stretching": "ストレッチ",
"Party life": "パーティの日常",
"Other idle companions step aside during player dialogue. The speaking NPC, furniture users and active scenes are untouched.":
 "プレイヤーの会話中、待機している他の従者は脇にどきます。話しているNPC、家具を使用中の者、進行中のシーンには影響しません。",
"Give conversations space": "会話の場所をあける",
"Keep simple two-follower conversations moving. Partners try to trade positions with a nearby companion and walk beside each other. Scripted movement scenes and player dialogue retain control.":
 "従者2人だけの単純な会話を止めずに進めます。相手は近くの従者と位置を入れ替えようとし、並んで歩きます。スクリプトによる移動シーンとプレイヤーとの会話が優先されます。",
"Walk during follower banter": "従者の雑談中に歩く",
"Stable automatic tendencies affect socializing, exploration and lookout preference. Override each companion on the Party page.":
 "固定の自動的な傾向が、交流、探索、見張りの好みに影響します。Partyページで従者ごとに上書きできます。",
"Companion personalities": "従者の性格",
"During longer wilderness or dungeon rests, one free companion watches briefly. Requires at least three companions so two can still socialize.":
 "荒野やダンジョンでの長めの休憩中に、手の空いた従者が1人、短時間見張りに立ちます。2人が交流を続けられるよう、従者が3人以上必要です。",
"Occasional lookout": "ときどき見張り",
"Clearance around you, the NPC and the space between you. Only reachable positions are used.":
 "あなた、NPC、そして二人の間の空間の周囲に確保する余白。到達できる位置のみが使われます。",
"Conversation space": "会話の余白",
"Minimum rest time before a lookout. Watches last 30-45 seconds, with 90-150 seconds between watches.":
 "見張りが始まるまでの最小休憩時間。見張りは30〜45秒続き、次の見張りまで90〜150秒あけます。",
"Lookout after": "見張りまでの時間",
"Restore rest defaults": "休憩の設定を初期値に戻す",
# ---- Roles ----
"Loot scouting": "戦利品探索",
"Point out loot": "戦利品を知らせる",
"Your loot finder looks over the chests, bodies and valuable items in view, walks to the richest one and kneels to search it. One find per area. Works while travelling or standing still, not during rest or Relax.":
 "戦利品の探索役が、視界内の宝箱、死体、貴重品を見渡し、最も価値のあるものへ歩いて行き、ひざまずいて調べます。1エリアにつき1回です。移動中や立ち止まっている間は動作しますが、休憩中やRelax中は動作しません。",
"Loot finder": "戦利品の探索役",
"Any companion": "誰でも",
"Only one companion goes to a find at a time. Choose who does it, or leave Any companion to send whoever is nearest. Selection saves automatically.":
 "戦利品に向かうのは一度に1人だけです。担当を選ぶか、「誰でも」のままにして最も近い従者に任せます。選択は自動で保存されます。",
"Chests, urns, sacks and other containers. Owned containers (stealing) and your own storage are ignored. Food-only containers are skipped.":
 "宝箱、つぼ、袋などの箱。所有者のいる箱（盗みになるもの）と自分の収納は対象外です。食べ物だけの箱もスキップされます。",
"Containers": "箱",
"Dead people and creatures carrying real loot. Bodies with only pelts, meat or ingredients are skipped.":
 "価値のある戦利品を持った死んだ人やクリーチャー。毛皮、肉、素材だけの死体はスキップされます。",
"Bodies": "死体",
"Unowned items lying in the world, but only when they are worth more than the valuable threshold.":
 "世界に落ちている持ち主のいないアイテム。ただし「貴重」のしきい値より価値が高いものに限ります。",
"Loose valuables": "落ちている貴重品",
"Off: no scouting inside houses, inns, temples, shops, castles, guilds and your own home. Caves, ruins and the outdoors are unaffected.":
 "オフ：家、宿屋、聖堂、店、城、ギルド、自宅の中では探索を行いません。洞窟、遺跡、屋外には影響しません。",
"Inside homes and inns": "家や宿屋の中",
"Search tuning": "探索の調整",
"How far from a companion a find can be. They must also have a clear line of sight to it.":
 "従者からどれだけ離れた物を見つけられるか。対象への見通しも必要です。",
"Notice within": "気づく距離",
"If you move this far from the find, the companion leaves it and rejoins you. Finds must start within 80% of this distance from you.":
 "この距離だけ見つけた物から離れると、従者はそれを離れてあなたに合流します。見つけた物は、あなたからこの距離の80パーセント以内にあるものだけが対象です。",
"Leave when you are beyond": "離れる距離",
"If any single item in the find is worth more than this, the icon turns gold. Piles of septims count as a whole.":
 "見つけた物の中に、これより価値の高いアイテムが1つでもあると、アイコンが金色になります。ゴールドの山は全体で数えます。",
"%d gold": "%d ゴールド",
"Valuable above": "貴重とみなす価値",
"How long the finder kneels at the find before standing up to wait beside it. Opening the find or moving away ends it sooner.":
 "探索役が見つけた物の前でひざまずき、立ち上がって脇で待つまでの時間。見つけた物を開くか、離れると早く終わります。",
"Search for": "調べる時間",
"After the finder reaches one find, they stop looking until you are this far from it, or enter another interior or worldspace.":
 "探索役が1つの発見に到達した後は、あなたがそこからこの距離だけ離れるか、別の屋内やワールドスペースに入るまで探すのをやめます。",
"Search again after moving": "再探索までの移動距離",
"Restore loot tuning": "探索の設定を初期値に戻す",
"Pathfinder": "パスファインダー",
"Point out new places": "新しい場所を知らせる",
"In Natural, Lead, Companion and Custom, a companion who spots a place you have never found runs out toward it, turns to wave at you and points it out, then leads the way. Outdoors only, never while fighting, sneaking or riding.":
 "Natural、Lead、Companion、Customでは、まだ見つけていない場所を見つけた従者がそちらへ走り出し、振り返ってあなたに手を振り、指さしてから、先導します。屋外のみで、戦闘中、隠密中、騎乗中は行いません。",
"Any companion, curious first": "誰でも（好奇心旺盛な人を優先）",
"Who points places out. Any companion lets whoever can see it go, a curious one first.":
 "場所を知らせる担当。「誰でも」なら見える人が行き、好奇心旺盛な従者を優先します。",
"Turn to you and wave before pointing, to catch your eye.": "指さす前に、あなたの方を向いて手を振り、気を引きます。",
"Wave first": "先に手を振る",
"Show a notice naming what they saw and which way it lies.": "見つけたものの名前と、その方角を通知で表示します。",
"Name what they saw": "見つけたものを知らせる",
"After pointing it out, keep going toward it. Whenever they get far enough ahead they stop and wave you on, and walk on once you come close. Go another way, or find it, and they come back.":
 "知らせた後も、その場所へ進み続けます。十分に先行したら立ち止まって手招きし、あなたが近づくとまた歩き出します。別の道へ行くか、その場所を発見すると戻ってきます。",
"Lead the way": "先導する",
"Pathfinder tuning": "パスファインダーの調整",
"How far away an undiscovered place can be spotted. Places closer than 1500 units are already on your compass.":
 "未発見の場所をどこまで遠くから見つけられるか。1500ユニットより近い場所はすでにコンパスに表示されています。",
"Notice places within": "場所に気づく距離",
"How far ahead of you, straight toward the place, the pathfinder gets before stopping to wave you on. They stop 450 units short of the place itself.":
 "場所へ向かってまっすぐ進み、あなたをどこまで先行してから立ち止まって手招きするか。場所そのものの450ユニット手前で止まります。",
"Stop ahead of you at": "先行して止まる距離",
"How close you come before they lead on. Never more than half the stopping distance.":
 "あなたがどこまで近づいたら先導を再開するか。止まる距離の半分を超えることはありません。",
"Walk on when you're within": "先導を再開する距離",
"The shortest time between two places being pointed out.": "場所を知らせる間隔の最短時間。",
"Between sightings": "発見の間隔",
"Restore pathfinder tuning": "パスファインダーの設定を初期値に戻す",
# ---- Interface ----
"Follower icons": "従者のアイコン",
"Show an ivory speech bubble above resting companions with unheard conversation options. Filters follower commands, trading, services and random chatter.":
 "未聴の会話選択肢がある休憩中の従者の頭上に、アイボリー色の吹き出しを表示します。従者のコマンド、取引、サービス、ランダムな雑談は除外されます。",
"Show chat icons": "会話アイコンを表示",
"Pop up and gently float chat icons above companions. Off keeps a still, slightly transparent icon.":
 "従者の頭上で会話アイコンがポップアップし、ゆるやかに浮かびます。オフにすると、動かない少し透明なアイコンになります。",
"Animate chat icons": "会話アイコンをアニメーション",
"An animated chest marks the loot finder: ivory for ordinary loot, gold for valuable items. Requires loot scouting on the Loot page.":
 "戦利品の探索役を、動く宝箱で示します。通常の戦利品はアイボリー、貴重品は金色です。戦利品探索を有効にしておく必要があります。",
"Show loot icons": "戦利品アイコンを表示",
"The Pathfinder emblem floats above a companion from the moment they spot a new place until they have pointed it out, or until they stop. Requires Pathfinder on the Roles page.":
 "従者が新しい場所を見つけた瞬間から、知らせ終えるか止まるまで、パスファインダーのエンブレムが頭上に浮かびます。Rolesページでパスファインダーを有効にする必要があります。",
"Show pathfinder icons": "パスファインダーアイコンを表示",
"Order emblem": "命令エンブレム",
"Shows the current order on the right side of the screen.": "現在の命令を画面右側に表示します。",
"Show emblem": "エンブレムを表示",
"Subtle dark backing behind the order. Disable for bare icon and text.":
 "命令の背後にうっすら暗い下地を敷きます。アイコンと文字だけにしたい場合は無効にします。",
"Soft HUD backing": "HUDのやわらかい下地",
"Scale the small order emblem.": "小さな命令エンブレムの大きさを変えます。",
"Size": "大きさ",
"Distance down the right edge.": "右端に沿った、上からの位置。",
"Height": "高さ",
"Changes take effect and save automatically.": "変更は自動で反映・保存されます。",
"Troubleshooting": "トラブルシューティング",
"Record why a companion is released.": "従者が解放された理由を記録します。",
"Eligibility log": "適格性ログ",
"Record movement samples once per second.": "移動のサンプルを1秒ごとに記録します。",
"Movement log": "移動ログ",
# ---- Controls ----
"KEY BINDINGS": "キー割り当て",
"Select a binding, then hold Shift, Ctrl or Alt and press a key. Modifiers can be combined; either side works. Esc cancels; Delete clears.":
 "割り当てを選び、Shift・Ctrl・Altを押しながらキーを押します。修飾キーは組み合わせ可能で、左右どちらでも使えます。Escでキャンセル、Deleteで解除します。",
"Use the exact combination: G, Ctrl + G and Shift + G can each have their own action.":
 "組み合わせは完全一致で判定されます。G、Ctrl + G、Shift + Gにそれぞれ別の動作を割り当てられます。",
"Action": "動作",
"Key": "キー",
"Clear": "解除",
"Wheel & signals": "ホイールとシグナル",
"Gamepad wheel": "ゲームパッドのホイール",
"Hold LB and press the chosen button. Right stick aims; A confirms; B cancels.":
 "LBを押したまま、選んだボタンを押します。右スティックで選択、Aで決定、Bでキャンセルです。",
"Third-person Lead, Companion and Rear gestures need OAR and generated GP Offset Movement Animation behaviors. First-person signals use installed First Person Interactions clips.":
 "三人称のLead・Companion・Rearのジェスチャーには、OARと生成済みのGP Offset Movement Animationビヘイビアが必要です。一人称のシグナルは、導入済みのFirst Person Interactionsのクリップを使います。",
"Command hand signal": "命令の手振り",
"Briefly turn toward the party during a signal. Third person only.": "シグナルの間、パーティの方を軽く向きます。三人称のみ。",
"Glance toward followers": "従者に視線を向ける",
"Use the bundled left-hand point in third person. First person keeps the installed FPI forward reach.":
 "三人称では付属の左手で指さすモーションを使います。一人称では導入済みのFPIの前方へ手を伸ばす動作のままです。",
"Point for Lead": "Leadで指さす",
"Use the bundled two-arm invitation in third person. First person uses the installed FPI wave.":
 "三人称では付属の両腕で招くモーションを使います。一人称では導入済みのFPIの手振りを使います。",
"Invitation for Companion": "Companionで招く",
"Open party orders": "パーティ命令を開く",
"Commands pause in game menus. Avoid keys used by other mods or Skyrim quicksave / quickload.":
 "コマンドはゲーム内メニューを開いている間は停止します。他のMODや、Skyrimのクイックセーブ／クイックロードで使うキーは避けてください。",
"Party orders": "パーティ命令",
}

# 参照を持たず、コンボ用に \0 区切りで連結されている文字列群（先頭要素から参照される）
COMBOS = {
 ("Automatic","Balanced","Sociable","Curious","Reserved","Watchful"):
 ("自動","バランス型","社交的","好奇心旺盛","控えめ","用心深い"),
 ("Unbound","LB + Right-stick click","LB + Y","LB + D-pad up"):
 ("未割り当て","LB + 右スティック押し込み","LB + Y","LB + 十字キー上"),
}

# ポインタ表(.rdata内のスロット)で参照される表示名: (スロットVA, 原文, 訳)
SLOTS = [
 (0x2152e0,"Enable / disable","有効 / 無効の切り替え"),
 (0x215300,"Cycle formation","隊列の切り替え"),
 (0x215380,"Reload INI","INIの再読み込み"),
 (0x2153a0,"Companion control","従者の制御"),
 (0x2153c0,"Hold hands","手つなぎ"),
 (0x2152c0,"Party orders","パーティ命令"),
]
EMBLEMS = {"Band":"一団","Banner":"旗印","Crown":"王冠","Castle":"城","Swords":"剣","Dragon":"ドラゴン",
 "Wolf":"オオカミ","Raven":"ワタリガラス","Stag":"牡鹿","Steed":"軍馬","Pine":"松","Rune":"ルーン",
 "Watch":"見張り","Moon":"月","Calm":"鎮静","Tavern":"酒場"}

# 命令(Order)の説明文: .rdata のポインタ表スロット。モード名(Natural等)は英語のまま。
DESC_SLOTS = [
 (0x214d68,"Find your own space as we travel","移動中はそれぞれ好きな位置を歩いて"),
 (0x214d70,"Take the lead along our route","道中は先頭を歩いて案内して"),
 (0x214d78,"Travel at my side","私の隣を歩いて"),
 (0x214d80,"Keep to the rear","後ろを歩いて"),
 (0x214d88,"Stay here and make yourselves at home","ここに残ってくつろいで"),
 (0x214d90,"Return travel and rest to Skyrim or your follower framework","移動と休憩を、Skyrim本来の動作または従者フレームワークに戻す"),
 (0x214d98,"Travel in the formation you drew in Travel settings","Travel設定で描いた隊列で移動する"),
]

# ホイール(WalkWithMeOrders)の命令説明: 関数 0xc7090 内の lea reg,[rip+disp32] を直接付け替える。
# (addr, 原文, 訳)  ポインタのみ・NUL終端文字列(ImDrawList_AddText)なので長さ固定の問題は無い。
WHEEL_LEA = [
 (0xc95c9, "Find your own pace",           "好きなペースで進んで"),
 (0xc95d7, "Take the road ahead",          "前を歩いて案内して"),
 (0xc95e5, "Stay by my side",              "私のそばにいて"),
 (0xc95f3, "Watch our backs",              "背後を見張って"),
 (0xc9601, "Make yourselves at home",      "くつろいで"),
 (0xc960f, "Return to follower AI",        "従者AIに戻す"),
 (0xc961d, "Walk as I drew it",            "描いた隊列で歩いて"),
 (0xc9879, "Draw one in Travel settings",  "先にTravel設定で隊列を描いて"),
]

# ---- Party Actions(ホイール) ----
# (a) strlen経由でstd::stringを作る箇所: lea のみ付け替え
ACTION_LEA = [
 # 下端の操作ヒント(ホイールと Party Actions の画面で、パッドとキーボードの2種類ずつ。NUL終端でテキスト描画へ渡される)
 (0xca4f4, "Stick: aim    A: order    D-pad down: party actions    B: back",
   "スティック: 方向を選ぶ    A: 命令    十字キー下: Party Actions    B: 戻る"),
 (0xca4fb, "Click / 1-7: order    Tab: party actions    Esc: back",
   "クリック / 1-7: 命令    Tab: Party Actions    Esc: 戻る"),
 (0xca5d7, "Stick / D-pad: choose    A: select    Up: party orders    B: back",
   "スティック / 十字キー: 選ぶ    A: 決定    上: Party Orders    B: 戻る"),
 (0xca5de, "Click / arrows: choose    Enter: select    Tab: party orders    Esc: back",
   "クリック / 方向キー: 選ぶ    Enter: 決定    Tab: Party Orders    Esc: 戻る"),
 (0xc7e35, "Saving...",            "保存中..."),
 (0xc7e3e, "Settle when you stop", "止まったらくつろぐ"),
 (0xc7e45, "Keep to your feet",    "立ったまま待機"),
 (0xc814a, "Guiding",              "案内中"),
 (0xc8151, "Follower AI",          "従者AI"),
 (0xc8925, "Roles and tactics",     "役割と戦術"),
 (0xc892c, "Needs Fight With Me",   "Fight With Meが必要"),
]
# (b) 下部の説明(ポインタ表 0x21a600 の8スロット)
HINT_SLOTS = [
 (0x21a600, "Bring every travelling companion to clear ground beside you, even from another cell.",
            "旅の従者を全員、別のセルにいても近くの開けた場所へ呼び寄せる。"),
 (0x21a608, "When you stop, the party settles in nearby. Off: they wait on their feet.",
            "立ち止まると、パーティは近くでくつろぐ。オフの場合は立ったまま待つ。"),
 (0x21a610, "Take or return control of the companion you were looking at.",
            "見ていた従者の制御を引き継ぐ、または返す。"),
 (0x21a618, "Switch party guidance on or off. Off hands everyone back to their own AI.",
            "パーティの案内をオン/オフに切り替える。オフにすると全員が各自のAIに戻る。"),
 (0x21a620, "Walk hand in hand in Companion style with your partner, or the nearest companion.",
            "Companionモードで選んだ相手、または最も近い従者と手をつないで歩く。"),
 (0x21a628, "Your finder points out chests, bodies and valuables worth a look.",
            "探索役が、宝箱や死体、調べる価値のある品を教えてくれる。"),
 (0x21a630, "Your pathfinder points out places you have never found, in Natural, Lead and Companion.",
            "Pathfinderが、まだ見つけていない場所を教えてくれる(Natural、Lead、Companion時)。"),
 (0x21a638, "Give each companion a role, a focus and a place in battle. Comes with Fight With Me.",
            "従者それぞれに、役割・狙う相手・戦闘での持ち場を与える。Fight With Meを導入すると使える。"),
]
# (c) コード内で文字をコピーしている箇所: 命令列を std::string コンストラクタ呼び出しに置換
#     (region_start, region_end, 出力先 rbp+off, 原文, 訳)
INLINE = [
 (0xc7bd7, 0xc7c25, 0x880, "Teleport queued",    "テレポート待機中"),
 (0xc7fd0, 0xc8013, 0x880, "Look at a companion","従者を見る"),
 (0xc82fa, 0xc8333, 0x8a0, "Nearest companion", "最寄りの従者"),
 (0xc8592, 0xc85d2, 0x860, "Any companion",      "どの従者でも"),
 (0xc86fe, 0xc8737, 0x860, "Not in this style",  "この命令では不可"),
 (0xc8769, 0xc87a9, 0x880, "Curious first",      "好奇心旺盛な従者が先"),
 (0xc83ce, 0xc8401, 0x860, "In Companion",      "Companionで有効"),
 (0xc823a, 0xc826d, 0x880, "your partner",      "指定の相手"),
]
# (d) fmt 書式(ポインタ+長さ): (lea addr, 長さ即値addr+7, 原文, 訳)  ※第2引数("s")は未使用になる
FMT_SITES = [(0xc7c9a, 0xc7ca8, "{} companion{} ready", "{}人の従者が準備完了")]
# (e) ホイール中央の説明の文字サイズ: movss xmm,[rip+disp] を新定数へ付け替え (addr, 旧値, 新値)
CONST_SITES = [
 (0xc964a, 0.33, 0.40),    # 説明の最大幅  (旧 0.33)
 (0xc9653, 0.02, 0.028),   # 説明の文字サイズ上限 (旧 0.02)
 (0xb9ae2, 0.02, 0.028),   # Party Actions 下部の説明: 文字サイズ上限 (mulss)
 (0xb9ac5, 0.88, 1.25),    # Party Actions 下部の説明: 最大幅 (mulss)
 (0xca4b9, 0.017, 0.024),  # 下端の操作ヒント(Click / arrows: ...): 文字サイズ上限 (mulss)
]

# (f) 前置詞つきの連結 "With " + 相手の名前: operator+ (0xb33f0) に 前置詞ポインタ(r9)と長さ(スタック [rsp+0x20])を渡す箇所。
#     (lea r9 の addr, 長さ即値 mov qword [rsp+0x20],imm32 の addr, 上限チェック cmp rax,imm8 の addr, 原文, 訳)
PREFIX_SITES = [(0xc8394, 0xc838b, 0xc8360, "With ", "相手: ")]
