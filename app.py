import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Force reload modules
if 'src.yaku_detector' in sys.modules:
    del sys.modules['src.yaku_detector']
if 'src.tile_parser' in sys.modules:
    del sys.modules['src.tile_parser']
if 'src.hand_analyzer' in sys.modules:
    del sys.modules['src.hand_analyzer']
if 'src.points_calculator' in sys.modules:
    del sys.modules['src.points_calculator']

from src.tile_parser import Tile, TileType
from src.hand_analyzer import HandAnalyzer
from src.yaku_detector import YakuDetector
from src.points_calculator import PointsCalculator

# Page config
st.set_page_config(
    page_title="日麻點數計算助手",
    page_icon="🀄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for tiles
if 'selected_tiles' not in st.session_state:
    st.session_state.selected_tiles = []

# Emoji mapping for tiles - 字牌順序修正！
TILE_EMOJI = {
    'm': {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣'},
    'p': {1: '🔴', 2: '🟠', 3: '🟡', 4: '🟢', 5: '🔵', 6: '🟣', 7: '🟤', 8: '⚪', 9: '⚫'},
    's': {1: '🌾', 2: '🌿', 3: '🍀', 4: '🌱', 5: '🌲', 6: '🌳', 7: '🌴', 8: '🎋', 9: '🎍'},
    'z': {1: '🀄', 2: '🀅', 3: '🀆', 4: '🀇', 5: '⚪', 6: '🟢', 7: '🔴'}  # 1=東 2=南 3=西 4=北 5=白 6=發 7=中
}

# ============================================================================
# MAIN UI
# ============================================================================

st.title("🀄 日麻點數計算助手")
st.markdown("🎯 **點擊下方牌圖選擇手牌（共14張）**")

# ============================================================================
# TILE SELECTION AREA
# ============================================================================

st.markdown("---")
st.subheader("🎴 選擇手牌")

# Create columns for each suit
suit_tabs = st.tabs(['🔢 萬子', '🟠 筒子', '🌾 索子', '🀄 字牌'])

# Wan (Man) - 萬子
with suit_tabs[0]:
    st.markdown("#### 萬子 (1-9)")
    cols = st.columns(9)
    for num in range(1, 10):
        with cols[num-1]:
            if st.button(
                f"{TILE_EMOJI['m'][num]}\n{num}",
                key=f"btn_m{num}",
                use_container_width=True,
                help=f"點擊添加萬子{num}"
            ):
                st.session_state.selected_tiles.append(Tile(num, TileType.MAN))
                st.rerun()

# Pin (Pinzu) - 筒子
with suit_tabs[1]:
    st.markdown("#### 筒子 (1-9)")
    cols = st.columns(9)
    for num in range(1, 10):
        with cols[num-1]:
            if st.button(
                f"{TILE_EMOJI['p'][num]}\n{num}",
                key=f"btn_p{num}",
                use_container_width=True,
                help=f"點擊添加筒子{num}"
            ):
                st.session_state.selected_tiles.append(Tile(num, TileType.PIN))
                st.rerun()

# Sou (Souzu) - 索子
with suit_tabs[2]:
    st.markdown("#### 索子 (1-9)")
    cols = st.columns(9)
    for num in range(1, 10):
        with cols[num-1]:
            if st.button(
                f"{TILE_EMOJI['s'][num]}\n{num}",
                key=f"btn_s{num}",
                use_container_width=True,
                help=f"點擊添加索子{num}"
            ):
                st.session_state.selected_tiles.append(Tile(num, TileType.SOU))
                st.rerun()

# Honor (Jihai) - 字牌
with suit_tabs[3]:
    st.markdown("#### 字牌 (東南西北中發白)")
    honor_names = ['東', '南', '西', '北', '白', '發', '中']
    honor_emojis = ['🀄', '🀅', '🀆', '🀇', '⚪', '🟢', '🔴']
    cols = st.columns(7)
    for num in range(1, 8):
        with cols[num-1]:
            if st.button(
                f"{honor_emojis[num-1]}\n{honor_names[num-1]}",
                key=f"btn_z{num}",
                use_container_width=True,
                help=f"點擊添加{honor_names[num-1]}"
            ):
                st.session_state.selected_tiles.append(Tile(num, TileType.HONOR))
                st.rerun()

# ============================================================================
# SELECTED TILES DISPLAY
# ============================================================================

st.markdown("---")
st.subheader(f"📋 已選擇的牌 ({len(st.session_state.selected_tiles)}/14)")

if st.session_state.selected_tiles:
    # Display selected tiles with emoji
    display_text = ""
    for i, tile in enumerate(st.session_state.selected_tiles):
        emoji = TILE_EMOJI[tile.tile_type.value].get(tile.number, '❓')
        display_text += emoji
        if (i + 1) % 7 == 0:
            display_text += "\n"
    
    st.markdown(f"### {display_text}")
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ 撤銷上一個", use_container_width=True, key="undo"):
            if st.session_state.selected_tiles:
                st.session_state.selected_tiles.pop()
                st.rerun()
    
    with col2:
        if st.button("🗑️ 清空所有", use_container_width=True, key="clear"):
            st.session_state.selected_tiles = []
            st.rerun()
    
    with col3:
        st.metric("", f"{len(st.session_state.selected_tiles)}/14 張牌")
else:
    st.info("👆 點擊上方的牌圖來選擇手牌")

# ============================================================================
# GAME SETTINGS
# ============================================================================

st.markdown("---")
st.subheader("⚙️ 場況設置")

col_basic1, col_basic2, col_basic3, col_basic4 = st.columns(4)

with col_basic1:
    is_parent = st.radio(
        "玩家身份",
        ["👑 親家", "👤 子家"],
        index=0,
        label_visibility="collapsed"
    ) == "👑 親家"

with col_basic2:
    is_tsumo = st.radio(
        "勝利方式",
        ["🎯 自摸", "🎪 榮和"],
        index=0,
        label_visibility="collapsed"
    ) == "🎯 自摸"

with col_basic3:
    dora = st.number_input("🎁 寶牌數", min_value=0, max_value=10, value=0, step=1)

with col_basic4:
    is_riichi = st.checkbox("⚡ 立直", value=False)

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

st.markdown("---")
st.subheader("🎲 進階設置")

col_adv1, col_adv2, col_adv3, col_adv4 = st.columns(4)

with col_adv1:
    field_wind = st.radio(
        "🌍 場風",
        ["東", "南", "西", "北"],
        index=0,
        label_visibility="collapsed"
    )

with col_adv2:
    player_wind = st.radio(
        "👤 自風",
        ["東", "南", "西", "北"],
        index=0,
        label_visibility="collapsed"
    )

with col_adv3:
    honba = st.number_input("💰 本場數", min_value=0, max_value=10, value=0, step=1)

with col_adv4:
    ura_dora = st.number_input("🔴 裏寶牌數", min_value=0, max_value=10, value=0, step=1)

# ============================================================================
# CALCULATE BUTTON
# ============================================================================

st.markdown("---")

calculate_button = st.button(
    "🧮 計算點數",
    use_container_width=True,
    type="primary",
    key="calculate"
)

# ============================================================================
# CALCULATION LOGIC
# ============================================================================

if calculate_button:
    if len(st.session_state.selected_tiles) != 14:
        st.error(f"❌ 手牌數量不對！\n\n目前選擇了 **{len(st.session_state.selected_tiles)}/14** 張牌，請繼續選擇。")
    else:
        try:
            # Initialize calculators
            analyzer = HandAnalyzer()
            detector = YakuDetector()
            calculator = PointsCalculator()
            
            tiles = st.session_state.selected_tiles
            
            # Check if winning hand
            is_winning = analyzer.is_winning_hand(tiles)
            
            if not is_winning:
                st.error("❌ 不是和牌！\n\n這個手牌組合不符合和牌條件，請檢查是否輸入正確。")
            else:
                # Get all yakus and check which are possible
                all_yakus = detector.detect_all_yakus(tiles, is_tsumo)
                
                # Detect primary yaku
                detected_yakus = detector.detect_yaku(tiles, is_tsumo)
                
                # Calculate han and fu
                han = 0
                fu = 30
                yaku_names = []
                
                for yaku_name, yaku_han, yaku_fu in detected_yakus:
                    yaku_names.append(yaku_name)
                    han = max(han, yaku_han)
                    fu = yaku_fu
                
                # Add riichi
                if is_riichi:
                    yaku_names.insert(0, "⚡ 立直")
                    han += 1
                
                # Total han with dora and ura dora
                total_han = han + dora + ura_dora
                
                # ============================================================
                # DISPLAY RESULTS
                # ============================================================
                
                st.markdown("---")
                st.success("✅ 和牌成功！")
                
                # Yaku display
                st.markdown("### 🎯 識別的役種")
                yaku_display = " + ".join(yaku_names) if yaku_names else "通常役"
                st.markdown(f"#### {yaku_display}")
                
                # Stats
                st.markdown("---")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("翻數", f"{total_han} 翻")
                
                with col2:
                    st.metric("符數", f"{fu} 符")
                
                with col3:
                    st.metric("寶牌", f"{dora + ura_dora} 張")
                
                with col4:
                    st.metric("本場", f"{honba} 場")
                
                with col5:
                    if total_han >= 5:
                        if total_han >= 13:
                            mangan_type = "役滿"
                        elif total_han >= 11:
                            mangan_type = "三倍滿"
                        elif total_han >= 8:
                            mangan_type = "倍滿"
                        elif total_han >= 6:
                            mangan_type = "跳滿"
                        else:
                            mangan_type = "滿貫"
                        st.metric("級別", f"🔥 {mangan_type}")
                    else:
                        st.metric("級別", "⭐ 通常役")
                
                # Payment calculation
                st.markdown("---")
                st.markdown("### 💰 點數分配")
                
                col_payment1, col_payment2 = st.columns(2)
                
                if is_parent:
                    if is_tsumo:
                        child_payment = calculator.calculate_parent_tsumo_payment(total_han, fu)
                        total_payment = child_payment * 3
                        honba_payment = 100 * honba
                        total_payment += honba_payment
                        
                        with col_payment1:
                            st.info(
                                f"### 👑 親自摸\n\n"
                                f"**每個子家支付**: {child_payment:,} 點\n\n"
                                f"**本場收益**: {honba_payment:,} 點\n\n"
                                f"**獲得總點**: {total_payment:,} 點"
                            )
                        
                        with col_payment2:
                            st.markdown("#### 支付詳情")
                            st.markdown(f"🔹 子家 1: {child_payment:,} 點")
                            st.markdown(f"🔹 子家 2: {child_payment:,} 點")
                            st.markdown(f"🔹 子家 3: {child_payment:,} 點")
                            st.markdown(f"🔹 本場收益: {honba_payment:,} 點")
                            st.markdown(f"---")
                            st.markdown(f"**合計**: {total_payment:,} 點")
                    else:
                        payment = calculator.calculate_parent_ron_payment(total_han, fu)
                        honba_payment = 300 * honba
                        total_payment = payment + honba_payment
                        
                        with col_payment1:
                            st.info(
                                f"### 👑 親榮和\n\n"
                                f"**放銃者支付**: {payment:,} 點\n\n"
                                f"**本場收益**: {honba_payment:,} 點\n\n"
                                f"**獲得點**: {total_payment:,} 點"
                            )
                        
                        with col_payment2:
                            st.markdown("#### 支付詳情")
                            st.markdown(f"🔹 放銃者: {payment:,} 點")
                            st.markdown(f"🔹 本場收益: {honba_payment:,} 點")
                            st.markdown(f"---")
                            st.markdown(f"**合計**: {total_payment:,} 點")
                else:
                    if is_tsumo:
                        parent_payment = calculator.calculate_child_tsumo_parent_payment(total_han, fu)
                        child_payment = calculator.calculate_child_tsumo_child_payment(total_han, fu)
                        total_payment = parent_payment + (child_payment * 2)
                        honba_payment = 100 * honba
                        total_payment += honba_payment
                        
                        with col_payment1:
                            st.info(
                                f"### 👤 子自摸\n\n"
                                f"**親家支付**: {parent_payment:,} 點\n\n"
                                f"**子家各支付**: {child_payment:,} 點\n\n"
                                f"**本場收益**: {honba_payment:,} 點\n\n"
                                f"**獲得總點**: {total_payment:,} 點"
                            )
                        
                        with col_payment2:
                            st.markdown("#### 支付詳情")
                            st.markdown(f"🔹 親家: {parent_payment:,} 點")
                            st.markdown(f"🔹 子家 1: {child_payment:,} 點")
                            st.markdown(f"🔹 子家 2: {child_payment:,} 點")
                            st.markdown(f"🔹 本場收益: {honba_payment:,} 點")
                            st.markdown(f"---")
                            st.markdown(f"**合計**: {total_payment:,} 點")
                    else:
                        payment = calculator.calculate_child_ron_payment(total_han, fu)
                        honba_payment = 300 * honba
                        total_payment = payment + honba_payment
                        
                        with col_payment1:
                            st.info(
                                f"### 👤 子榮和\n\n"
                                f"**放銃者支付**: {payment:,} 點\n\n"
                                f"**本場收益**: {honba_payment:,} 點\n\n"
                                f"**獲得點**: {total_payment:,} 點"
                            )
                        
                        with col_payment2:
                            st.markdown("#### 支付詳情")
                            st.markdown(f"🔹 放銃者: {payment:,} 點")
                            st.markdown(f"🔹 本場收益: {honba_payment:,} 點")
                            st.markdown(f"---")
                            st.markdown(f"**合計**: {total_payment:,} 點")
                
                # Hand analysis
                st.markdown("---")
                st.markdown("### 📊 手牌分析")
                
                hand_analysis = analyzer.analyze_hand_structure(tiles)
                
                col_analysis1, col_analysis2, col_analysis3, col_analysis4 = st.columns(4)
                
                with col_analysis1:
                    st.metric("花色數", f"{hand_analysis['color_count']} 種")
                
                with col_analysis2:
                    has_terminal_text = "✅ 有" if hand_analysis['has_terminal'] else "❌ 無"
                    st.metric("么九牌", has_terminal_text)
                
                with col_analysis3:
                    has_honor_text = "✅ 有" if hand_analysis['has_honor'] else "❌ 無"
                    st.metric("字牌", has_honor_text)
                
                with col_analysis4:
                    st.metric("場風", field_wind)
                
                # Show all possible yakus
                st.markdown("---")
                st.markdown("### 📋 所有可能的役種")
                
                yaku_cols = st.columns(3)
                col_idx = 0
                
                for yaku_name in sorted(all_yakus.keys()):
                    yaku_info = all_yakus[yaku_name]
                    is_possible = yaku_info.get('possible', False)
                    han_count = yaku_info.get('han', 0)
                    
                    with yaku_cols[col_idx % 3]:
                        if is_possible:
                            st.success(f"✅ {yaku_name}\n({han_count} 翻)")
                        else:
                            st.write(f"❌ {yaku_name}\n({han_count} 翻)")
                    
                    col_idx += 1
        
        except Exception as e:
            st.error(f"❌ 計算發生錯誤\n\n{str(e)}")
            import traceback
            st.write(traceback.format_exc())

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85rem;'>"
    "日麻點數計算助手 v6.1 | 完整場況 + 所有役種列表 | 已修復"
    "</div>",
    unsafe_allow_html=True
)
