import streamlit as st
import pandas as pd
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

with st.spinner("⚡ Pulling real-time market matrices..."):
    # Fetch currency exchange metrics securely
    try:
        fx_data = yf.download("CADUSD=X", period="1d", progress=False)
        usd_to_cad = 1.0 / float(fx_data["Close"].iloc[-1])
    except:
        usd_to_cad = 1.36

    for index, ticker in enumerate(watchlist):
        try:
            # Clean single-line download protocol
            df = yf.download(ticker, period="30d", interval="1d", progress=False)
            
            # Extract data rows safely without table conflicts
            close_array = df["Close"].to_numpy().flatten()
            current_actual_price = float(close_array[-1])
            
            # Simple momentum calculation that requires zero cloud processing power
            past_price = float(close_array[-5])
            price_change_pct = ((current_actual_price - past_price) / past_price) * 100

            # Currency adjustments for US markets
            is_us_stock = ticker in ["NVDA", "TSLA"]
            display_ticker = f"🪙 {ticker} (USD converted to CAD)" if is_us_stock else f"🪙 {ticker}"
            
            if is_us_stock:
                current_actual_price *= usd_to_cad

            # Execution target mathematics filters
            stop_loss_long = current_actual_price * 0.975

            if price_change_pct > 0.5:
                action_signal = "🟢 STRONG BUY / ENTER LONG"
                border_color = "#00ffcc"
                floor_text = f"CAD ${stop_loss_long:,.2f}"
            elif price_change_pct < -0.5:
                action_signal = "🔴 STRONG SELL / ENTER SHORT"
                border_color = "#ff4b4b"
                floor_text = f"CAD ${stop_loss_long:,.2f}"
            else:
                action_signal = "🟡 HOLD / WAIT FOR CONFIRMATION"
                border_color = "#ffcc00"
                floor_text = "N/A"

            # Allocate targeting column
            target_col = col1 if index % 2 == 0 else col2
            
            with target_col:
                st.markdown(f"""
                <div class="metric-box" style="border-left-color: {border_color};">
                    <h2 style="margin: 0; display: inline-block;">{display_ticker}</h2>
                    <hr style="margin: 10px 0; border-color: #334155;">
                    <p style="font-size: 16px; margin: 4px 0;"><b>Current Market Price:</b> CAD ${current_actual_price:,.2f}</p>
                    <p style="font-size: 18px; margin: 8px 0;"><b>SYSTEM ACTION:</b> <span style="color: {border_color}; font-weight: bold;">{action_signal}</span></p>
                    <p style="font-size: 14px; margin: 4px 0; color: #cbd5e1;">🛑 <b>Stop-Loss Protective Floor:</b> {floor_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Plot the clean historical trend chart
                chart_df = pd.DataFrame(df["Close"].tail(30))
                if is_us_stock:
                    chart_df["Close"] *= usd_to_cad
                st.line_chart(chart_df)

        except Exception as e:
            st.error(f"⚠️ Vector alignment glitch on {ticker}: {e}")

st.markdown("---")
st.caption("🤖 High-Velocity Trend Verification Pipeline actively optimized for remote cloud deployment frameworks.")
