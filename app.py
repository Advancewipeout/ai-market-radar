import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json, urllib.request
from datetime import datetime
import pytz

# 1. PREMIUM PAGE SETUP
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color: #0d0f14; color: #f8fafc; }.metric-box { background-color: #151922; padding: 24px; border-radius: 14px; border-left: 6px solid #6366f1; margin-bottom: 20px; border: 1px solid #222b3c; }.ai-analysis { background-color: #0b0f17; padding: 14px; border-radius: 8px; border: 1px dashed #6366f1; margin-top: 15px; font-size: 14px; color: #cbd5e1; }</style>", unsafe_allow_html=True)

clock = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M:%S %p")
st.markdown(f"<div style='background: linear-gradient(135deg, #1e1b4b, #0f172a); padding:30px; border-radius:16px; border:1px solid #312e81; text-align:center;'><h1 style='background:linear-gradient(90deg, #00ffcc, #6366f1, #ff4b4b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; font-size:38px; font-weight:800;'>🌐 ADVANCE AI MATRIX SYSTEM</h1><p style='color:#94a3b8; margin:5px 0 0 0;'>⚡ SYSTEM STATUS: ACTIVE | SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

watchlist = {"BTC-CAD": "🪙 Bitcoin", "ETH-CAD": "💎 Ethereum", "SOL-CAD": "☀️ Solana", "ARE.TO": "🏗️ Aecon Group", "NVDA": "🎮 NVIDIA Corp", "TSLA": "⚡ Tesla Inc"}
if "live_prices" not in st.session_state: st.session_state.live_prices = {}
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
            df.columns = [str(c).strip().capitalize() for c in df.columns]
            close_arr = df["Close"].to_numpy().flatten()
            price = float(close_arr[-1])
            if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
            st.session_state.live_prices[ticker] = price
            
            pct = ((price - float(close_arr[-5])) / float(close_arr[-5])) * 100
            signal, color = ("🟡 HOLD", "#ffcc00") if abs(pct) <= 0.5 else (("🟢 BUY", "#00ffcc") if pct > 0.5 else ("🔴 SELL", "#ff4b4b"))
            txt = f"Consolidation channels are active for {ticker} ({pct:+.2f}% change). Momentum signals suggest standing by." if signal == "🟡 HOLD" else f"Momentum breakout detected for {ticker} ({pct:+.2f}% change). System filters recommend executing {signal} entries."

            with col1 if index % 2 == 0 else col2:
                st.markdown(f"<div class='metric-box' style='border-left-color:{color};'><h3>{display_name}</h3><hr style='border-color:#222b3c;'><p><b>Market Price:</b> CAD ${price:,.2f}</p><p><b>SYSTEM ACTION:</b> <span style='color:{color}; font-weight:bold;'>{signal}</span></p><div class='ai-analysis'>🤖 <b>Neural Analyst:</b> {txt}</div></div>", unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(df["Close"].tail(30)))
        except Exception as e:
            st.error(f"⚠️ Vector glitch on {ticker}: {e}")

# 2. ISOLATED CHAT INTERFACE LOOP
st.markdown("---")
st.header("💬 ADVANCE LEARNING CHAT INTERFACE")
for chat in st.session_state.chat_history_matrix:
    with st.chat_message(chat["role"]): st.write(chat["content"])

with st.form(key="chat_secure_form", clear_on_submit=True):
    user_txt = st.text_input("Ask the Matrix AI a question...")
    submit = st.form_submit_button(label="⚡ Send to Matrix Brain")

if submit and user_txt:
    st.session_state.chat_history_matrix.append({"role": "user", "content": user_txt})
    with st.chat_message("user"): st.write(user_txt)
    
    with st.chat_message("assistant"):
        p = st.session_state.live_prices
        q = user_txt.lower().strip()
        ctx = f"BTC: ${p.get('BTC-CAD',0):,.2f}, ETH: ${p.get('ETH-CAD',0):,.2f}, NVDA: ${p.get('NVDA',0):,.2f}, TSLA: ${p.get('TSLA',0):,.2f} CAD."
        key = st.secrets.get("GROQ_API_KEY", "WIPE")
        
        if key == "WIPE":
            reply = f"Live feed status: {ctx} Ask about specific assets or update your Groq API secrets token!"
            if "bitcoin" in q or "btc" in q: reply = f"Bitcoin's price is currently **${p.get('BTC-CAD',0):,.2f} CAD**."
            if "ethereum" in q or "eth" in q: reply = f"Ethereum's price is currently **${p.get('ETH-CAD',0):,.2f} CAD**."
            if "stop loss" in q: reply = "A stop-loss acts as a protective mathematical floor value to secure trading capital."
        else:
            try:
                req = urllib.request.Request("https://groq.com", data=json.dumps({"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": f"You are a financial analyst. Use data: {ctx}. Max 2 short sentences."}, {"role": "user", "content": user_txt}]}).encode("utf-8"), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req) as resp:
                    reply = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"API connection link lag: {e}"
                
        st.write(reply)
        st.session_state.chat_history_matrix.append({"role": "assistant", "content": reply})
        st.rerun()

time.sleep(30)
st.rerun()
