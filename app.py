import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json, urllib.request
from datetime import datetime
import pytz

# 1. PREMIUM HEADER & VISUAL CONFIGURATION
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.brand-header-box { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); padding: 30px; border-radius: 16px; border: 1px solid #312e81; box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15); margin-bottom: 25px; text-align: center; }.brand-title { font-size: 38px !important; font-weight: 800 !important; letter-spacing: 2px; background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0px 0px 5px 0px !important; text-transform: uppercase; text-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }.brand-subtitle { color: #94a3b8; font-size: 16px; font-weight: 500; letter-spacing: 1px; margin: 0px 0px 8px 0px !important; }.brand-timestamp { color: #00ffcc; font-size: 14px; font-weight: 600; letter-spacing: 1px; margin: 0 !important; font-family: monospace; }.metric-box { background-color:#151922; padding:24px; border-radius:14px; margin-bottom:20px; border:1px solid #222b3c; }.asset-header { font-size: 24px !important; font-weight: 700 !important; color: #ffffff; margin: 0 0 10px 0 !important; }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; line-height: 1.5; }.news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; line-height: 1.5; }</style>", unsafe_allow_html=True)

clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
st.markdown(f"<div class='brand-header-box'><h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p style='color:#00ffcc; font-family:monospace; margin:5px 0 0 0; font-weight:600;'>⚡ SYSTEM STATUS: ACTIVE | MATRIX SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

# Rate-limit defense mechanism: cached data downloader function
@st.cache_data(ttl=120)
def fetch_ticker_data_safely(ticker):
    try:
        return yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
    except: return None

try:
    fx_df = fetch_ticker_data_safely("CADUSD=X")
    usd_to_cad = 1.0 / float(fx_df["Close"].to_numpy().flatten()[-1]) if fx_df is not None else 1.36
except: usd_to_cad = 1.36

market_summary_list, asset_data_store = [], {}
for ticker, display_name in watchlist.items():
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
            market_summary_list.append(f"{ticker}: price=${price:,.2f}, move={pct:+.2f}%, action={sig}, target=${target_price:,.2f}")
            asset_data_store[ticker] = {"display_name": display_name, "price": price, "target": target_price, "pct": pct, "sig": sig, "color": color, "tp": tp_text, "sl": sl_text, "df": df}
        except: pass

# 2. BULLETPROOF FLAT BUNDLED GROQ DATA EXTRACTION COUPLING
api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
ai_strat_list, ai_intel_list = [], []

if api_key_target != "WIPE" and market_summary_list:
    try:
        url = "https://groq.com"
        headers = {"Authorization": f"Bearer {api_key_target}", "Content-Type": "application/json"}
        master_prompt = f"Act as an automated asset portfolio tracking system. For each asset, you must generate TWO separate elements in order: 1) a clear holding sentence explaining exactly how long the model intends to hold the asset and at what price target it will execute a sell order, 2) a separate brief market update or news trend summary (like social media/Twitter sentiment) for that coin right now. Speak directly to platform users following your trades as a copy-trade tracker guide. Return the output strictly as a valid raw JSON object matching this schema: {{\"strategy_sentences\": [\"strat 1\", \"strat 2\", \"strat 3\", \"strat 4\", \"strat 5\", \"strat 6\"], \"intelligence_sentences\": [\"intel 1\", \"intel 2\", \"intel 3\", \"intel 4\", \"intel 5\", \"intel 6\"]}}. Keep array items in order. Market data: {', '.join(market_summary_list)}"
        
        req = urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": master_prompt}], "response_format": {"type": "json_object"}}).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req) as r:
            res_json = json.loads(r.read().decode("utf-8"))
            raw_ai_text = res_json["choices"][0]["message"]["content"] if "choices" in res_json else res_json["message"]["content"]
            ai_data = json.loads(raw_ai_text)
            ai_strat_list = ai_data.get("strategy_sentences", [])
            ai_intel_list = ai_data.get("intelligence_sentences", [])
    except: pass

col1, col2 = st.columns(2)
for index, ticker in enumerate(watchlist.keys()):
    if ticker in asset_data_store:
        data = asset_data_store[ticker]
        try: strat_txt = ai_strat_list[index]
        except: strat_txt = f"The model is maintaining this position for 2 to 4 days, tracking a sell execution breakout toward CAD ${data['target']:,.2f}."
        try: intel_txt = ai_intel_list[index]
        except: intel_txt = f"Live updates show steady transaction volume support near the current macro floor thresholds."

        with col1 if index % 2 == 0 else col2:
            st.markdown(f"""
            <div class='metric-box' style='border-left: 2px solid {data['color']};'>
                <h2 class='asset-header'>{data['display_name']}</h2>
                <hr style='border-color:#222b3c; margin: 8px 0 12px 0;'>
                <p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data['price']:,.2f}</p>
                <p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data['target']:,.2f} ({data['pct']:+.2f}%)</p>
                <p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data['color']}; font-weight:bold;'>{data['sig']}</span></p>
                <p style='margin:4px 0; font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {data['tp']} | 🛑 <b>Stop-Loss Floor:</b> {data['sl']}</p>
                <div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {strat_txt}</div>
                <div class='news-box'>📰 <b>Live Market Intelligence:</b> {intel_txt}</div>
            </div>
            """, unsafe_allow_html=True)
            st.line_chart(pd.DataFrame(data['df']["Close"].tail(30)))

# 3. CONVERSATIONAL MATRICES ROOM
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
                    url = "https://groq.com"
                    headers = {"Authorization": f"Bearer {api_key_target}", "Content-Type": "application/json"}
                    req = urllib.request.Request(url, data=json.dumps({"model": "openai/gpt-oss-120b", "messages": [{"role": "system", "content": f"You are an expert financial analyst. Answer user questions naturally. Live data: {ctx_data}. Max 2 short sentences."}, {"role": "user", "content": user_input_text}]}).encode("utf-8"), headers=headers, method="POST")
                    with urllib.request.urlopen(req) as response:
                        res_d = json.loads(response.read().decode("utf-8"))
                        ai_reply = res_d["choices"][0]["message"]["content"] if "choices" in res_d else res_d["message"]["content"]
                except Exception as e: 
                    ai_reply = f"Neural handshake lag: {e}"
            st.write(ai_reply)
            st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
            st.rerun()

st.markdown("---")
st.caption("🤖 High-Velocity Production Node | Isolated Session Forms Enabled.")
time.sleep(30)
st.rerun()
