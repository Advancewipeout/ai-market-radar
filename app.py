import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

# 1. PAGE CORE STYLING LAYOUT
st.set_page_config(page_title="AI Market Matrix", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .metric-box { background-color: #1f293d; padding: 22px; border-radius: 12px; border-left: 6px solid #00ffcc; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    h1, h2, h3 { font-family: 'Helvetica Neue', Arial, sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI MULTIVARIATE DEEP LEARNING RADAR")
st.subheader("Live Multi-Asset Hardware-Accelerated Tracking Dashboard")
st.markdown("---")

# 2. DEVICE ARCHITECTURE DETECTION CHECK
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
st.sidebar.markdown(f"**⚡ GPU Target:** `{str(device).upper()}`")
st.sidebar.markdown(f"**🎮 Core Engine:**  \n`{torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU Engine'}`")

# EXPANDED WATCHLIST: Crypto + TSX Industry Leaders + Nasdaq High-Beta Tech Heavyweights
watchlist = ["BTC-CAD", "ETH-CAD", "SOL-CAD", "ARE.TO", "NVDA", "TSLA"]

# LSTM Model Architecture blueprint
class WebsiteCryptoLSTM(nn.Module):
    def __init__(self, input_size=2, hidden_size=64, num_layers=2):
        super(WebsiteCryptoLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

# Create 2 visual columns on the webpage layout
col1, col2 = st.columns(2)

# Trigger loading state animation while the 4060 Ti computes calculus
with st.spinner("🤖 RTX 4060 Ti processing multi-variable deep learning optimization matrices... Please standby."):
    # Dynamically fetch USD to CAD exchange rate to keep all outputs grounded in Canadian Dollars
    try:
        fx_data = yf.download("CADUSD=X", period="1d", progress=False)
        fx_data.columns = fx_data.columns.get_level_values(0)
        usd_to_cad = 1.0 / float(fx_data["Close"].to_numpy().flatten()[-1])
    except:
        usd_to_cad = 1.36 # Hardcoded robust fallback if FX server lags

    for index, ticker in enumerate(watchlist):
        try:
            # Siphon asset dataset arrays
            df = yf.download(ticker, start="2019-01-01", progress=False)
            if df.empty or len(df) < 100:
                continue
            df.columns = df.columns.get_level_values(0)

            # Flatten inputs to explicitly remove dimensional multi-index shapes
            close_prices = df["Close"].to_numpy().flatten()
            volumes = df["Volume"].to_numpy().flatten()

            features_data = np.column_stack((close_prices, volumes))
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(features_data)

            # Sequence memory structures
            LOOKBACK_WINDOW = 60
            X, y = [], []
            for i in range(LOOKBACK_WINDOW, len(scaled_data)):
                X.append(scaled_data[i-LOOKBACK_WINDOW:i, :])
                y.append(scaled_data[i, 0])

            X, y = np.array(X), np.array(y)
            X_tensor = torch.tensor(X, dtype=torch.float32).to(device)
            y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1).to(device)

            # Model instance and optimization layers
            model = WebsiteCryptoLSTM().to(device)
            criterion = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

            # 200 Core Epoch Training Loops per asset
            epochs = 200
            for epoch in range(epochs):
                model.train()
                optimizer.zero_grad()
                predictions = model(X_tensor)
                loss = criterion(predictions, y_tensor)
                loss.backward()
                optimizer.step()

            # Predictive data matrix inversion calculations
            model.eval()
            with torch.no_grad():
                last_60_days = scaled_data[-LOOKBACK_WINDOW:]
                last_60_days_tensor = torch.tensor(last_60_days, dtype=torch.float32).unsqueeze(0).to(device)
                future_scaled_pred = model(last_60_days_tensor).cpu().numpy().flatten()[0]
                
                last_volume_scaled = float(scaled_data[-1, 1])
                aligned_dummy_matrix = np.array([[float(future_scaled_pred), last_volume_scaled]])
                inverted_matrix = scaler.inverse_transform(aligned_dummy_matrix)
                
                tomorrow_predicted_price = float(inverted_matrix.flatten()[0])
                current_actual_price = float(close_prices[-1])

            # Currency Normalization Rule: Convert US Stock Quotes automatically into CAD format strings
            is_us_stock = ticker in ["NVDA", "TSLA"]
            display_ticker = f"🪙 {ticker} (USD converted to CAD)" if is_us_stock else f"🪙 {ticker}"
            
            if is_us_stock:
                current_actual_price *= usd_to_cad
                tomorrow_predicted_price *= usd_to_cad

            # Execution target mathematics filters
            price_change_pct = ((tomorrow_predicted_price - current_actual_price) / current_actual_price) * 100
            stop_loss_long = current_actual_price * 0.975
            stop_loss_short = current_actual_price * 1.025

            if price_change_pct > 0.75:
                action_signal = "🟢 STRONG BUY / ENTER LONG"
                border_color = "#00ffcc"
                target_text = f"CAD \${tomorrow_predicted_price:,.2f} (Take Profit Limit)"
                floor_text = f"CAD \${stop_loss_long:,.2f} (Stop Loss Floor)"
            elif price_change_pct < -0.75:
                action_signal = "🔴 STRONG SELL / ENTER SHORT"
                border_color = "#ff4b4b"
                target_text = f"CAD \${tomorrow_predicted_price:,.2f} (Short Cover Target)"
                floor_text = f"CAD \${stop_loss_short:,.2f} (Short Stop Ceiling)"
            else:
                action_signal = "🟡 HOLD / WAIT FOR CONFIRMATION"
                border_color = "#ffcc00"
                target_text = "N/A"
                floor_text = "N/A"

            # Dynamically alternate columns to keep web interface balanced
            target_col = col1 if index % 2 == 0 else col2
            
            with target_col:
                st.markdown(f"""
                <div class="metric-box" style="border-left-color: {border_color};">
                    <h2 style="margin: 0; display: inline-block;">{display_ticker}</h2>
                    <hr style="margin: 10px 0; border-color: #334155;">
                    <p style="font-size: 16px; margin: 4px 0;"><b>Current Market Price:</b> CAD \${current_actual_price:,.2f}</p>
                    <p style="font-size: 16px; margin: 4px 0;"><b>Neural Wave Target:</b> CAD \${tomorrow_predicted_price:,.2f} ({price_change_pct:+.2f}%)</p>
                    <p style="font-size: 18px; margin: 8px 0;"><b>SYSTEM ACTION:</b> <span style="color: {border_color}; font-weight: bold;">{action_signal}</span></p>
                    <p style="font-size: 14px; margin: 4px 0; color: #cbd5e1;">🎯 <b>Take-Profit Order:</b> {target_text} | 🛑 <b>Stop-Loss Floor:</b> {floor_text}</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Vector loop collision on {ticker}: {e}")

st.markdown("---")
st.caption("🤖 Multi-Variable Recurrent LSTM Framework actively querying Yahoo Finance API datasets and utilizing local NVIDIA CUDA cores.")
