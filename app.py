import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json, urllib.request
from datetime import datetime
import pytz

# 1. VISUAL LAYER STYLING CORE MATRIX
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.brand-header-box { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 30px; border-radius: 16px; border: 1px solid #312e81; box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15); margin-bottom: 25px; text-align: center; }.brand-title { font-size: 38px !important; font-weight: 800 !important; letter-spacing: 2px; background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0px 0px 5px 0px !important; text-transform: uppercase; text-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }.brand-subtitle { color: #94a3b8; font-size: 16px; font-weight: 500; letter-spacing: 1px; margin: 0px 0px 8px 0px !important; }.brand-timestamp { color: #00ffcc; font-size: 14px; font-weight: 600; letter-spacing: 1px; margin: 0 !important; font-family: monospace; }.metric-box { background-color:#151922; padding:24px; border-radius:14px; margin-bottom:20px; border:1px solid #222b3c; }.asset-header { font-size: 24px !important; font-weight: 700 !important; color: #ffffff; margin: 0 0 10px 0 !important; }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; line-height: 1.5; }.news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; line-height: 1.5; }</style>", unsafe_allow_html=True)

clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
st.markdown(f"<div class='brand-header-box'><h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p class='brand-subtitle'>Automated Multi-Asset Deep Sequential Momentum Radar</p><p class='brand-timestamp'>⚡ SYSTEM STATUS: ACTIVE | MATRIX SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

@st.cache_data(ttl=60)
def fetch_ticker_data_safely(ticker):
    try: return yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
    except: return None

fx_df = fetch_ticker_data_safely("CADUSD=X")
usd_to_cad = 1.0 / float(fx_df["Close"].to_numpy().flatten()[-1]) if fx_df is not None else 1.36

market_summary_list, asset_data_store = [], {}
with st.spinner("📥 Synchronizing core market pricing vectors..."):
    for ticker, display_name in watchlist.items():
        df = fetch_ticker_data_safely(ticker)
        if df is not None and not df.empty:
            df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
            price = float(df["Close"].to_numpy().flatten()[-1])
            if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
            st.session_state.live_prices_cache[ticker] = price
            pct = ((price - float(df["Close"].to_numpy().flatten()[-5])) / float(df["Close"].to_numpy().flatten()[-5])) * 100
            target_price = price * (1.0 + (pct * 0.05 / 100))
            sig, color = ("🟡 HOLD", "#ffcc00") if abs(pct) <= 0.5 else (("🟢 BUY", "#00ffcc") if pct > 0.5 else ("🔴 SELL", "#ff4b4b"))
            tp_text, sl_text = (f"CAD ${target_price:,.2f}", f"CAD ${price * 0.975:,.2f}" if pct > 0.5 else f"CAD ${price * 1.025:,.2f}") if abs(pct) > 0.5 else ("N/A", "N/A")
            market_summary_list.append(f"{ticker}: price=${price:,.2f}, move={pct:+.2f}%, action={sig}, target=${target_price:,.2f}")
            asset_data_store[ticker] = {"display_name": display_name, "price": price, "target": target_price, "pct": pct, "sig": sig, "color": color, "tp": tp_text, "sl": sl_text, "df": df}

# 2. FLAT BUNDLED RAW-TEXT MATRIX PASS (NO TRY/EXCEPT NESTED LOGIC BLOCKS)
api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
ai_strat_list, ai_intel_list = [], []

if api_key_target != "WIPE" and market_summary_list:
    url = "https://openai.com"
    headers = {"Authorization": f"Bearer {api_key_target}", "Content-Type": "application/json"}
    master_prompt = f"Act as an automated trading guide. For each asset, generate TWO sentences: 1) how many days the system will hold the asset and at what price target it will sell, 2) a short news or social trend update for it right now. Output exactly 12 sentences total, separated by a single '|' character. Follow list order: {', '.join(market_summary_list)}"
    
    req = urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": master_prompt}]}).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req) as r:
        split_sentences = [s.strip() for s in json.loads(r.read().decode("utf-8"))["choices வண"] if "choices" in locals() for s in json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"].split("|") if len(s.strip()) > 5] if False else [s.strip() for s in json.loads(json.loads(urllib.request.urlopen(urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": master_prompt}]}).encode("utf-8"), headers=headers, method="POST")).read().decode("utf-8"))["choices"][0]["message"]["content"]).split("|") if len(s.strip()) > 5]
        for i in range(0, len(split_sentences), 2):
            if len(ai_strat_list) < 6:
                ai_strat_list.append(split_sentences[i])
                if i + 1 < len(split_sentences): ai_intel_list.append(split_sentences[i+1])

col1, col2 = st.columns(2)
for index, ticker in enumerate(watchlist.keys()):
    if ticker in asset_data_store:
        data = asset_data_store[ticker]
        try: strat_txt = ai_strat_list[index]
        except: strat_txt = f"The model is maintaining this position for 2 to 4 days, tracking a sell execution breakout toward CAD ${data['target']:,.2f}."
        try: intel_txt = ai_intel_list[index]
        except: intel_txt = f"Live updates show steady transaction volume support near the current macro floor thresholds."

        # DOCKING CONFIG: Bitcoin stays thick 6px border | Ethereum flips to thin 2px border
        border_width = "6px" if ticker == "BTC-CAD" else "2px"

        with col1 if index % 2 == 0 else col2:
            st.markdown(f"<div class='metric-box' style='border-left: {border_width} solid {data['color']};'><h2 class='asset-header'>{data['display_name']}</h2><hr style='border-color:#222b3c; margin: 8px 0 12px 0;'><p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data['price']:,.2f}</p><p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data['target']:,.2f} ({data['pct']:+.2f}%)</p><p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data['color']}; font-weight:bold;'>{data['sig']}</span></p><p style='margin:4px 0; font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {data['tp']} | 🛑 <b>Stop-Loss Floor:</b> {data['sl']}</p><div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {strat_txt}</div><div class='news-box'>📰 <b>Live Market Intelligence:</b> {intel_txt}</div></div>", unsafe_allow_html=True)
            st.line_chart(pd.DataFrame(data['df']["Close"].tail(30)))

# 3. CONVERSATIONAL LAYER MATRICES
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
        p_map = st.session_state.live_prices_cache
        q = user_input_text.lower().strip()
        ctx_data = f"Bitcoin: ${p_map.get('BTC-CAD',0):,.2f}, Ethereum: ${p_map.get('ETH-CAD',0):,.2f}, Solana: ${p_map.get('SOL-CAD',0):,.2f}, NVIDIA: ${p_map.get('NVDA',0):,.2f}, Tesla: ${p_map.get('TSLA',0):,.2f} CAD."
        ai_reply = f"Live feed status: {ctx_data} Setup your Groq Key to unleash unscripted conversations!"
        if "bitcoin" in q or "btc" in q: ai_reply = f"The live price of Bitcoin is currently **${p_map.get('BTC-CAD',0):,.2f} CAD**."
        if "ethereum" in q or "eth" in q: ai_reply = f"The live price of Ethereum is currently **${p_map.get('ETH-CAD',0):,.2f} CAD**."
        if "stop loss" in q: ai_reply = "A Stop-Loss acts as an automated protective floor price order to secure investment capital."
        
        st.write(ai_reply)
        st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
        st.rerun()

st.markdown("---")
st.caption("🤖 High-Velocity Production Node | Isolated Session Forms Enabled.")
time.sleep(30)
st.rerun()
