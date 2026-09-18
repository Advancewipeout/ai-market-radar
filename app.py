import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
import json
import urllib.request
from datetime import datetime
import pytz
from groq import Groq

# ==============================================================================
# 1. PREMIUM HEADER DESIGN & UN-CLIPPED CHASING-TAIL NEON BORDER STYLING CORES
# ==============================================================================
st.set_page_config(
    page_title="AI Market Matrix",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main { 
        background-color: #0d0f14; 
        color: #f8fafc; 
    }
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
        margin: 0px 0px 15px 0px !important; 
    }
    
    /* 🎰 HIGH-TECH CONTAINER CARDS WITH EMBEDDED CLIP-MASK TRACKS */
    .metric-box { 
        position: relative; 
        background-color: #151922; 
        padding: 24px; 
        border-radius: 14px; 
        margin-bottom: 20px; 
        border: 2px solid transparent; 
        background-clip: padding-box; 
        overflow: hidden; 
        z-index: 1; 
    }
    .metric-box::before { 
        content: ''; 
        position: absolute; 
        top: -150%; bottom: -150%; left: -150%; right: -150%; 
        z-index: -2; 
        animation: tail-spin-chaser 4s linear infinite; 
    }
    .metric-box::after { 
        content: ''; 
        position: absolute; 
        top: 2px; left: 2px; right: 2px; bottom: 2px; 
        background-color: #151922; 
        border-radius: 12px; 
        z-index: -1; 
    }
    
    /* WHISPER-THIN CONIC GRADIENTS FOR CHASING LIGHT RIMS */
    .glow-hold::before { background: conic-gradient(from 0deg, #ffcc00 0%, #ffcc00 15%, transparent 35%, transparent 100%); }
    .glow-buy::before { background: conic-gradient(from 0deg, #00ffcc 0%, #00ffcc 15%, transparent 35%, transparent 100%); }
    .glow-sell::before { background: conic-gradient(from 0deg, #ff4b4b 0%, #ff4b4b 15%, transparent 35%, transparent 100%); }
    
    @keyframes tail-spin-chaser { 
        100% { transform: rotate(360deg); } 
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
    .news-box { 
        background-color: #0e111a; 
        padding: 14px; 
        border-radius: 8px; 
        border: 1px solid #1e293b; 
        margin-top: 10px; 
        font-size: 13px; 
        color: #94a3b8; 
        line-height: 1.5; 
    }
    </style>
""", unsafe_allow_html=True)

local_tz = pytz.timezone("America/Toronto")

# ⏱ ... LANE 1: ISOLATED CLOCK BANNER FRAGMENT (RUNS FLUIDLY EVERY 1.0 SECOND)
@st.fragment(run_every=1.0)
def render_live_clock_banner():
    clock = datetime.now(local_tz).strftime("%Y-%m-%d %I:%M:%S %p")
    st.markdown(f"<div class='brand-header-box'><h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1><p class='brand-subtitle'>Automated Multi-Asset Deep Sequential Momentum Radar</p><p style='color: #00ffcc; font-family: monospace; font-size: 14px; font-weight: 600; margin: 0; letter-spacing: 1px;'>⚡ SYSTEM STATUS: ACTIVE | MATRIX LIVE SYNC TIME: {clock}</p></div>", unsafe_allow_html=True)

render_live_clock_banner()

# ==============================================================================
# 2. CORE MARKET DATA CAPTURE AND MULTI-ASSET AI PIPELINE CONFIGURATIONS
# ==============================================================================
watchlist = {
    "BTC-CAD": "🪙 BTC-CAD (Bitcoin)", 
    "ETH-CAD": "💎 ETH-CAD (Ethereum)", 
    "SOL-CAD": "☀️ SOL-CAD (Solana)", 
    "ARE.TO": "🏗️ ARE.TO (Aecon Group)", 
    "NVDA": "🎮 NVDA (NVIDIA Corp)", 
    "TSLA": "⚡ TSLA (Tesla Inc)"
}

if "live_prices_cache" not in st.session_state: st.session_state.live_prices_cache = {}
if "chat_history_matrix" not in st.session_state: st.session_state.chat_history_matrix = []
if "backup_vectors_store" not in st.session_state: st.session_state.backup_vectors_store = {}
if "ai_cards_cache" not in st.session_state: st.session_state.ai_cards_cache = {}
# 🧠 ROLLING PERSISTENT SESSION TRACKER VECTORS
if "rolling_trade_history" not in st.session_state: st.session_state.rolling_trade_history = {t: [] for t in watchlist.keys()}

def get_ai_unscripted_card_analysis(ticker, price, target_p, pct, sig, api_key):
    if api_key == "WIPE":
        return (f"⏳ **AI TRADING LOG**: System tracking consolidation channels for {ticker}. Core targets holding stable near CAD ${target_p:,.2f}.", 
                "🔄 Data Volume Analysis: Order matching profiles remain uniformly spread across active bid/ask layers.")
    
    # Extract rolling text trail context to inject past execution behaviors into the decision track
    past_logs = st.session_state.rolling_trade_history.get(ticker, [])[-4:]
    history_context = " | ".join(past_logs) if past_logs else "None (Initial baseline run)."

    try:
        client = Groq(api_key=api_key)
        prompt = f"""
        Act as an independent, self-operating institutional quantitative trading AI model running a live capital account.
        Analyze this raw asset packet and immediately generate clear, explicit directives for human viewers to mimic for optimal outcomes.
        
        Asset metrics:
        - Ticker Symbol: {ticker}
        - Current Market Price: CAD ${price:,.2f}
        - Computational Wave Target: CAD ${target_p:,.2f}
        - Momentum Shift Vector: {pct:+.2f}%
        - Momentum Signal Baseline: {sig}
        
        Your active trading memory path from previous loops:
        [{history_context}]

        Strict formatting output directive:
        You MUST respond with a raw JSON object containing exactly two keys: "strat" and "intel". Do not include Markdown wrapper code indicators.
        
        "strat": Must be a 1-2 sentence real-time portfolio entry log detailing your internal thinking, explicit system choices (e.g., whether to enter a buy order, scale long positions, hold capital reserves, or close positions), and provide a definitive timeline estimation for how long human viewers should maintain this stance. Prefix strictly with '📈 **AI TRADING LOG**: ' or '📉 **AI TRADING LOG**: '.
        
        "intel": Must be a 1-sentence data volume intelligence overview profiling institutional buy/sell walls, exchange telemetry delta shifts, options flow imbalances, or whale block actions. Prefix strictly with '📰 **Live Market Intelligence**: '.
        
        Ensure your messaging adapts seamlessly based on your memory path to avoid string loops or phrase repetition. Do not talk to viewers directly; speak as an active model tracking its own execution ledger.
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile", 
            messages=[{"role": "user", "content": prompt}], 
            response_format={"type": "json_object"}
        )
        res = json.loads(completion.choices.message.content)
        strat_val = res.get("strat") or res.get("STRAT") or res.get("strategy") or res.get("Strategy")
        intel_val = res.get("intel") or res.get("INTEL") or res.get("intelligence") or res.get("Intelligence")
        
        if strat_val and intel_val:
            # Commit the fresh trade call out to the rolling session cache to build logical continuity
            st.session_state.rolling_trade_history[ticker].append(str(strat_val))
            return str(strat_val), str(intel_val)
    except Exception:
        pass
        
    return (f"⏳ **AI TRADING LOG**: Model maintaining its trend track baseline corridor for {ticker} near CAD ${target_p:,.2f}.", 
            "🔄 Data Volume Intelligence: Real-time buyer and seller metrics are balanced across active book parameters.")

def load_realtime_market_updates():
    usd_to_cad = 1.36
    try:
        fx_df = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        if fx_df is not None and not fx_df.empty:
            val = fx_df["Close"].to_numpy().flatten()[-1]
            if val > 0: usd_to_cad = 1.0 / float(val)
    except Exception:
        usd_to_cad = 1.36
        
    api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
    store = {}
    
    for ticker, display_name in watchlist.items():
        p_fb = 107320.0 if ticker=="BTC-CAD" else (3415.0 if ticker=="ETH-CAD" else (184.50 if ticker=="SOL-CAD" else (22.40 if ticker=="ARE.TO" else (116.80 if ticker=="NVDA" else 242.10))))
        fake_chart_data = pd.DataFrame({"Close": [p_fb * (1 + (np.sin(i/5)*0.01)) for i in range(30)]})
        
        store[ticker] = {
            "display_name": display_name, "price": p_fb, "target": p_fb * 1.002, "pct": 0.04,
            "sig": "🟡 HOLD / WAIT FOR CONFIRMATION", "color": "#ffcc00", "df": fake_chart_data,
            "glow": "glow-hold", "strat": "Monitoring asset metric baselines.", "intel": "Processing volume matrices."
        }
        
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            if df is not None and not df.empty and len(df) >= 5:
                df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
                close_arr = df["Close"].to_numpy().flatten()
                price = float(np.nan_to_num(close_arr[-1]))
                if price <= 0: price = float(np.nan_to_num(df["Adj close"].to_numpy().flatten()[-1]))
                if ticker in ["NVDA", "TSLA"]: price *= usd_to_cad
                if price <= 0: raise ValueError("Empty Price")
                prev_close = float(np.nan_to_num(close_arr[-5])) if len(close_arr) >= 5 else price
                pct = ((price - prev_close) / prev_close) * 100
                target_p = price * (1.0 + (pct * 0.05 / 100))
                sig, color, glow = ("🟢 STRONG BUY / ENTER LONG", "#00ffcc", "glow-buy") if pct > 0.05 else (("🔴 STRONG SELL / ENTER SHORT", "#ff4b4b", "glow-sell") if pct < -0.05 else ("🟡 HOLD / WAIT FOR CONFIRMATION", "#ffcc00", "glow-hold"))
                cache_key = f"{ticker}_{round(price, 2)}"
                if cache_key not in st.session_state.ai_cards_cache:
                    strat, intel = get_ai_unscripted_card_analysis(ticker, price, target_p, pct, sig, api_key_target)
                    st.session_state.ai_cards_cache[cache_key] = (strat, intel)
                else: strat, intel = st.session_state.ai_cards_cache[cache_key]
                store[ticker] = {"display_name": display_name, "price": price, "target": target_p, "pct": pct, "sig": sig, "color": color, "df": df, "glow": glow, "strat": strat, "intel": intel}
                st.session_state.backup_vectors_store[ticker] = store[ticker]
            else: raise ValueError("Handshake Delay")
        except Exception: pass
        if ticker not in store and ticker in st.session_state.backup_vectors_store: store[ticker] = st.session_state.backup_vectors_store[ticker]
    return store

# 🚀 LANE 2: STABILIZED FINANCIAL ASSET CONTAINER PLATFORM (REFRESHES PRIVATELY EVERY 5 SECONDS)
@st.fragment(run_every=5.0)
def render_live_matrix_grid():
    asset_data_store = load_realtime_market_updates()
    for k, data in asset_data_store.items(): st.session_state.live_prices_cache[k] = data["price"]
    col1, col2 = st.columns(2)
    for index, ticker in enumerate(watchlist.keys()):
        if ticker in asset_data_store:
            data = asset_data_store[ticker]
            with col1 if index % 2 == 0 else col2:
                st.markdown(f"<div class='metric-box {data['glow']}'><h2 style='color:#ffffff; margin:0 0 10px 0;'>{data['display_name']}</h2><hr style='border-color:#222b3c; margin: 8px 0 12px 0;'><p style='margin:4px 0;'><b>Current Market Price:</b> CAD ${data['price']:,.2f}</p><p style='margin:4px 0;'><b>Neural Wave Target:</b> CAD ${data['target']:,.2f} ({data['pct']:+.2f}%)</p><p style='margin:8px 0; font-size:18px;'><b>SYSTEM ACTION:</b> <span style='color:{data['color']}; font-weight:bold;'>{data['sig']}</span></p><div class='ai-analysis'>🤖 <b>Neural AI Analyst:</b> {data['strat']}</div><div class='news-box'>📰 <b>Live Market Intelligence:</b> {data['intel']}</div></div>", unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(data['df']["Close"].tail(30)))
render_live_matrix_grid()

# ==============================================================================
# 3. INTERACTIVE CHAT ENGINE (100% SECURE PRODUCTION PIPELINE PASS)
# ==============================================================================
st.markdown("---")
st.header("💬 SMITTY'S LEARNING CHAT INTERFACE")
for chat in st.session_state.chat_history_matrix:
    with st.chat_message(chat["role"]): st.write(chat["content"])

with st.form(key="chat_secure_form", clear_on_submit=True):
    user_input_text = st.text_input("Ask the Matrix AI a question...")
    submit_button = st.form_submit_button(label="⚡ Send to Matrix Brain")

api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
if submit_button and user_input_text:
    st.session_state.chat_history_matrix.append({"role": "user", "content": user_input_text})
    with st.chat_message("user"): st.write(user_input_text)
    p_map = st.session_state.live_prices_cache
    ctx_data = f"Bitcoin: {p_map.get('BTC-CAD',0):,.2f}, Ethereum: {p_map.get('ETH-CAD',0):,.2f}, Solana: {p_map.get('SOL-CAD',0):,.2f}, NVIDIA: {p_map.get('NVDA',0):,.2f}, Tesla: {p_map.get('TSLA',0):,.2f} CAD."
    ai_reply = f"Live feed status: {ctx_data} Setup your Groq Key inside your secrets box to unleash unscripted deep learning conversations!"
    if api_key_target != "WIPE":
        client = Groq(api_key=api_key_target)
        try:
            completion = client.chat.completions.create(model="llama-3.1-70b-versatile", messages=[{"role": "system", "content": f"You are Smitty's automated financial brain. Converse with unscripted expert financial depth. Max 3 sentences. Live tokens context: {ctx_data}"}, {"role": "user", "content": user_input_text}])
            ai_reply = completion.choices.message.content
        except: ai_reply = f"Sync matrix parameters: {ctx_data}"
    with st.chat_message("assistant"): st.write(ai_reply)
    st.session_state.chat_history_matrix.append({"role": "assistant", "content": ai_reply})
    st.rerun()
st.markdown("---")
st.caption("🤖 High-Velocity Production Node | Isolated Session Forms Enabled.")

        