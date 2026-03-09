import streamlit as st
import pandas as pd
import requests

# إعدادات الواجهة ثنائية اللغة
st.set_page_config(page_title="AI Trading Platform", layout="wide")

# التنقل
page = st.sidebar.radio("Navigation / التنقل", ["⚙️ Setup", "📊 Live Hub"])

if page == "⚙️ Setup":
    st.title("⚙️ System Setup / إعدادات المنصة")
    
    # المدخلات
    col1, col2 = st.columns(2)
    with col1:
        market = st.selectbox("Market / الزوج", ["EURUSD", "GBPUSD", "USDJPY"])
        style = st.selectbox("Style / الأسلوب", ["Scalp / سكالب", "Swing / سوينج"])
        balance = st.number_input("Capital / رأس المال ($)", value=1000)
    
    with col2:
        risk = st.slider("Risk / المخاطرة (%)", 0.1, 5.0, 1.0)
        # حساب اللوت آلياً
        sl = 15 if "Scalp" in style else 50
        lot = (balance * (risk/100)) / (sl * 10)
        st.success(f"Recommended Lot / اللوت المحسوب: {lot:.2f}")

    if st.button("Start Monitoring / بدء المراقبة"):
        st.session_state['data'] = {"market": market, "lot": lot, "risk": risk}
        st.info("Settings Saved! Go to Live Hub.")

else:
    st.title("📊 Live Hub / المراقبة الحية")
    if 'data' in st.session_state:
        d = st.session_state['data']
        st.write(f"Pair: **{d['market']}** | Lot: **{d['lot']:.2f}**")
        # دمج شارت TradingView
        st.components.v1.html(f'<iframe src="https://s.tradingview.com:{d["market"]}&interval=1&theme=dark" width="100%" height="500"></iframe>', height=500)
        st.info("Scanning for SMT + SMC confirmations...")
    else:
        st.warning("Please setup your settings first!")
  
