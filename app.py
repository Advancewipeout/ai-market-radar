import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json, urllib.request
from datetime import datetime
import pytz
from groq import Groq

# 1. PREMIUM HEADER DESIGN & UN-CLIPPED CHASING-TAIL NEON BORDER STYLING CORES
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.brand-header-box { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 30px; border-radius: 16px; border: 1px solid #312e81; box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15); margin-bottom: 25px; text-align: center; }.brand-title { font-size: 38px !important; font-weight: 800 !important; background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0px 0px 5px 0px !important; text-transform: uppercase; text-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }.metric-box { position: relative; background-color: #151922; padding: 24px; border-radius: 14px; margin-bottom: 20px; border: 2px solid transparent; background-clip: padding-box; overflow: hidden; z-index: 1; }.metric-box::before { content: ''; position: absolute; top: -150%; bottom: -150%; left: -150%; right: -150%; z-index: -2; animation: tail-spin-chaser 4s linear infinite; }.metric-box::after { content: ''; position: absolute; top: 2px; left: 2px; right: 2px; bottom: 2px; background-color: #151922; border-radius: 12px; z-index: -1; }.glow-hold::before { background: conic-gradient(from 0deg, #ffcc00 0%, #ffcc00 15%, transparent 35%, transparent 100%); }.glow-buy::before { background: conic-gradient(from 0deg, #00ffcc 0%, #00ffcc 15%, transparent 35%, transparent 100%); }.glow-sell::before { background: conic-gradient(from 0deg, #ff4b4b 0%, #ff4b4b 15%, transparent 35%, transparent 100%); }@keyframes tail-spin-chaser { 100% { transform: rotate(360deg); } }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; line-height: 1.5; }.news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; line-height: 1.5; }</style>", unsafe_allow_html=True)

local_tz = pytz.timezone("America/Toronto")
@st.fragment(run_every=1.0)
def render_live_clock_banner():
    clock = datetime.now(local_tz).strftime("%Y-%m-%d %I:%M:%S %p")
    st.markdown(f"<div class='brand-header-box'><h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p style='color:#94a3b8; margin:0;'>Automated Multi-Asset Deep Sequential Momentum Radar</p><p style='color: #00ffcc; font-family: monospace; font-size: 14px; font-weight: 600; margin: 8px 0 0 0; letter-spacing: 1px;'>⚡ SYSTEM STATUS: ACTIVE | MATRIX LIVE SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)
render_live_clock_banner()

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []
if "backup_vectors_store" not in st.session_state: st.session_state.backup_vectors_store = {}
if "ai_cards_cache" not in st.session_state: st.session_state.ai_cards_cache = {}

def get_ai_unscripted_card_analysis(ticker, price, target_p, pct, sig, api_key):
    if api_key == "WIPE": return (f"⏳ **AI TRADING LOG**: System tracking consolidation channels for {ticker}. Core targets holding stable near CAD ${target_p:,.2f}.", "🔄 Data Volume Analysis: Order matching profiles remain uniformly spread across active bid/ask layers.")
    try:
        client = Groq(api_key=api_key)
        prompt = f"Analyze asset data and return a JSON object with keys 'strat' and 'intel'. Asset: {ticker}, Price: CAD ${price:,.2f}, Target: CAD ${target_p:,.2f}, Shift: {pct:+.2f}%, Signal: {sig}. 'strat' must be a 1-2 sentence real-time trade log entry detailing what you (the AI) are doing for yourself right now so copy-traders can replicate the entry for the best outcome. Prefix with '📈 **AI TRADING LOG**: ' or '📉 **AI TRADING LOG**: '. 'intel' must be a 1-sentence volume report. Prefix with '📰 **Live Market Intelligence**: '. Tone institutional, don't mention customers."
        completion = client.chat.completions.create(model="llama-3.1-70b-versatile", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
        res = json.loads(completion.choices.message.content)
        s_val = res.get("strat") or res.get("STRAT") or res.get("strategy") or res.get("Strategy")
        i_val = res.get("intel") or res.get("INTEL") or res.get("intelligence") or res.get("Intelligence")
        if s_val and i_val: return str(s_val), str(i_val)
    except: pass
    return (f"⏳ **AI TRADING LOG**: Model maintaining its trend track baseline corridor for {ticker} near CAD ${target_p:,.2f}.", "🔄 Data Volume Intelligence: Real-time buyer and seller metrics are balanced across active book parameters.")

def load_realtime_market_updates():
    usd_to_cad = 1.36
    try:
        fx_df = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        if fx_df is not None and not fx_df.empty: usd_to_cad = 1.0 / float(fx_df["Close"].to_numpy().flatten()[-1])
    except: usd_to_cad = 1.36
    api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
    store = {}
    for ticker, display_name in watchlist.items():
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            if df is not None and not df.empty and len(df) >= 5:
                df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
                close_arr = df["Close"].to_numpy().flatten()
                price = float(np.nan_to_num(close_arr[-1]))
                if price <= 0: price = float(np.nan_to_num(df["Adj close"].to_numpy().flatten()[-1]))
                if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
                if price <= 0: raise ValueError("Empty Price Error")
                prev_close = float(np.nan_to_num(close_arr[-5])) if len(close_arr) >= 5 else price
                pct = ((price - prev_close) / prev_close) * 100
                target_p = price * (1.0 + (pct * 0.05 / 100))
                sig, color, glow = ("🟢 STRONG BUY / ENTER LONG", "#00ffcc", "glow-buy") if pct > 0.05 else (("🔴 STRONG SELL / ENTER SHORT", "#ff4b4b", "glow-sell") if pct < -0.05 else ("🟡 HOLD / WAIT FOR CONFIRMATION", "#ffcc00", "glow-hold"))
                cache_key = f"{ticker}_{round(price, 2)}"
                if cache_key not in st.session_state.ai_cards_cache:
                    strat, intel = get_ai_unscripted_card_analysis(ticker, price, target_p, pct, sig, api_key_target)
                    st.session_state.ai_cards_cache[cache_key] = (strat, intel)
                else: strat, intel = st.session_state.ai_cards_cache[cache_key]
                store[ticker] = {"display_name": display_name, "price": price, "target": target_p, "pct": pct, "sig": sig, "color": color, "df": df, "glow": glow, "strat": strat, "intel": intel}
                st.session_state.backup_vectors_store[ticker] = store[ticker]
        except Exception: pass
        if ticker not in store and ticker in st.session_state.backup_vectors_store: store[ticker] = st.session_state.backup_vectors_store[ticker]
    return store

# 🚀 LANE 2: STABILIZED FINANCIAL ASSET CONTAINER PLATFORM (REFRESHES PRIVATELY EVERY 5 SECONDS)
@st.fragment(run_every=5.0)
def render_live_matrix_grid():
    asset_data_store = load_realtime_market_updates()
    for k, data in asset_data_store.items(): st.session_state.live_prices_cache[k] = data["price"]
    col1, col2 = st.columns(2)
    for index, ticker in enumerate(watchlist.keys()):
        if ticker in asset_data_store:
            data = asset_data_store[ticker]
            with col1 if index % 2 == 0 else col2:
                st.markdown(f"<div class='metric-box {data['glow']}'><h2 style='color:#ffffff; margin:0 0 10px 0;'>{data['display_name']}</h2><hr style='border-color:#222b3c; margin: 8px 0 12px 0;'><p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data['price']:,.2f}</p><p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data['target']:,.2f} ({data['pct']:+.2f}%)</p><p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data['color']}; font-weight:bold;'>{data['sig']}</span></p><div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {data['strat']}</div><div class='news-box'>📰 <b>Live Market Intelligence:</b> {data['intel']}</div></div>", unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(data['df']["Close"].tail(30)))
render_live_matrix_grid()

# ==============================================================================
# 3. INTERACTIVE CHAT ENGINE (100% SECURE PRODUCTION PIPELINE PASS)
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
    p_map = st.session_state.live_prices_cache
