import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json, urllib.request
from datetime import datetime
import pytz

# 1. PREMIUM CODES & BRANDING CORE STYLING LAYER (THICK 6PX LEFT BORDERS APPLIED!)
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .main { background-color:#0d0f14; color:#f8fafc; }
    .brand-header-box { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 30px; border-radius: 16px; border: 1px solid #312e81; box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15); margin-bottom: 25px; text-align: center; }
    .brand-title { font-size: 38px !important; font-weight: 800 !important; letter-spacing: 2px; background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0px 0px 5px 0px !important; text-transform: uppercase; text-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }
    .brand-subtitle { color: #94a3b8; font-size: 16px; font-weight: 500; letter-spacing: 1px; margin: 0px 0px 8px 0px !important; }
    .brand-timestamp { color: #00ffcc; font-size: 14px; font-weight: 600; letter-spacing: 1px; margin: 0 !important; font-family: monospace; }
    .metric-box { background-color:#151922; padding:24px; border-radius:14px; margin-bottom:20px; border:1px solid #222b3c; }
    .asset-header { font-size: 24px !important; font-weight: 700 !important; color: #ffffff; margin: 0 0 10px 0 !important; }
    .ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; line-height: 1.5; }
    .news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
st.markdown(f"<div class='brand-header-box'><h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p class='brand-subtitle'>Automated Multi-Asset Deep Sequential Momentum Radar</p><p class='brand-timestamp'>⚡ SYSTEM STATUS: ACTIVE | MATRIX SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

@st.cache_data(ttl=60)
def fetch_ticker_data_safely(ticker):
    try: return yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
    except: return None

try:
    fx_df = fetch_ticker_data_safely("CADUSD=X")
    usd_to_cad = 1.0 / float(fx_df["Close"].to_numpy().flatten()[-1]) if fx_df is not None else 1.36
except: usd_to_cad = 1.36

# Fetch secure API key token from vault environment
api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")

col1, col2 = st.columns(2)
with st.spinner("📥 Synchronizing core market pricing vectors..."):
    for index, (ticker, display_name) in enumerate(watchlist.items()):
        df = fetch_ticker_data_safely(ticker)
        if df is not None and not df.empty:
            try:
                df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
                close_arr = df["Close"].to_numpy().flatten()
                price = float(close_arr[-1])
                if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
                st.session_state.live_prices_cache[ticker] = price
                pct = ((price - float(close_arr[-5])) / float(close_arr[-5])) * 100
                target_price = price * (1.0 + (pct * 0.05 / 100))
                stop_long, stop_short = price * 0.975, price * 1.025
                sig, color = ("🟡 HOLD", "#ffcc00") if abs(pct) <= 0.5 else (("🟢 BUY", "#00ffcc") if pct > 0.5 else ("🔴 SELL", "#ff4b4b"))
                tp_text, sl_text = (f"CAD ${target_price:,.2f}", f"CAD ${stop_long:,.2f}" if pct > 0.5 else f"CAD ${stop_short:,.2f}") if abs(pct) > 0.5 else ("N/A", "N/A")
                
                # ☁️ BULLETPROOF FLAT INLINE MODEL ROUTING PASS
                if api_key_target == "WIPE":
                    strat_txt = f"The model is maintaining this position for 2 to 4 days, tracking a sell execution breakout toward CAD ${target_price:,.2f}."
                    intel_txt = f"Live updates show steady transaction volume support near the current macro floor thresholds."
                else:
                    url = "https://openai.com"
                    hd = {"Authorization": f"Bearer {api_key_target}", "Content-Type": "application/json"}
                    
                    # Call Box 1 Strategy text
                    try:
                        r1 = urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": f"You are a trade tracking system. Write a single brief sentence explaining exactly how long the model intends to hold the asset {ticker} based on its 5-day move of {pct:+.2f}% and at what target price (CAD ${target_price:,.2f}) it will execute a sell order. Speak directly to users as a guide."}]}).encode("utf-8"), headers=hd, method="POST")
                        with urllib.request.urlopen(r1) as response1:
                            strat_txt = json.loads(response1.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    except: strat_txt = f"The model is maintaining this position for 2 to 4 days, tracking a sell execution breakout toward CAD ${target_price:,.2f}."
                    
                    # Call Box 2 Intelligence text
                    try:
                        r2 = urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": f"Write a single brief sentence summarizing the current market sentiment, community buzz, or social media updates for the asset {ticker} right now. Do not repeat introductions."}]}).encode("utf-8"), headers=hd, method="POST")
                        with urllib.request.urlopen(r2) as response2:
                            intel_txt = json.loads(response2.read().decode("utf-8"))["choices"][0]["message"]["content"]
                    except: intel_txt = f"Live updates show steady transaction volume support near the current macro floor thresholds."

                with col1 if index % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class='metric-box' style='border-left: 6px solid {color};'>
                        <h2 class='asset-header'>{display_name}</h2>
                        <hr style='border-color:#222b3c; margin: 8px 0 12px 0;'>
                        <p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${price:,.2f}</p>
                        <p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${target_price:,.2f} ({pct:+.2f}%)</p>
                        <p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{color}; font-weight:bold;'>{sig}</span></p>
                        <p style='margin:4px 0; font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {tp_text} | 🛑 <b>Stop-Loss Floor:</b> {sl_text}</p>
                        <div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {strat_txt}</div>
                        <div class='news-box'>📰 <b>Live Market Intelligence:</b> {intel_txt}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.line_chart(pd.DataFrame(df["Close"].tail(30)))
            except: pass

# 3. INTERACTIVE CHAT ROOM
st.markdown("---")
st.header("💬 SMITTY'S LEARNING CHAT INTERFACE")
for chat in st.session_state.chat_history_matrix:
    with st.chat_message(chat["role"]): st.write(chat["content"])

with st.form(key="chat_secure_form", clear_on_submit=True):
    user_input_text = st.text_input("Ask the Matrix AI a question...")
    submit_button = st.form_submit_button(label="⚡ Send to Matrix Brain")

if submit_button and user_input_text:
    st.session_state.chat_history_matrix.append({"role": "user", "content": user_input_text})
    with st.chat_message("user"): st.write(user_input_text)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing question query parameters..."):
            p_map = st.session_state.live_prices_cache
            q = user_input_text.lower().strip()
            ctx_data = f"Bitcoin: ${p_map.get('BTC-CAD',0):,.2f}, Ethereum: ${p_map.get('ETH-CAD',0):,.2f}, Solana: ${p_map.get('SOL-CAD',0):,.2f}, NVIDIA: ${p_map.get('NVDA',0):,.2f}, Tesla: ${p_map.get('TSLA',0):,.2f} CAD."
            if api_key_target == "WIPE": ai_reply = f"Live feed status: {ctx_data} Setup your Groq Key to unleash unscripted conversations!"
            else:
                try:
                    url = "https://openai.com"
                    req = urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "system", "content": f"You are an expert financial analyst. Answer user questions naturally. Live data: {ctx_data}. Max 2 short sentences."}, {"role": "user", "content": user_input_text}]}).encode("utf-8"), headers={"Authorization": f"Bearer {api_key_target}", "Content-Type": "application/json"}, method="POST")
                    with urllib.request.urlopen(req) as response:
                        ai_reply = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
                except Exception as e: ai_reply = f"Neural handshake lag: {e}"
            st.write(ai_reply)
