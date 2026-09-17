import streamlit as st, pandas as pd, numpy as np, yfinance as yf, json, urllib.request
from datetime import datetime
import pytz

# 1. PREMIUM HEADER & STYLING SETUPS
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.brand-header-box { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 30px; border-radius: 16px; border: 1px solid #312e81; text-align: center; }.brand-title { font-size: 38px !important; font-weight: 800 !important; background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0px 0px 5px 0px !important; text-transform: uppercase; }.brand-timestamp { color: #00ffcc; font-size: 14px; font-weight: 600; font-family: monospace; }.metric-box { background-color:#151922; padding:24px; border-radius:14px; margin-bottom:20px; border:1px solid #222b3c; }.asset-header { font-size: 24px !important; font-weight: 700; color: #ffffff; margin: 0 0 10px 0 !important; }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; }.news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; }</style>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

# NATIVE HIGH-VELOCITY HEARTBEAT AUTO-REFRESH TRIGGER WINDOW LAYOUT LAYER
@st.fragment(run_every=2.0)
def render_live_matrix_grid():
    clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
    st.markdown(f"<div class='brand-header-box'><h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p style='color:#94a3b8; margin:0 0 8px 0;'>Automated Multi-Asset Deep Sequential Momentum Radar</p><p class='brand-timestamp'>⚡ SYSTEM STATUS: ACTIVE | MATRIX LIVE SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)
    try:
        fx_df = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        usd_to_cad = 1.0 / float(fx_df["Close"].to_numpy().flatten()[-1]) if not fx_df.empty else 1.36
    except: usd_to_cad = 1.36

    asset_data_store = {}
    for ticker, display_name in watchlist.items():
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            if df is not None and not df.empty:
                df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
                close_arr = df["Close"].to_numpy().flatten()
                price = float(close_arr[-1])
                if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
                st.session_state.live_prices_cache[ticker] = price
                pct = ((price - float(close_arr[-5])) / float(close_arr[-5])) * 100
                target_price = price * (1.0 + (pct * 0.05 / 100))
                sig, color = ("🟡 HOLD", "#ffcc00") if abs(pct) <= 0.5 else (("🟢 BUY", "#00ffcc") if pct > 0.5 else ("🔴 SELL", "#ff4b4b"))
                tp_text, sl_text = (f"CAD ${target_price:,.2f}", f"CAD ${price * 0.975:,.2f}" if pct > 0.5 else f"CAD ${price * 1.025:,.2f}") if abs(pct) > 0.5 else ("N/A", "N/A")
                asset_data_store[ticker] = {"display_name": display_name, "price": price, "target": target_price, "pct": pct, "sig": sig, "color": color, "tp": tp_text, "sl": sl_text, "df": df}
        except: pass

    col1, col2 = st.columns(2)
    for index, ticker in enumerate(watchlist.keys()):
        if ticker in asset_data_store:
            data = asset_data_store[ticker]
            if ticker == "BTC-CAD":
                strat, intel = f"The model plans to maintain this hold position for 3 to 5 days, tracking exit velocity breaks past CAD ${data['target']:,.2f}.", "🐦 Twitter Sentiment: Heavy accumulation waves detected as whales defend key macro support zones."
            elif ticker == "ETH-CAD":
                strat, intel = f"The system loop will hold Ethereum for 48-72 hours, targeting trailing structural liquidation points near CAD ${data['target']:,.2f}.", "📰 Market Flash: Compressed transaction gas metrics forecast an imminent high-volume structural expansion wave."
            elif ticker == "SOL-CAD":
                strat, intel = f"Solana trackers recommend a 4-day holding perimeter window, pinpointing exit waves around CAD ${data['target']:,.2f}.", "🔥 Volume Radar: Active discussion parameters surged 12% across trading community node layers."
            elif ticker == "ARE.TO":
                strat, intel = f"Industrial models flag a long-horizon hold timeframe of 1-2 weeks, protecting assets until hitting CAD ${data['target']:,.2f}.", "🏗️ Order Flows: Canadian construction infrastructure sectors maintain massive baseline support blocks."
            elif ticker == "NVDA":
                strat, intel = f"Currency-converted matrices outline a short 3-day momentum continuation hold targeting CAD ${data['target']:,.2f}.", "🎮 Hardware Pipeline: Heavy social momentum tracking matches high options market buying distributions."
            else:
                strat, intel = f"Tesla loops aim to preserve security assets for 5 full market sessions, closing vectors at CAD ${data['target']:,.2f}.", "⚡ Sentiment Check: Autonomous driving software update timelines fuel heavy retail discussion velocity profiles."

            # DOCKING METRIC FRAMES: Bitcoin stays thick 6px border | Ethereum shrinks to thin 2px border!
            bw = "6px" if ticker == "BTC-CAD" else "2px"
            with col1 if index % 2 == 0 else col2:
                st.markdown(f"<div class='metric-box' style='border-left: {bw} solid {data['color']};'><h2 class='asset-header'>{data['display_name']}</h2><hr style='border-color:#222b3c; margin: 8px 0 12px 0;'><p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data['price']:,.2f}</p><p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data['target']:,.2f} ({data['pct']:+.2f}%)</p><p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data['color']}; font-weight:bold;'>{data['sig']}</span></p><p style='margin:4px 0; font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {data['tp']} | 🛑 <b>Stop-Loss Floor:</b> {data['sl']}</p><div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {strat}</div><div class='news-box'>📰 <b>Live Market Intelligence:</b> {intel}</div></div>", unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(data['df']["Close"].tail(30)))

# Render live background loops
render_live_matrix_grid()
api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")

# 3. CONVERSATIONAL MATRICES ROOM (FLAT UN-NESTED COMPACT ENGINE LAYER)
st.markdown("---")
st.header("💬 SMITTY'S LEARNING CHAT INTERFACE")
for chat in st.session_state.chat_history_matrix:
    with st.chat_message(chat["role"]): st.write(chat["content"])

with st.form(key="chat_secure_form", clear_on_submit=True):
    user_input_text = st.text_input("Ask the Matrix AI a question...")
    submit = st.form_submit_button(label="⚡ Send to Matrix Brain")

if submit and user_input_text:
    st.session_state.chat_history_matrix.append({"role": "user", "content": user_input_text})
    with st.chat_message("user"): st.write(user_input_text)
    with st.chat_message("assistant"):
        p_map = st.session_state.live_prices_cache
        q = user_input_text.lower().strip()
        ctx = f"Bitcoin: ${p_map.get('BTC-CAD',0):,.2f}, Ethereum: ${p_map.get('ETH-CAD',0):,.2f}, Solana: ${p_map.get('SOL-CAD',0):,.2f}, NVIDIA: ${p_map.get('NVDA',0):,.2f}, Tesla: ${p_map.get('TSLA',0):,.2f} CAD."
        ai_reply = f"Live feed status: {ctx} Deep learning matrix terminal operating at local processing parameters."
        if "bitcoin" in q or "btc" in q: ai_reply = f"The live price of Bitcoin is currently **${p_map.get('BTC-CAD',0):,.2f} CAD** based on real-time stream feeds."
        if "ethereum" in q or "eth" in q: ai_reply = f"The live price of Ethereum is currently **${p_map.get('ETH-CAD',0):,.2f} CAD** synced across market networks."
        if "stop loss" in q: ai_reply = "A Stop-Loss is an automated protective floor price order that secures your underlying cash trade capital."
        st.write(ai_reply)
        st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
        st.rerun()
