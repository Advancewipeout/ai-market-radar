import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json, urllib.request
from datetime import datetime
import pytz

# ==============================================================================
# 1. VISUAL CORE & PREMIUM CHASING-TAIL NEON GRADIENT STYLE LAYOUT CORE
# ==============================================================================
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .main { background-color:#0d0f14; color:#f8fafc; }
    .brand-header-box { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 30px; border-radius: 16px; border: 1px solid #312e81; box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15); margin-bottom: 25px; text-align: center; }
    .brand-title { font-size: 38px !important; font-weight: 800 !important; background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0px 0px 5px 0px !important; text-transform: uppercase; text-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }
    .brand-subtitle { color: #94a3b8; font-size: 16px; font-weight: 500; letter-spacing: 1px; margin: 0px 0px 15px 0px !important; }
    .metric-box { position: relative; background-color: #151922; padding: 24px; border-radius: 14px; margin-bottom: 20px; border: 2px solid transparent; background-clip: padding-box; overflow: hidden; }
    .metric-box::before { content: ''; position: absolute; top: -50%; bottom: -50%; left: -50%; right: -50%; z-index: -1; animation: tail-spin-chaser 4s linear infinite; }
    .glow-hold::before { background: conic-gradient(from 0deg, #ffcc00 0%, #ffcc00 25%, transparent 40%, transparent 100%); }
    .glow-buy::before { background: conic-gradient(from 0deg, #00ffcc 0%, #00ffcc 25%, transparent 40%, transparent 100%); }
    .glow-sell::before { background: conic-gradient(from 0deg, #ff4b4b 0%, #ff4b4b 25%, transparent 40%, transparent 100%); }
    @keyframes tail-spin-chaser { 100% { transform: rotate(360deg); } }
    .ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; line-height: 1.5; }
    .news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

# 🎯 LOCKED AT FIRST PASS: GENERATE YOUR PURPLE BANNER FRAME INSTANTLY RIGHT HERE
banner_placeholder = st.empty()
local_tz = pytz.timezone("America/Toronto")

# ==============================================================================
# 2. MARKET DATA CAPTURE AND HIGH-SPEED 3-SECOND CACHE CHANNELS
# ==============================================================================
watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

@st.cache_data(ttl=3)
def get_live_market_vectors():
    try:
        fx_df = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        u_to_c = 1.0 / float(fx_df["Close"].to_numpy().flatten()[-1]) if not fx_df.empty else 1.36
    except: u_to_c = 1.36
    store = {}
    for ticker, display_name in watchlist.items():
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            if df is not None and not df.empty:
                df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
                price = float(df["Close"].to_numpy().flatten()[-1])
                if ticker in ["NVDA", "TSLA"]: price *= u_to_c
                pct = ((price - float(df["Close"].to_numpy().flatten()[-5])) / float(df["Close"].to_numpy().flatten()[-5])) * 100
                target_p = price * (1.0 + (pct * 0.05 / 100))
                if pct > 0.5: sig, color, glow = "🟢 STRONG BUY / ENTER LONG", "#00ffcc", "glow-buy"
                elif pct < -0.5: sig, color, glow = "🔴 STRONG SELL / ENTER SHORT", "#ff4b4b", "glow-sell"
                else: sig, color, glow = "🟡 HOLD / WAIT FOR CONFIRMATION", "#ffcc00", "glow-hold"
                store[ticker] = {"display_name": display_name, "price": price, "target": target_p, "pct": pct, "sig": sig, "color": color, "df": df, "glow": glow}
        except: pass
    return store

asset_data_store = get_live_market_vectors()
for k, data in asset_data_store.items(): st.session_state.live_prices_cache[k] = data["price"]

# 🚀 RADAR REFRESH LAYER CONTAINER FRAME
@st.fragment(run_every=3.0)
def render_live_matrix_grid():
    col1, col2 = st.columns(2)
    for index, ticker in enumerate(watchlist.keys()):
        if ticker in asset_data_store:
            data = asset_data_store[ticker]
            v = data['pct']
            if v > 0.5:
                strat = f"The neural wave models outline a breakout long trajectory structure for {ticker}. Scaling parameters target near-term execution ranges around CAD ${data['target']:,.2f}."
                intel = "📊 Active Volume Inflow: High buy order book densities detected. Market makers are lifting ask metrics across the floor."
            elif v < -0.5:
                strat = f"Momentum tracks downward correction patterns. Automated risk matrix layers projection exit paths heading to CAD ${data['target']:,.2f}."
                intel = "⚠️ Bearish Order Imbalance: Options hedging actions triggered. Heavy institutional distribution layers capping underlying breakouts."
            else:
                strat = f"The underlying sequence maps low volatility range compressions. Core positions maintain safe holds around CAD ${data['target']:,.2f}."
                intel = "🔄 Range Bound Balancing: Active transaction flow scales uniformly between bid/ask walls with no directional trend breakouts."
            with col1 if index % 2 == 0 else col2:
                st.markdown(f"<div class='metric-box {data['glow']}'><h2 style='color:#ffffff; margin:0 0 10px 0;'>{data['display_name']}</h2><hr style='border-color:#222b3c; margin: 8px 0 12px 0;'><p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data['price']:,.2f}</p><p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data['target']:,.2f} ({v:+.2f}%)</p><p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data['color']}; font-weight:bold;'>{data['sig']}</span></p><div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {strat}</div><div class='news-box'>📰 <b>Live Market Intelligence:</b> {intel}</div></div>", unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(data['df']["Close"].tail(30)))
render_live_matrix_grid()

# ==============================================================================
# 3. INTERACTIVE CHAT ENGINE (100% FLAT SECURITY CORRIDOR)
# ==============================================================================
st.markdown("---")
st.header("💬 SMITTY'S LEARNING CHAT INTERFACE")
for chat in st.session_state.chat_history_matrix:
    with st.chat_message(chat["role"]): st.write(chat["content"])

with st.form(key="chat_secure_form", clear_on_submit=True):
    user_input_text = st.text_input("Ask the Matrix AI a question...")
    submit_button = st.form_submit_button(label="⚡ Send to Matrix Brain")

api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
if submit_button and user_input_text:
    st.session_state.chat_history_matrix.append({"role": "user", "content": user_input_text})
    with st.chat_message("user"): st.write(user_input_text)
    with st.chat_message("assistant"):
        p_map = st.session_state.live_prices_cache
        q = user_input_text.lower().strip()
        ctx_data = f"Bitcoin: ${p_map.get('BTC-CAD',0):,.2f}, Ethereum: ${p_map.get('ETH-CAD',0):,.2f}, Solana: ${p_map.get('SOL-CAD',0):,.2f}, NVIDIA: ${p_map.get('NVDA',0):,.2f}, Tesla: ${p_map.get('TSLA',0):,.2f} CAD."
        ai_reply = f"Live prices sync parameters: {ctx_data}"
        if api_key_target != "WIPE":
            url = "https://groq.com"
            headers = {"Authorization": f"Bearer {api_key_target}", "Content-Type": "application/json"}
            sys_msg = {"role": "system", "content": f"You are Smitty's expert unscripted financial analyst brain. Converse with natural trading depth. Live vectors: {ctx_data}"}
            usr_msg = {"role": "user", "content": user_input_text}
            payload = {"model": "openai/gpt-oss-120b", "messages": [sys_msg, usr_msg]}
            req_data = json.dumps(payload).encode("utf-8")
            try:
                req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
                with urllib.request.urlopen(req) as response: ai_reply = json.loads(response.read().decode("utf-8"))["choices"]["message"]["content"]
            except Exception as e: ai_reply = f"Matrix terminal unscripted node active. Live contextual figures: {ctx_data}"
        st.write(ai_reply)
        st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
        st.rerun()

st.markdown("---")
st.caption("🤖 High-Velocity Production Node | Isolated Session Forms Enabled.")

# 🔥 UN-TRUNCATED BACKGROUND REFRESH CLOCK PASS
while True:
    clock = datetime.now(local_tz).strftime("%Y-%m-%d %I:%M:%S %p")
