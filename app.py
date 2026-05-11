import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tile_parser import TileParser
from hand_analyzer import HandAnalyzer
from yaku_detector import YakuDetector
from points_calculator import PointsCalculator

# Page config
st.set_page_config(
    page_title="日麻點數計算助手",
    page_icon="🀄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #F0F8FF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #FFE5E5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #E5F5E5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #52A552;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>🀄 日麻點數計算助手</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>輸入手牌和場況，自動計算點數</p>", unsafe_allow_html=True)

# Sidebar - Game settings
st.sidebar.header("⚙️ 場況設置")

is_parent = st.sidebar.radio("玩家身份", ["親家 (Parent)", "子家 (Child)"], index=0)
is_parent = (is_parent == "親家 (Parent)")

win_type = st.sidebar.radio("勝利方式", ["自摸 (Self-draw)", "榮和 (Ron)"], index=0)
is_tsumo = (win_type == "自摸 (Self-draw)")

# Main content - Two columns
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🎴 輸入手牌")
    st.markdown("**格式說明**: 使用 m(萬子) p(筒子) s(索子) z(字牌)")
    st.markdown("**例子**: `123m456p789s1122z`")
    
    hand_input = st.text_input(
        "手牌輸入",
        value="",
        placeholder="123m456p789s1122z",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.subheader("🎯 役種選擇")
    
    yaku_options = [
        "立直 (Riichi)",
        "門前清模和 (Menzen Tsumo)",
        "平胡 (Pinfu)",
        "斷么九 (Tanyao)",
        "一盃口 (Iipeiko)",
        "三色同順 (Sanshoku Doujun)",
        "一氣通貫 (Ittsu)",
        "三色同刻 (Sanshoku Doukou)",
        "三槓子 (Sankantsu)",
        "三暗刻 (Sanankou)",
        "小三元 (Shousangen)",
        "混老頭 (Honroutou)",
        "混全帶么九 (Honchantaghan)",
        "混一色 (Honisou)",
        "清一色 (Chiisou)",
        "國士無双 (Kokushi)",
        "大三元 (Daisangen)",
        "大四喜 (Daisushi)",
        "清老頭 (Chinroutou)",
        "字一色 (Tsuisou)",
        "綠一色 (Ryuisou)",
        "四暗刻 (Suankou)",
        "九蓮寶燈 (Chuuren Poutou)"
    ]
    
    selected_yakus = st.multiselect(
        "選擇役種",
        yaku_options,
        default=[],
        label_visibility="collapsed"
    )
    
    # Additional options
    st.markdown("---")
    st.subheader("📊 其他設置")
    
    is_riichi = "立直 (Riichi)" in selected_yakus
    is_double_riichi = st.checkbox("雙立直", value=False, disabled=not is_riichi)
    is_ippatsu = st.checkbox("一發", value=False)
    is_kan = st.checkbox("嶺上開花", value=False)
    is_sea = st.checkbox("海底撈月", value=False)
    is_river = st.checkbox("河底撈魚", value=False)
    
    dora_count = st.number_input("寶牌數", min_value=0, max_value=10, value=0)
    ura_dora_count = st.number_input("裏寶牌數", min_value=0, max_value=10, value=0)

with col2:
    st.subheader("📈 計算結果")
    
    if hand_input:
        try:
            # Parse tiles
            parser = TileParser()
            tiles = parser.parse(hand_input)
            
            if len(tiles) != 14:
                st.markdown(
                    f"<div class='error-box'><strong>❌ 錯誤</strong><br/>手牌數量應為14張，目前為 {len(tiles)} 張</div>",
                    unsafe_allow_html=True
                )
            else:
                # Analyze hand
                analyzer = HandAnalyzer()
                is_winning = analyzer.is_winning_hand(tiles)
                
                if not is_winning:
                    st.markdown(
                        "<div class='error-box'><strong>❌ 不是和牌</strong><br/>輸入的手牌不符合和牌條件</div>",
                        unsafe_allow_html=True
                    )
                else:
                    # Detect yaku
                    detector = YakuDetector()
                    detected_yakus = detector.detect_yaku(tiles, is_tsumo)
                    
                    # Calculate points
                    calculator = PointsCalculator()
                    
                    han = 0
                    fu = 30
                    
                    # Get han from detected yaku
                    for yaku_name, yaku_han, yaku_fu in detected_yakus:
                        han = max(han, yaku_han)
                        fu = yaku_fu
                    
                    # Add dora
                    han += dora_count + ura_dora_count
                    
                    # Calculate payment
                    if is_parent:
                        if is_tsumo:
                            child_payment = calculator.calculate_parent_tsumo_payment(han, fu)
                            total = child_payment * 3
                            st.markdown(f"""
                            <div class='result-box'>
                                <h3 style='color: #2E86AB;'>親自摸</h3>
                                <p><strong>番數:</strong> {han} 番</p>
                                <p><strong>符數:</strong> {fu} 符</p>
                                <p><strong>支付額:</strong> 子家各 {child_payment:,} 點</p>
                                <p style='font-size: 1.2rem; color: #2E86AB;'><strong>合計: {total:,} 點</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            payment = calculator.calculate_parent_ron_payment(han, fu)
                            st.markdown(f"""
                            <div class='result-box'>
                                <h3 style='color: #2E86AB;'>親榮和</h3>
                                <p><strong>番數:</strong> {han} 番</p>
                                <p><strong>符數:</strong> {fu} 符</p>
                                <p><strong>支付額:</strong> {payment:,} 點</p>
                                <p style='font-size: 1.2rem; color: #2E86AB;'><strong>合計: {payment:,} 點</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        if is_tsumo:
                            parent_payment = calculator.calculate_child_tsumo_parent_payment(han, fu)
                            child_payment = calculator.calculate_child_tsumo_child_payment(han, fu)
                            total = parent_payment + (child_payment * 2)
                            st.markdown(f"""
                            <div class='result-box'>
                                <h3 style='color: #2E86AB;'>子自摸</h3>
                                <p><strong>番數:</strong> {han} 番</p>
                                <p><strong>符數:</strong> {fu} 符</p>
                                <p><strong>親家支付:</strong> {parent_payment:,} 點</p>
                                <p><strong>子家各支付:</strong> {child_payment:,} 點</p>
                                <p style='font-size: 1.2rem; color: #2E86AB;'><strong>合計: {total:,} 點</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            payment = calculator.calculate_child_ron_payment(han, fu)
                            st.markdown(f"""
                            <div class='result-box'>
                                <h3 style='color: #2E86AB;'>子榮和</h3>
                                <p><strong>番數:</strong> {han} 番</p>
                                <p><strong>符數:</strong> {fu} 符</p>
                                <p><strong>支付額:</strong> {payment:,} 點</p>
                                <p style='font-size: 1.2rem; color: #2E86AB;'><strong>合計: {payment:,} 點</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Show detected yaku
                    if detected_yakus:
                        st.markdown("---")
                        st.subheader("🎯 識別的役種")
                        for yaku_name, yaku_han, yaku_fu in detected_yakus:
                            st.markdown(
                                f"<div class='success-box'><strong>{yaku_name}</strong> - {yaku_han} 番 {yaku_fu} 符</div>",
                                unsafe_allow_html=True
                            )
                    
                    # Show hand structure
                    st.markdown("---")
                    st.subheader("🎴 手牌結構")
                    tiles_str = parser.to_string(tiles)
                    st.code(tiles_str, language="text")
                    
        except Exception as e:
            st.markdown(
                f"<div class='error-box'><strong>❌ 錯誤</strong><br/>{str(e)}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("👈 在左側輸入手牌開始計算")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9rem;'>
    <p>日麻點數計算助手 v2.0</p>
    <p>© 2026 zanhdada1024-sketch</p>
</div>
""", unsafe_allow_html=True)
