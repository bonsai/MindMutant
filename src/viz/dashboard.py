import streamlit as st
import os
import sys
import glob
import json
import streamlit.components.v1 as components

# Ensure modules can be imported from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.deap.evolution import Evolution

st.set_page_config(layout="wide", page_title="MindMutant Dashboard")

st.title("MindMutant Evolution Dashboard")

# Sidebar for controls
st.sidebar.header("Evolution Controls")

# Initialize Evolution Engine
# We use st.cache_resource for the engine if it's heavy, but it's lightweight here.
# However, we want to persist it across reruns.
if 'evolution' not in st.session_state:
    st.session_state.evolution = Evolution()

# Get current generation
def get_latest_generation():
    dirs = glob.glob("data/g*")
    max_g = 0
    if not dirs:
        return 0
    for d in dirs:
        try:
            name = os.path.basename(d)
            if name.startswith('g') and name[1:].isdigit():
                g = int(name[1:])
                if g > max_g:
                    max_g = g
        except:
            pass
    return max_g

current_g = get_latest_generation()
st.sidebar.markdown(f"**Current Generation:** g{current_g}")

# Controls
if st.sidebar.button("🧬 Evolve Next Generation"):
    with st.spinner(f"Evolving from g{current_g} to g{current_g + 1}..."):
        st.session_state.evolution.evolve(current_g)
        st.success("Evolution Complete!")
        # Rerun to update the UI with new generation
        st.rerun()

if st.sidebar.button("💀 Force Disaster (Next Gen)"):
    st.sidebar.warning("This will evolve to next generation with a disaster event.")
    with st.spinner("Executing Disaster..."):
        st.session_state.evolution.evolve(current_g, force_disaster=True)
        st.success("Disaster Executed!")
        st.rerun()

# Visualization
st.header(f"Generation g{current_g} Visualization")

# Check if wordcrowd.html exists (physically) to decide whether to show the iframe
html_path = f"data/g{current_g}/wordcrowd.html"
if os.path.exists(html_path):
    # Use localhost server to serve the HTML
    # Ensure run.ps1 has started the server on port 8000 serving 'data' directory
    url = f"http://localhost:8000/g{current_g}/wordcrowd.html"
    st.caption(f"Loading visualization from: {url}")
    components.iframe(url, height=800, scrolling=True)
else:
    st.warning(f"No visualization found for Generation g{current_g}. Run evolution to generate.")

# Data Inspection
st.header("Population Data")
json_path = f"data/g{current_g}/situation.json"
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle dict wrapper (new format) vs list (old format)
    if isinstance(data, dict) and "analysis" in data:
        population_list = data["analysis"]
    elif isinstance(data, list):
        population_list = data
    else:
        population_list = []

    # Flatten for table
    table_data = []
    for item in population_list:
        if isinstance(item, dict):
            row = {
                "ID": item.get("id"),
                "Content": item.get("content"),
                "Novelty": item.get("fitness", {}).get("novelty", 0.0)
            }
            table_data.append(row)
        
    st.dataframe(table_data, use_container_width=True)
    st.caption(f"Total Population: {len(table_data)}")
else:
    st.info("No population data found.")
