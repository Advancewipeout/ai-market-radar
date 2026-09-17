import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time
from datetime import datetime
import pytz

# 1. VISUAL INTERFACE & PREMIUM BRANDING
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.metric-box { background-color:#151922; padding:24px; border-radius:14px; border-left:6px solid #6366f1; margin-bottom:20px; border:1px solid #222b3c; }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; }</style>", unsafe_allow_html=True)

clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
st.markdown(f"<div style='background:linear-gradient(135deg,#1e1b4b,#0f172a); padding:30px; border-radius:16px; border:1px solid #312e81; text-align:center;'><h1 style='background:linear-gradient(90deg,#00ffcc,#6366f1,#ff4b4b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; font-size:38px; font-weight:800;'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p style='color:#00ffcc; font-family:monospace; margin:5px 0 0 0; font-weight:600;'>⚡ SYSTEM STATUS: ACTIVE | MATRIX SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

try:
    fx = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
    usd_to_cad = 1.0 / float(fx["Close"].to_numpy().flatten()[-1])
except:
    usd_to_cad = 1.36

market_summary_list = []
asset_data_store = {}

with st.spinner("📥 Synchronizing core market pricing vectors..."):
    for ticker, display_name in watchlist.items():
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
            close_arr = df["Close"].to_numpy().flatten()
            price = float(close_arr[-1])
            if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
            st.session_state.live_prices_cache[ticker] = price
            
            pct = ((price - float(close_arr[-5])) / float(close_arr[-5])) * 100
            target_price = price * (1.0 + (pct * 0.05 / 100))
            stop_long, stop_short = price * 0.975, price * 1.025
            
            if pct > 0.5:
                sig, color = "🟢 STRONG BUY / ENTER LONG", "#00ffcc"
                tp_text, sl_text = f"CAD ${target_price:,.2f}", f"CAD ${stop_long:,.2f}"
            elif pct < -0.5:
                sig, color = "🔴 STRONG SELL / ENTER SHORT", "#ff4b4b"
                tp_text, sl_text = f"CAD ${target_price:,.2f}", f"CAD ${stop_short:,.2f}"
            else:
                sig, color = "🟡 HOLD / WAIT FOR CONFIRMATION", "#ffcc00"
                tp_text, sl_text = "N/A", "N/A"

            market_summary_list.append(f"{ticker} ({display_name}): price=${price:,.2f}, 5day_move={pct:+.2f}%, system_action={sig}, mathematically_calculated_target=${target_price:,.2f}")
            asset_data_store[ticker] = {"display_name": display_name, "price": price, "target": target_price, "pct": pct, "sig": sig, "color": color, "tp": tp_text, "sl": sl_text, "df": df}
        except:
            pass

# 2. BULLETPROOF RAW-TEXT NEURAL PASS WITH DIVISION PARSING
api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
ai_analysis_list = []

if api_key_target != "WIPE" and market_summary_list:
    try:
        from groq import Groq
        client = Groq(api_key=api_key_target)
        
        master_prompt = f"You are an automated portfolio tracking strategy engine. Based on the market data below, write a single direct holding sentence for website viewers following this system. Explain exactly how long the model intends to hold the asset based on current metrics, and at what target price it will execute a sell order. Speak directly to platform users following your trades as a trade tracker guide. You MUST output exactly 6 sentences, with each sentence separated by a single '|' character. Follow the order of the assets listed below. Market data: {', '.join(market_summary_list)}"
        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": master_prompt}]
        )
        # Split the raw text response by the divider symbol safely into our list
        raw_text_response = completion.choices[0].message.content
        ai_analysis_list = [s.strip() for s in raw_text_response.split("|")]
    except:
        pass

# Render grid layout columns cleanly
col1, col2 = st.columns(2)
for index, ticker in enumerate(watchlist.keys()):
    if ticker in asset_data_store:
        data = asset_data_store[ticker]
        
        try:
            txt = ai_analysis_list[index]
            if len(txt) < 5: raise Exception() # Fallback check if splitter mismatched
        except:
            txt = f"The sequential AI layers for {ticker} have locked onto consolidation targets ({data['pct']:+.2f}% velocity change). The model intends to maintain this position for 2 to 4 days, standing by for a sell target breakout toward CAD ${data['target']:,.2f}."

        with col1 if index % 2 == 0 else col2:
            st.markdown(f"""
            <div class='metric-box' style='border-left-color:{data["color"]};'>
                <h2 class='asset-header'>{data["display_name"]}</h2>
                <hr style='border-color:#222b3c;'>
                <p style='font-size:16px;'><b>Current Market Price:</b> CAD ${data["price"]:,.2f}</p>
                <p style='font-size:16px;'><b>Neural Wave Target:</b> CAD ${data["target"]:,.2f} ({data["pct"]:+.2f}%)</p>
                <p style='font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data["color"]}; font-weight:bold;'>{data["sig"]}</span></p>
                <p style='font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {data["tp"]} | 🛑 <b>Stop-Loss Floor:</b> {data["sl"]}</p>
                <div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {txt}</div>
            </div>
            """, unsafe_allow_html=True)
            st.line_chart(pd.DataFrame(data["df"]["Close"].tail(30)))

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
            if api_key_target == "WIPE":
                ai_reply = f"Live feed status: {ctx_data} Setup your Groq Key to unleash unscripted deep learning conversations!"
                if "bitcoin" in q or "btc" in q: ai_reply = f"The live price of Bitcoin is currently **${p_map.get('BTC-CAD',0):,.2f} CAD**."
                if "ethereum" in q or "eth" in q: ai_reply = f"The live price of Ethereum is currently **${p_map.get('ETH-CAD',0):,.2f} CAD**."
                if "stop loss" in q: ai_reply = "A Stop-Loss acts as an automated protective floor price order to secure investment capital."
            else:
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key_target)
                    completion = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "system", "content": f"You are an expert financial analyst. Answer user questions naturally. Live data: {ctx_data}. Max 2 short sentences."}, {"role": "user", "content": user_input_text}])
                    ai_reply = completion.choices[0].message.content
                except Exception as e: ai_reply = f"Neural handshake lag: {e}"
            st.write(ai_reply)
            st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
            st.rerun()

time.sleep(30)
st.rerun()
