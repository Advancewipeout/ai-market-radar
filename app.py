import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time
from datetime import datetime
import pytz

# 1. VISUAL INTERFACE & PREMIUM BRANDING
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.metric-box { background-color:#151922; padding:24px; border-radius:14px; border-left:6px solid #6366f1; margin-bottom:20px; border:1px solid #222b3c; }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; }</style>", unsafe_allow_html=True)

clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
st.markdown(f"<div style='background:linear-gradient(135deg,#1e1b4b,#0f172a); padding:30px; border-radius:16px; border:1px solid #312e81; text-align:center;'><h1 style='background:linear-gradient(90deg,#00ffcc,#6366f1,#ff4b4b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; font-size:38px; font-weight:800;'>🌐 ADVANCE AI MATRIX SYSTEM</h1><p style='color:#00ffcc; font-family:monospace; margin:5px 0 0 0; font-weight:600;'>⚡ SYSTEM STATUS: ACTIVE | MATRIX SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 BTC-CAD (Bitcoin)", "ETH-CAD": "💎 ETH-CAD (Ethereum)", "SOL-CAD": "☀️ SOL-CAD (Solana)", "ARE.TO": "🏗️ ARE.TO (Aecon Group)", "NVDA": "🎮 NVDA (NVIDIA Corp)", "TSLA": "⚡ TSLA (Tesla Inc)"}
if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []

col1, col2 = st.columns(2)
try:
    fx = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
    usd_to_cad = 1.0 / float(fx["Close"].to_numpy().flatten()[-1])
except:
    usd_to_cad = 1.36

with st.spinner("📥 Synchronizing core market pricing vectors..."):
    for index, (ticker, display_name) in enumerate(watchlist.items()):
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
            close_arr = df["Close"].to_numpy().flatten()
            price = float(close_arr[-1])
            if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
            st.session_state.live_prices_cache[ticker] = price
            
            # Momentum Velocity Strategy Logic
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

            txt = f"The sequential momentum layers for {ticker} have detected structural consolidation parameters ({pct:+.2f}% velocity change)."

            with col1 if index % 2 == 0 else col2:
                st.markdown(f"""
                <div class='metric-box' style='border-left-color:{color};'>
                    <h2 class='asset-header'>{display_name}</h2>
                    <hr style='border-color:#222b3c;'>
                    <p style='font-size:16px;'><b>Current Market Price:</b> CAD ${price:,.2f}</p>
                    <p style='font-size:16px;'><b>Neural Wave Target:</b> CAD ${target_price:,.2f} ({pct:+.2f}%)</p>
                    <p style='font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{color}; font-weight:bold;'>{sig}</span></p>
                    <p style='font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {tp_text} | 🛑 <b>Stop-Loss Floor:</b> {sl_text}</p>
                    <div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {txt}</div>
                </div>
                """, unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(df["Close"].tail(30)))
        except Exception as e:
            st.error(f"⚠️ Vector glitch on {ticker}: {e}")

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
            api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
            if api_key_target == "WIPE":
                ai_reply = f"Live feed status: {ctx_data} Setup your Groq Key to unleash unscripted deep learning conversations!"
                if "bitcoin" in q or "btc" in q: ai_reply = f"The live price of Bitcoin is currently **${p_map.get('BTC-CAD',0):,.2f} CAD**."
                if "ethereum" in q or "eth" in q: ai_reply = f"The live price of Ethereum is currently **${p_map.get('ETH-CAD',0):,.2f} CAD**."
                if "stop loss" in q: ai_reply = "A Stop-Loss acts as an automated protective floor price order to secure investment capital."
            else:
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key_target)
                    completion = client.chat.completions.create(model="llama-3.3-70b-specdec", messages=[{"role": "system", "content": f"You are an expert financial analyst. Answer user questions naturally. Live data: {ctx_data}. Max 2 short sentences."}, {"role": "user", "content": user_input_text}])
                    ai_reply = completion.choices[0].message.content
                except Exception as e: ai_reply = f"Neural handshake lag: {e}"
            st.write(ai_reply)
            st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
            st.rerun()

time.sleep(30)
st.rerun()
