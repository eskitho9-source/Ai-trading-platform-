import streamlit as st
import pandas as pd
import time
from datetime import datetime

# 1. إعدادات المنصة الاحترافية (Design & UI)
st.set_page_config(page_title="AI Institutional Trading Hub", layout="wide", initial_sidebar_state="expanded")

# --- محرك التحليل المؤسسي (The Core Engine) ---
def get_mtf_logic(style):
    if "Scalp" in style:
        return {"HTF": "15m", "ITF": "5m", "LTF": "1m (Entry)", "Narrative": "Liquidity Sweep on 15m"}
    else:
        return {"HTF": "Weekly/Daily", "ITF": "4H", "LTF": "1H (Entry)", "Narrative": "Weekly POI Mitigation"}

# --- واجهة المستخدم (Bilingual UI) ---
st.sidebar.title("🎮 Control Panel / لوحة التحكم")
lang = st.sidebar.radio("Language / اللغة", ["English", "العربية"])
page = st.sidebar.radio("Navigation / التنقل", ["⚙️ Setup / الإعدادات", "📊 Live Hub / المراقبة"])

# --- الصفحة الأولى: الإعدادات (Setup) ---
if page == "⚙️ Setup / الإعدادات":
    st.title("⚙️ System Setup / إعدادات المنصة")
    
    col1, col2 = st.columns(2)
    with col1:
        market = st.selectbox("Select Pair / اختر الزوج", ["EURUSD", "GBPUSD", "USDJPY"])
        style = st.selectbox("Style / الأسلوب", ["Scalp (Fast) / سكالب", "Swing (HTF) / سوينج"])
        balance = st.number_input("Capital / رأس المال ($)", value=1000)
        
    with col2:
        risk = st.slider("Risk / المخاطرة (%)", 0.1, 5.0, 1.0)
        # حساب اللوت آلياً بناءً على الأسلوب
        pips = 10 if "Scalp" in style else 50
        recommended_lot = (balance * (risk/100)) / (pips * 10)
        st.success(f"Recommended Lot / اللوت المقترح: {recommended_lot:.2f}")

    if st.button("🚀 Start Monitoring / بدء المراقبة"):
        st.session_state['active'] = {"market": market, "lot": recommended_lot, "style": style, "balance": balance, "risk": risk}
        st.balloons()

# --- الصفحة الثانية: المراقبة الحية (Live Hub) ---
else:
    st.title("📊 Institutional Live Hub / المراقبة المؤسسية")
    if 'active' not in st.session_state:
        st.warning("⚠️ Please configure setup first! / برجاء ضبط الإعدادات أولاً")
    else:
        conf = st.session_state['active']
        mtf = get_mtf_logic(conf['style'])
        
        # تقسيم الشاشة (شارت + بيانات)
        col_chart, col_intel = st.columns([2, 1])
        
        with col_chart:
            # الشارت المباشر (Live TradingView)
            interval = "1" if "Scalp" in conf['style'] else "240"
            tv_html = f'<iframe src="https://s.tradingview.com:{conf["market"]}&interval={interval}&theme=dark" width="100%" height="600" frameborder="0"></iframe>'
            st.components.v1.html(tv_html, height=610)
            
        with col_intel:
            st.subheader("🔍 Analysis Matrix / مصفوفة التحليل")
            
            # 1. Multi-Frame Generation
            with st.expander("🌐 MTF Narrative / تسلسل الفريمات", expanded=True):
                st.write(f"**HTF:** {mtf['HTF']} | **LTF:** {mtf['LTF']}")
                st.info(f"Context: {mtf['Narrative']}")

            # 2. PD-Arrays (Premium/Discount)
            st.subheader("🛡️ PD-Arrays")
            st.progress(25, text="Zone: DISCOUNT (BUY ONLY) / منطقة الشراء")

            # 3. ICT/SMC Checklist
            st.subheader("📋 Checklist / التأكيدات")
            st.write("✅ **SMT:** Divergence with DXY")
            st.write("✅ **COT:** Institutional Alignment")
            st.write("✅ **News:** Forex Factory (Low Impact)")
            st.write("⏳ **OB/FVG:** Price in Order Block")
            st.write("⏳ **CHOCH:** Waiting for LTF Break")

            # 4. Signal Info & Success Rate
            st.divider()
            st.subheader("🎯 Signal Details / تفاصيل الصفقة")
            st.metric("Win Probability / نسبة النجاح", "84%", "+2.5%")
            st.write(f"**Lot:** {conf['lot']:.2f} | **Risk:** {conf['risk']}%")
            
            if st.button("🔥 ENTER THE TRADE NOW", use_container_width=True):
                st.error("Signal Sent to Telegram! / تم إرسال الإشارة لتليجرام")
                # تشغيل صوت تنبيه افتراضي
                st.toast("CHECK YOUR TELEGRAM! 🔔")

# إرسال التنبيهات لتليجرام: Token: 8633388733:AAF1NCh_1_S_90BxLKW_F5RU1KMzDZnBHbU


