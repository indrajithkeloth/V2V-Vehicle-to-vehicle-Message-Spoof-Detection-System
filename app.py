import streamlit as st
import pandas as pd
import time
import pickle
import folium
from streamlit_folium import st_folium
from v2v_simulator import generate_message

# Load ML model
with open("ml_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(layout="wide")
st.title("🚗 V2V Message Spoof Detection Dashboard")

log = []
df = pd.DataFrame()

# Delay to let the app initialize before starting the loop
time.sleep(1)

while True:
    # Generate simulated V2V message
    msg = generate_message()

    # Rule-based spoof checks
    rule_spoof = False
    reason = "Normal"
    if msg["vehicle_id"] not in {"V1", "V2"}:
        rule_spoof = True
        reason = "Unknown ID"
    elif msg["speed"] > 200:
        rule_spoof = True
        reason = "Unrealistic Speed"

    # ML-based anomaly detection
    pred = model.predict([[msg["speed"]]])[0]
    if pred == -1 and not rule_spoof:
        reason = "Anomaly (ML)"

    msg["result"] = reason
    log.append(msg)

    # Update DataFrame
    df = pd.DataFrame(log)

    # Display message log
    st.subheader("📝 V2V Message Log")
    st.dataframe(df.tail(10), use_container_width=True)

    # Speed trend chart
    st.subheader("📊 Speed Trend (Last 10 Messages)")
    st.line_chart(df["speed"].tail(10))

    # Map visualization
    st.subheader("🗺️ Real-Time Vehicle Location Map")
    df_map = df.tail(10).copy()

    try:
        # Extract lat/lon
        df_map[["lat", "lon"]] = pd.DataFrame(df_map["location"].tolist(), index=df_map.index)

        if not df_map.empty:
            center_lat = df_map["lat"].mean()
            center_lon = df_map["lon"].mean()

            # Create folium map
            m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

            # Add vehicle markers
            for _, row in df_map.iterrows():
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=5,
                    popup=folium.Popup(
                        f"Vehicle: {row['vehicle_id']}<br>Speed: {row['speed']} km/h<br>Result: {row['result']}",
                        max_width=250
                    ),
                    color='red' if row["result"] != "Normal" else 'green',
                    fill=True,
                    fill_color='red' if row["result"] != "Normal" else 'green',
                    fill_opacity=0.7
                ).add_to(m)

            # Draw trail line connecting vehicle positions
            folium.PolyLine(
                df_map[["lat", "lon"]].values.tolist(),
                color="blue",
                weight=2.5,
                opacity=1
            ).add_to(m)

            # Display the map
            st_folium(m, width=700, height=500)
        else:
            st.info("Waiting for location data to display map...")

    except Exception as e:
        st.error(f"Error rendering map: {e}")

    # Wait before next update
    time.sleep(1)
