# ============================================
# 🚆 DRIVER DASHBOARD PRO (AI Connected)
# ============================================

import streamlit as st
import random
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from main import run_system

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Driver Dashboard Pro", layout="wide")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🧭 Driver Control Panel")
    theme = st.radio("Choose Theme", ["Dark", "Light"], index=0)
    st.markdown("---")
    st.caption("AI Railway Optimization System 🚆")

# ---------- THEME ----------
if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {background-color: #0e1117; color: #fafafa;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {background-color: #ffffff; color: #000000;}
        </style>
    """, unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🚆 AI-Powered Train Driver Dashboard")
st.caption("Smart Safety + Real-time AI Monitoring")

# ============================================
# 🔹 GET DATA FROM AI ENGINE (STABLE)
# ============================================

if "system_data" not in st.session_state:
    st.session_state.system_data = run_system()

result = st.session_state.system_data
ai_data = result["ai_result"]
trains = ai_data["optimized_trains"]


# ---------- TRAIN SELECTION (Dynamic 20 Trains) ----------
train_options = [f"Train {t['id']}" for t in trains]
selected_train = st.selectbox("Select Your Train", train_options)

selected_id = int(selected_train.split()[1])
train_data = next(t for t in trains if t["id"] == selected_id)

speed = train_data["speed"]
recommended_speed = train_data["recommended_speed"]
delay = train_data["delay"]
# ---------- CONTROL PANEL ----------
st.subheader("🕹️ Driver Control Panel")
colA, colB, colC = st.columns(3)
if colA.button("🟢 Start Train"):
    st.success("Train accelerating smoothly...")
if colB.button("🟠 Slow Down"):
    st.warning("AI applying controlled brakes...")
if colC.button("🔴 Emergency Stop"):
    st.error("Train stopped — emergency brakes activated!")
# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)
col1.metric("Current Speed", f"{round(speed,1)} km/h")
col2.metric("AI Recommended Speed", f"{round(recommended_speed,1)} km/h")
col3.metric("Current Delay", f"{delay} min")

# ---------- SPEEDOMETER ----------
st.subheader("🚀 Live Speedometer")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=speed,
    title={'text': "Current Speed"},
    gauge={'axis': {'range': [0, 160]},
           'bar': {'color': "orange"}}
))
st.plotly_chart(fig, use_container_width=True)

# ---------- AI ALERT ----------
st.subheader("⚠️ AI Recommendation")

if speed > recommended_speed:
    st.warning("Reduce Speed – AI Safety Triggered")
elif speed < recommended_speed - 5:
    st.info("AI Suggests Slight Speed Increase")
else:
    st.success("Speed Perfectly Optimized")

# ---------- PERFORMANCE GRAPH ----------
st.subheader("📈 AI Performance Trend")

trend_data = [random.randint(70, 100) for _ in range(10)]
fig_trend = px.line(y=trend_data, markers=True,
                    title="Efficiency Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# ---------- ROUTE MAP ----------
st.subheader("🗺️ Route Overview")

route_map = folium.Map(location=[27.8, 79], zoom_start=7)

# simple position mapping from simulation
raw_progress = train_data["position"] / 300

# keep train always between start & end
progress = max(0.05, min(raw_progress, 0.95))

start_lat, start_lon = 28.6139, 77.2090
end_lat, end_lon = 26.8467, 80.9462

current_lat = start_lat + (end_lat - start_lat) * progress
current_lon = start_lon + (end_lon - start_lon) * progress

# route line
folium.PolyLine(
    [[start_lat, start_lon], [end_lat, end_lon]],
    color="blue",
    weight=4
).add_to(route_map)

# start
folium.Marker(
    [start_lat, start_lon],
    popup="Start",
    icon=folium.Icon(color="green")
).add_to(route_map)

# end
folium.Marker(
    [end_lat, end_lon],
    popup="Destination",
    icon=folium.Icon(color="red")
).add_to(route_map)

# current train (always between)
folium.Marker(
    [current_lat, current_lon],
    popup=f"Train {selected_id}",
    icon=folium.Icon(color="orange", icon="train", prefix="fa")
).add_to(route_map)

st_folium(route_map, width=900, height=450)
# ---------- DRIVER LOG ----------
st.subheader("📝 Driver Log")

st.text_area(
    "Event Log",
    f"Train {selected_id} | Speed {round(speed,1)} km/h | Delay {delay} min\nAI Monitoring Active...",
    height=150
)
