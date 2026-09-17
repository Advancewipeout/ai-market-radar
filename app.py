import streamlit as st, pandas as pd, numpy as np, yfinance as yf, time, json
from datetime import datetime
import pytz

# 1. VISUAL INTERFACE STYLE & PREMIUM BRANDING
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.main { background-color:#0d0f14; color:#f8fafc; }.metric-box { background-color:#151922; padding:24px; border-radius:14px; margin-bottom:20px; border:1px solid #222b3c; }.ai-analysis { background-color:#0b0f17; padding:14px; border-radius:8px; border:1px dashed #6366f1; margin-top:15px; font-size:14px; color:#cbd5e1; line-height:1.5; }.news-box { background-color:#0e111a; padding:14px; border-radius:8px; border:1px solid #1e293b; margin-top:10px; font-size:13px; color:#94a3b8; line-height:1.5; }</style>", unsafe_allow_html=True)

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
        except: pass

api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")

col1, col2 = st.columns(2)
for index, ticker in enumerate(watchlist.keys()):
    if ticker in asset_data_store:
        data = asset_data_store[ticker]
        
        if api_key_target == "WIPE":
            strat_txt = f"The model is maintaining this position for 2 to 4 days, tracking a sell execution breakout toward CAD ${data['target']:,.2f}."
            intel_txt = f"Live updates show steady transaction volume support near the current macro floor thresholds."
        else:
            try:
                from groq import Groq
                client = Groq(api_key=api_key_target)
                p1 = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "user", "content": f"You are a trade tracking system. Write a single brief sentence explaining exactly how long the model intends to hold the asset {ticker} based on its 5-day move of {data['pct']:+.2f}% and at what target price (CAD ${data['target']:,.2f}) it will execute a sell order. Speak directly to users as a guide."}])
                strat_txt = p1.choices.message.content
            except:
                strat_txt = f"The model is maintaining this position for 2 to 4 days, tracking a sell execution breakout toward CAD ${data['target']:,.2f}."
            
            try:
                p2 = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "user", "content": f"Write a single brief sentence summarizing the current real-time market sentiment or recent social media updates for the asset {ticker} right now. Do not repeat introductions."}])
                intel_txt = p2.choices.message.content
            except:
                intel_txt = f"Live updates show steady transaction volume support near the current macro floor thresholds."

        with col1 if index % 2 == 0 else col2:
            st.markdown(f"""
            <div class='metric-box' style='border-left: 6px solid {data["color"]};'>
                <h2 class='asset-header'>{data["display_name"]}</h2>
                <hr style='border-color:#222b3c; margin: 8px 0 12px 0;'>
                <p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data["price"]:,.2f}</p>
                <p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data["target"]:,.2f} ({data["pct"]:+.2f}%)</p>
                <p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data["color"]}; font-weight:bold;'>{data["sig"]}</span></p>
                <p style='margin:4px 0; font-size:14px; color:#cbd5e1;'>🎯 <b>Take-Profit Target:</b> {data["tp"]} | 🛑 <b>Stop-Loss Floor:</b> {data["sl"]}</p>
                <div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {strat_txt}</div>
                <div class='news-box'>📰 <b>Live Market Intelligence:</b> {intel_txt}</div>
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
            else:
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key_target)
                    completion = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "system", "content": f"You are an expert financial analyst. Answer user questions naturally. Live data: {ctx_data}. Max 2 short sentences."}, {"role": "user", "content": user_input_text}])
                    ai_reply = completion.choices.message.content
                except Exception as e: ai_reply = f"Neural handshake lag: {e}"
            st.write(ai_reply)
            st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
            st.rerun()

st.markdown("---")
st.caption("🤖 High-Velocity Production Node | Isolated Session Forms Enabled.")
time.sleep(30)
st.rerun()
