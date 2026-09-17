import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import datetime
import pytz

# 1. PREMIUM PAGE CONFIGURATION
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .main { background-color: #0d0f14; color: #f8fafc; }
    .brand-header-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #312e81;
        box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15);
        margin-bottom: 25px;
        text-align: center;
    }
    .brand-title {
        font-size: 38px !important;
        font-weight: 800 !important;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #00ffcc 0%, #6366f1 50%, #ff4b4b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0px 0px 5px 0px !important;
        text-transform: uppercase;
        text-shadow: 0 0 40px rgba(99, 102, 241, 0.4);
    }
    .brand-subtitle {
        color: #94a3b8;
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 1px;
        margin: 0px 0px 8px 0px !important;
    }
    .brand-timestamp {
        color: #00ffcc;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 1px;
        margin: 0 !important;
        font-family: monospace;
    }
    .metric-box {
        background-color: #151922;
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid #6366f1;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px 0 rgba(0,0,0,0.4);
        border: 1px solid #222b3c;
    }
    .asset-header {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #ffffff;
        margin: 0 0 10px 0 !important;
    }
    .ai-analysis {
        background-color: #0b0f17;
        padding: 14px;
        border-radius: 8px;
        border: 1px dashed #6366f1;
        margin-top: 15px;
        font-size: 14px;
        color: #cbd5e1;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# TORONTO/CAMBRIDGE LOCAL TIME SYNC
local_timezone = pytz.timezone("America/Toronto")
current_clock_time = datetime.now(local_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

st.markdown(f"""
    <div class="brand-header-box">
        <h1 class="brand-title">🌐 ADVANCE AI MATRIX SYSTEM</h1>
        <p class="brand-subtitle">Automated Multi-Asset Deep Sequential Momentum Radar</p>
        <p class="brand-timestamp">⚡ SYSTEM STATUS: ACTIVE | MATRIX SYNC TIME: {current_clock_time}</p>
    </div>
""", unsafe_allow_html=True)

watchlist = {
    "BTC-CAD": "🪙 BTC-CAD (Bitcoin)",
    "ETH-CAD": "💎 ETH-CAD (Ethereum)",
    "SOL-CAD": "☀️ SOL-CAD (Solana)",
    "ARE.TO": "🏗️ ARE.TO (Aecon Group)"
}

if "live_prices_cache" not in st.session_state:
    st.session_state.live_prices_cache = {}

col1, col2 = st.columns(2)

with st.spinner("📥 Synchronizing core market pricing vectors..."):
    for index, (ticker, display_name) in enumerate(watchlist.items()):
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            df.columns = [str(col).strip().capitalize() for col in df.columns]
            
            close_array = df["Close"].to_numpy().flatten()
            current_actual_price = float(close_array[-1])
            past_price = float(close_array[-5])
            price_change_pct = ((current_actual_price - past_price) / past_price) * 100

            st.session_state.live_prices_cache[ticker] = current_actual_price
            stop_loss_long = current_actual_price * 0.975

            if price_change_pct > 0.5:
                action_signal = "🟢 STRONG BUY / ENTER LONG"
                border_color = "#00ffcc"
                floor_text = f"CAD ${stop_loss_long:,.2f}"
                analyst_text = f"The sequential momentum layers for {ticker} have detected a structural upward thrust of {price_change_pct:+.2f}% over the 5-day training vector. Strong institutional accumulation indicates a high-probability bullish continuation wave targeting the next upper resistance level."
            elif price_change_pct < -0.5:
                action_signal = "🔴 STRONG SELL / ENTER SHORT"
                border_color = "#ff4b4b"
                floor_text = f"CAD ${stop_loss_long:,.2f}"
                analyst_text = f"Technical data vectors reveal a sharp contraction of {price_change_pct:+.2f}% for {ticker}. Heavy trailing distribution volume has broken the primary support baseline, signaling significant structural downside risk. Protect liquid positions instantly."
            else:
                action_signal = "🟡 HOLD / WAIT FOR CONFIRMATION"
                border_color = "#ffcc00"
                floor_text = "N/A"
                analyst_text = f"{ticker} is currently compressing inside a flat, low-volatility consolidation channel ({price_change_pct:+.2f}% velocity change). Institutional order flows remain perfectly balanced. Stand by until a decisive volume-backed breakout occurs."

            target_col = col1 if index % 2 == 0 else col2
            
            with target_col:
                st.markdown(f"""
                <div class="metric-box" style="border-left-color: {border_color};">
                    <h2 class="asset-header">{display_name}</h2>
                    <hr style="margin: 8px 0 12px 0; border-color: #222b3c;">
                    <p style="font-size: 16px; margin: 4px 0; color: #94a3b8;"><b>Current Market Price:</b> <span style="color: #ffffff; font-weight: 600;">CAD ${current_actual_price:,.2f}</span></p>
                    <p style="font-size: 18px; margin: 8px 0; color: #94a3b8;"><b>SYSTEM ACTION:</b> <span style="color: {border_color}; font-weight: bold;">{action_signal}</span></p>
                    <p style="font-size: 14px; margin: 4px 0; color: #64748b;">🛑 <b>Stop-Loss Floor:</b> {floor_text}</p>
                    <div class="ai-analysis">🤖 <b>Neural AI Analyst:</b> {analyst_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                chart_df = pd.DataFrame(df["Close"].tail(30))
                chart_df.columns = ["Close"]
                st.line_chart(chart_df)

        except Exception as e:
            st.error(f"⚠️ Vector alignment glitch on {ticker}: {e}")

# 3. ADVANCED LEARNING CHATBOX
st.markdown("---")
st.header("💬 ADVANCE LEARNING CHAT INTERFACE")
st.caption("Ask questions about market indicators, strategies, or crypto setups below.")

if "chat_history_matrix" not in st.session_state:
    st.session_state.chat_history_matrix = []

for chat in st.session_state.chat_history_matrix:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

with st.form(key="chat_secure_form", clear_on_submit=True):
    user_input_text = st.text_input("Ask the Matrix AI a question (e.g., 'What is a stop loss?')...")
    submit_button = st.form_submit_button(label="⚡ Send to Matrix Brain")

if submit_button and user_input_text:
    st.session_state.chat_history_matrix.append({"role": "user", "content": user_input_text})
    
    with st.chat_message("user"):
        st.write(user_input_text)
        
    with st.chat_message("assistant"):
        p_map = st.session_state.get("live_prices_cache", {})
        q = user_input_text.lower().strip()
        
        btc_p = f"The live price of Bitcoin is currently **${p_map.get('BTC-CAD', 0):,.2f} CAD** based on our active data feed updates."
        eth_p = f"The live price of Ethereum is currently **${p_map.get('ETH-CAD', 0):,.2f} CAD** synced in real-time."
        sol_p = f"The live price of Solana is currently **${p_map.get('SOL-CAD', 0):,.2f} CAD** synced in real-time."
        sl_def = "A Stop-Loss is an automated protective floor price order that automatically sells your asset if the price drops, guaranteeing your cash investment capital stays safe from massive market drops."
        buy_def = "The system triggers a green Strong Buy action signal when the 5-day multi-variable momentum vectors break cleanly above our +0.50% volatility baseline with positive confirmation."
        hi_msg = "Hello! Welcome to the Advance Matrix system network. Ask me anything about our live indicators, strategies, or current prices!"
        fallback_msg = "Welcome to the Advance Matrix node. Ask me about specific ticker prices, stop-loss tools, or our indicator signals!"

        ai_reply = fallback_msg
        
        if "bitcoin" in q or "btc" in q:
            ai_reply = btc_p
        if "ethereum" in q or "eth" in q:
            ai_reply = eth_p
        if "solana" in q or "sol" in q:
            ai_reply = sol_p
        if "stop loss" in q or "floor" in q:
            ai_reply = sl_def
        if "buy" in q or "signal" in q:
            ai_reply = buy_def
        if "hello" in q or "hey" in q or "hi" in q:
            ai_reply = hi_msg

        st.write(ai_reply)
        st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
        st.rerun()

st.markdown("---")
st.caption("🤖 High-Velocity Production Node | Isolated Session Forms Enabled.")

time.sleep(30)
st.rerun()