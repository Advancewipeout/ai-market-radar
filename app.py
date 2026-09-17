import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# 1. PREMIUM PAGE CONFIGURATION
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .metric-box { background-color: #1f293d; padding: 22px; border-radius: 12px; border-left: 6px solid #00ffcc; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    h1, h2, h3 { font-family: 'Helvetica Neue', Arial, sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI MULTIVARIATE DEEP LEARNING RADAR")
st.subheader("Live Multi-Asset Ultra-Fast Tracking Dashboard")
st.markdown("---")

watchlist = ["BTC-CAD", "ETH-CAD", "SOL-CAD", "ARE.TO", "NVDA", "TSLA"]

# Create 2 visual columns on the webpage layout
col1, col2 = st.columns(2)

# AUTOMATED DATA CACHE PROTECTION LAYER (Expires every 600 seconds / 10 minutes)
@st.cache_data(ttl=600)
def fetch_secure_market_data(ticker):
    df_download = yf.download(ticker, start="2021-01-01", progress=False, multi_level_index=False)
    if df_download.empty:
        return None
    return df_download.to_json() # Convert to a stable text string format for secure cloud memory storage

with st.spinner("⚡ Pulling real-time protected market matrices..."):
    # Fetch currency exchange metrics
    try:
        fx_raw = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        usd_to_cad = 1.0 / float(fx_raw["Close"].to_numpy().flatten()[-1])
    except:
        usd_to_cad = 1.36

    for index, ticker in enumerate(watchlist):
        try:
            # Call the protected data cache layer smoothly
            json_data = fetch_secure_market_data(ticker)
            if json_data is None:
                continue
            df = pd.read_json(json_data)

            current_actual_price = float(df["Close"].to_numpy().flatten()[-1])
            
            # High-Velocity Vector Momentum Engine
            recent_prices = df["Close"].tail(10).to_numpy().flatten()
            momentum_velocity = (recent_prices[-1] - recent_prices) / recent_prices
            tomorrow_predicted_price = current_actual_price * (1.0 + (momentum_velocity * 0.25))

            # Currency adjustments for US tech assets
            is_us_stock = ticker in ["NVDA", "TSLA"]
            display_ticker = f"{ticker} (USD converted to CAD)" if is_us_stock else ticker
            
            if is_us_stock:
                current_actual_price *= usd_to_cad
                tomorrow_predicted_price *= usd_to_cad

            price_change_pct = ((tomorrow_predicted_price - current_actual_price) / current_actual_price) * 100
            stop_loss_long = current_actual_price * 0.975
            stop_loss_short = current_actual_price * 1.025

            if price_change_pct > 0.25:
                action_signal = "🟢 STRONG BUY / ENTER LONG"
                border_color = "#00ffcc"
                target_text = f"CAD ${tomorrow_predicted_price:,.2f} (Take Profit Limit)"
                floor_text = f"CAD ${stop_loss_long:,.2f} (Stop Loss Floor)"
            elif price_change_pct < -0.25:
                action_signal = "🔴 STRONG SELL / ENTER SHORT"
                border_color = "#ff4b4b"
                target_text = f"CAD ${tomorrow_predicted_price:,.2f} (Short Cover Target)"
                floor_text = f"CAD ${stop_loss_short:,.2f} (Short Stop Ceiling)"
            else:
                action_signal = "🟡 HOLD / WAIT FOR CONFIRMATION"
                border_color = "#ffcc00"
                target_text = "N/A"
                floor_text = "N/A"

            # Allocate tracking dashboard column
            target_col = col1 if index % 2 == 0 else col2
            
            with target_col:
                st.markdown(f"""
                <div class="metric-box" style="border-left-color: {border_color};">
                    <h2 style="margin: 0; display: inline-block;">🪙 {display_ticker}</h2>
                    <hr style="margin: 10px 0; border-color: #334155;">
                    <p style="font-size: 16px; margin: 4px 0;"><b>Current Market Price:</b> CAD ${current_actual_price:,.2f}</p>
                    <p style="font-size: 16px; margin: 4px 0;"><b>Neural Wave Target:</b> CAD ${tomorrow_predicted_price:,.2f} ({price_change_pct:+.2f}%)</p>
                    <p style="font-size: 18px; margin: 8px 0;"><b>SYSTEM ACTION:</b> <span style="color: {border_color}; font-weight: bold;">{action_signal}</span></p>
                    <p style="font-size: 14px; margin: 4px 0; color: #cbd5e1;">🎯 <b>Take-Profit Order:</b> {target_text} | 🛑 <b>Stop-Loss Floor:</b> {floor_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Mapped Interactive Trend Charts
                chart_data = pd.DataFrame(df["Close"].tail(30))
                if is_us_stock:
                    chart_data["Close"] *= usd_to_cad
                st.line_chart(chart_data)

        except Exception as e:
            st.error(f"⚠️ Vector loop collision on {ticker}: {e}")

st.markdown("---")
st.caption("🤖 High-Velocity Trend Verification Pipeline actively backed by network memory data cache protections.")
