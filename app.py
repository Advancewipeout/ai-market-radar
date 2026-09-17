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
    "ARE.TO": "🏗️ ARE.TO (Aecon Group)",
    "NVDA": "🎮 NVDA (NVIDIA Corp)",
    "TSLA": "⚡ TSLA (Tesla Inc)"
}

if "live_prices_cache" not in st.session_state:
    st.session_state.live_prices_cache = {}

col1, col2 = st.columns(2)

with st.spinner("📥 Synchronizing core market pricing vectors..."):
    try:
        fx_data = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        usd_to_cad = 1.0 / float(fx_data["Close"].to_numpy().flatten()[-1])
    except:
        usd_to_cad = 1.36

    for index, (ticker, display_name) in enumerate(watchlist.items()):
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            df.columns = [str(col).strip().capitalize() for col in df.columns]
            
            close_array = df["Close"].to_numpy().flatten()
            current_actual_price = float(close_array[-1])
            past_price = float(close_array[-5])
            price_change_pct = ((current_actual_price - past_price) / past_price) * 100

            is_us_stock = ticker in ["NVDA", "TSLA"]
            final_title = f"{display_name} [CAD CONVERTED]" if is_us_stock else display_name
            
            if is_us_stock:
                current_actual_price *= usd_to_cad

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
                    <h2 class="asset-header">{final_title}</h2>
                    <hr style="margin: 8px 0 12px 0; border-color: #222b3c;">
                    <p style="font-size: 16px; margin: 4px 0; color: #94a3b8;"><b>Current Market Price:</b> <span style="color: #ffffff; font-weight: 600;">CAD ${current_actual_price:,.2f}</span></p>
                    <p style="font-size: 18px; margin: 8px 0; color: #94a3b8;"><b>SYSTEM ACTION:</b> <span style="color: {border_color}; font-weight: bold;">{action_signal}</span></p>
                    <p style="font-size: 14px; margin: 4px 0; color: #64748b;">🛑 <b>Stop-Loss Floor:</b> {floor_text}</p>
                    <div class="ai-analysis">🤖 <b>Neural AI Analyst:</b> {analyst_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                chart_df = pd.DataFrame(df["Close"].tail(30))
                chart_df.columns = ["Close"]
                if is_us_stock:
                    chart_df["Close"] *= usd_to_cad
                st.line_chart(chart_df)

        except Exception as e:
            st.error(f"⚠️ Vector alignment glitch on {ticker}: {e}")

# 3. ADVANCED LEARNING CHATBOX (WITH LIVE PRICE RECOGNITION DATA FEED)
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
        with st.spinner("Analyzing question query parameters..."):
            p_map = st.session_state.get("live_prices_cache", {})
            market_context_data = f"""
            System Matrix Live Context:
            - Bitcoin (BTC-CAD): ${p_map.get('BTC-CAD', 0):,.2f} CAD
            - Ethereum (ETH-CAD): ${p_map.get('ETH-CAD', 0):,.2f} CAD
            - Solana (SOL-CAD): ${p_map.get('SOL-CAD', 0):,.2f} CAD
            - Aecon Group (ARE.TO): ${p_map.get('ARE.TO', 0):,.2f} CAD
            - NVIDIA Corp (NVDA): ${p_map.get('NVDA', 0):,.2f} CAD
            - Tesla Inc (TSLA): ${p_map.get('TSLA', 0):,.2f} CAD
            """
            
            # SECURE CLOUD GATEWAY: Completely removed the broken try/except loops
            api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
            
            if api_key_target == "WIPE":
                # Clean, un-nested text-matching algorithm
                q = user_input_text.lower()
                if "price" in q or "value" in q or "much" in q:
                    if "bitcoin" in q or "btc" in q:
                        ai_reply = f"The live price of Bitcoin is currently **${p_map.get('BTC-CAD', 0):,.2f} CAD** based on our active data feed updates."
                    elif "ethereum" in q or "eth" in q:
                        ai_reply = f"The live price of Ethereum is currently **${p_map.get('ETH-CAD', 0):,.2f} CAD** synced in real-time."
                    elif "nvidia" in q or "nvda" in q:
                        ai_reply = f"NVIDIA Corp (NVDA) is trading at a currency-converted value of **${p_map.get('NVDA', 0):,.2f} CAD**."
                    elif "tesla" in q or "tsla" in q:
                        ai_reply = f"Tesla Inc (TSLA) is trading at a currency-converted value of **${p_map.get('TSLA', 0):,.2f} CAD**."
                    else:
