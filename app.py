import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
import json
import urllib.request
from datetime import datetime
import pytz

# ==============================================================================
# 1. VISUAL LAYER LAYOUT DESIGN & PERFECT 2PX CHASING-TAIL NEON BORDER LAYOUT
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

# ⏱️ LANE 1: ISOLATED CLOCK BANNER FRAGMENT (RUNS FLUIDLY EVERY 1.0 SECOND)
@st.fragment(run_every=1.0)
def render_live_clock_banner():
    clock = datetime.now(local_tz).strftime("%Y-%m-%d %I:%M:%S %p")
    st.markdown(f"""
        <div class='brand-header-box'>
            <h1 class='brand-title'>🌐 SMITTY'S AI MATRIX SYSTEM</h1>
            <p class='brand-subtitle'>Automated Multi-Asset Deep Sequential Momentum Radar</p>
            <p style='color: #00ffcc; font-family: monospace; font-size: 14px; font-weight: 600; margin: 0; letter-spacing: 1px;'>⚡ SYSTEM STATUS: ACTIVE | MATRIX LIVE SYNC TIME: {clock}</p>
        </div>
    """, unsafe_allow_html=True)

render_live_clock_banner()

# ==============================================================================
# 2. CORE MARKET DATA CAPTURE AND MULTI-ASSET ANALYSIS PIPELINE
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

def get_ai_unscripted_card_analysis(ticker, price, target_p, pct, sig, api_key):
    # Fallback to prevent crashing if keys are blank
    if api_key == "WIPE":
        return ("⏳ **AI TRADING LOG**: System monitoring consolidation channels. Awaiting model calculations.", 
                "🔄 Data Volume Intelligence: Volume profile is distributed evenly between macro bids and asks.")
    
    url = "https://groq.com"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    prompt = f"""
    Analyze this asset data and generate exactly two distinct text strings for a dashboard view.
    Asset: {ticker}
    Current Price: CAD ${price:,.2f}
    Target Price: CAD ${target_p:,.2f}
    Percentage Shift: {pct:+.2f}%
    System Action Signal: {sig}

    Strict formatting output instruction:
    Your output MUST be a JSON object with exactly two keys: "strat" and "intel". 
    "strat" value must be a 1-2 sentence real-time portfolio trade log entry detailing what the AI is thinking and doing for itself so copy-traders can mimic the move. Do not use generic placeholders.
    "intel" value must be a 1-sentence data volume intelligence report detailing order book dynamics, options flows, or whale activity.
    Keep both strings short, highly realistic, professional, and unscripted. 
    Do not mention 'customers' or 'instruct your customers'. Speak as a self-operating AI model portfolio log.
    """
    
    payload = {"model": "llama-3.1-70b-versatile", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            parsed = json.loads(res["choices"][0]["message"]["content"])
            return parsed.get("strat", "Error parsing log"), parsed.get("intel", "Error parsing intel")
    except Exception as e:
        return (f"⏳ **AI TRADING LOG**: Model maintaining its trend track baseline corridor for {ticker} near CAD ${target_p:,.2f}.", 
                "🔄 Data Volume Intelligence: Real-time buyer and seller metrics are balanced across active book parameters.")

def load_realtime_market_updates():
    usd_to_cad = 1.36
    try:
        fx_df = yf.download("CADUSD=X", period="1d", progress=False, multi_level_index=False)
        if fx_df is not None and not fx_df.empty:
            val = fx_df["Close"].to_numpy().flatten()[-1]
            if val > 0: usd_to_cad = 1.0 / float(val)
    except:
        usd_to_cad = 1.36
        
    api_key_target = st.secrets.get("GROQ_API_KEY", "WIPE")
    store = {}
    
    for ticker, display_name in watchlist.items():
        try:
            df = yf.download(ticker, period="30d", interval="1d", progress=False, multi_level_index=False)
            if df is not None and not df.empty:
                df.columns = [str(c).strip().capitalize() for col in [df.columns] for c in col]
                close_arr = df["Close"].to_numpy().flatten()
                price = float(np.nan_to_num(close_arr[-1]))
                
                if price <= 0:
                    price = float(np.nan_to_num(df["Adj close"].to_numpy().flatten()[-1]))
                if ticker in ["NVDA", "TSLA"]:
                    price *= usd_to_cad
                    
                if price <= 0:
                    price = 107000.0 if ticker=="BTC-CAD" else (3425.0 if ticker=="ETH-CAD" else (185.0 if ticker=="SOL-CAD" else (22.5 if ticker=="ARE.TO" else (116.0 if ticker=="NVDA" else 242.0))))
                    
                prev_close = float(np.nan_to_num(close_arr[-5])) if len(close_arr) >= 5 else price
                pct = ((price - prev_close) / prev_close) * 100
                target_p = price * (1.0 + (pct * 0.05 / 100))
                
                if pct > 0.05: sig, color, glow = "🟢 STRONG BUY / ENTER LONG", "#00ffcc", "glow-buy"
                elif pct < -0.05: sig, color, glow = "🔴 STRONG SELL / ENTER SHORT", "#ff4b4b", "glow-sell"
                else: sig, color, glow = "🟡 HOLD / WAIT FOR CONFIRMATION", "#ffcc00", "glow-hold"
                
                # Cache unscripted text analysis to avoid overloading API on rapid reruns
                cache_key = f"{ticker}_{round(price, 2)}"
                if cache_key not in st.session_state.ai_cards_cache:
                    strat, intel = get_ai_unscripted_card_analysis(ticker, price, target_p, pct, sig, api_key_target)
                    st.session_state.ai_cards_cache[cache_key] = (strat, intel)
                else:
                    strat, intel = st.session_state.ai_cards_cache[cache_key]
                
                store[ticker] = {"display_name": display_name, "price": price, "target": target_p, "pct": pct, "sig": sig, "color": color, "df": df, "glow": glow, "strat": strat, "intel": intel}
                st.session_state.backup_vectors_store[ticker] = store[ticker]
        except:
            pass
        if ticker not in store and ticker in st.session_state.backup_vectors_store:
            store[ticker] = st.session_state.backup_vectors_store[ticker]
    return store
