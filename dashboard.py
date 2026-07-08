import streamlit as st
import pandas as pd
import plotly.express as px
from main import run_system
import folium
from streamlit_folium import st_folium
import random

# --- Page Config ---
st.set_page_config(page_title="AI Train Control Dashboard", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("🧭 Control Panel")
    theme = st.radio("Choose Theme", ["Dark", "Light"], index=0)
    refresh = st.button("🔁 Refresh Dashboard")
    st.markdown("---")
    st.caption("AI Railway Optimization System 🚆")

# --- Dark Theme ---
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {background-color: #0e1117; color: #fafafa;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Title ---
st.title("🚆 AI-Based Train Control Room Dashboard")

# ===============================
# 🔹 RUN COMPLETE SYSTEM
# ===============================
result = run_system()

ai_data = result["ai_result"]
traditional_data = result["traditional_result"]

df = pd.DataFrame(ai_data["optimized_trains"])

# ===============================
# 🔹 Layout 1: Train Table + Speed Chart
# ===============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Real-Time Train Status")
    st.dataframe(df, use_container_width=True)

    st.subheader("🚆 Speed Comparison")
    fig_speed = px.bar(
        df,
        x="id",
        y=["speed", "recommended_speed"],
        barmode="group",
        title="Original vs Recommended Speed"
    )
    st.plotly_chart(fig_speed, use_container_width=True)

with col2:
    st.subheader("📈 System Performance Comparison")

    performance_df = pd.DataFrame({
        "System": ["Traditional", "AI Optimized"],
        "Throughput": [
            traditional_data["throughput"],
            ai_data["throughput"]
        ],
        "Average Delay": [
            traditional_data["average_delay"],
            ai_data["average_delay"]
        ]
    })

    fig_throughput = px.bar(
        performance_df,
        x="System",
        y="Throughput",
        color="System",
        title="Throughput Comparison"
    )

    fig_delay = px.bar(
        performance_df,
        x="System",
        y="Average Delay",
        color="System",
        title="Average Delay Comparison"
    )

    st.plotly_chart(fig_throughput, use_container_width=True)
    st.plotly_chart(fig_delay, use_container_width=True)

# ===============================
# 🔹 Layout 2: AI vs Traditional Metrics
# ===============================
st.subheader("🤖 AI Optimization Insights")

col3, col4, col5 = st.columns(3)

col3.metric("AI Throughput", round(ai_data["throughput"], 2))
col4.metric("AI Avg Delay (min)", round(ai_data["average_delay"], 2))
col5.metric("Congestion Points", ai_data["congestion_points"])

# ===============================
# 🔹 Live Train Map (Demo Purpose)
# ===============================
# ===============================
# 🔹 Live Train Map (20 Trains Stable)
# ===============================

st.subheader("🌍 Live Train Movement (20 Trains)")

# 🔒 Freeze system data (No blink)
if "system_data" not in st.session_state:
    st.session_state.system_data = run_system()

result = st.session_state.system_data
trains = result["ai_result"]["optimized_trains"]

map_center = [27.5, 79]
train_map = folium.Map(location=map_center, zoom_start=6)

# 🎨 20 UNIQUE COLORS
color_palette = [
    "red","blue","green","purple","orange",
    "darkred","lightred","beige","darkblue","darkgreen",
    "cadetblue","darkpurple","pink","lightblue","lightgreen",
    "gray","black","white","lightgray","darkpurple"
]

# 🚉 Station Pool
stations = [
    (28.6139, 77.2090),  # Delhi
    (28.6692, 77.4538),
    (27.8974, 78.0880),
    (27.1767, 78.0081),
    (26.4499, 80.3319),
    (26.8467, 80.9462),
    (25.3176, 82.9739),
]

for index, train in enumerate(trains):

    # Unique route per train
    start_index = train["id"] % len(stations)
    end_index = (train["id"] + 3) % len(stations)

    start_lat, start_lon = stations[start_index]
    end_lat, end_lon = stations[end_index]

    # Keep train between start & end
    progress = max(0.05, min(train["position"] / 300, 0.95))

    current_lat = start_lat + (end_lat - start_lat) * progress
    current_lon = start_lon + (end_lon - start_lon) * progress

    train_color = color_palette[index % 20]

    # Route Line
    folium.PolyLine(
        [[start_lat, start_lon], [end_lat, end_lon]],
        color=train_color,
        weight=3,
        opacity=0.5
    ).add_to(train_map)

    # Train Marker
    folium.Marker(
        [current_lat, current_lon],
        popup=f"Train {train['id']} | Speed {round(train['speed'],1)} | Delay {train['delay']} min",
        icon=folium.Icon(color=train_color, icon="train", prefix="fa")
    ).add_to(train_map)

st_folium(train_map, width=1100, height=550)


# ===============================
# 🔹 AI Live Insights
# ===============================
st.subheader("🧠 AI Live Insights")

insights = [
    "🚨 AI detected potential congestion — speed optimized.",
    "⚡ Average delay reduced through dynamic headway.",
    "📊 Throughput improved using adaptive scheduling.",
    "🚆 Safe distance maintained across all trains.",
    "🔄 AI recalculated optimal speed based on delay severity."
]

if st.button("Generate AI Insight"):
    st.info(random.choice(insights))
else:
    st.success("AI Monitoring Active...")
