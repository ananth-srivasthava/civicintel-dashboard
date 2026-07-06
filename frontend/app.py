import streamlit as st
import sys
import os
import json
import time
import pandas as pd
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.ai_engine import process_grievance


# ---------- Utility functions ----------

def get_real_coordinates(location_name):
    """Tool to fetch exact coordinates using a free Geocoding API."""
    if not location_name or str(location_name).strip().lower() in ("null", "none", ""):
        return None, None
        
    try:
        # OpenStreetMap's free Nominatim API
        url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
        headers = {'User-Agent': 'CivicIntelHackathonApp/1.0'}
        
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            geo_data = response.json()
            if geo_data:
                return float(geo_data[0]['lat']), float(geo_data[0]['lon'])
    except Exception:
        pass 
        
    return None, None


def log_pipeline_metrics(latency, is_cache_hit: bool):
    if is_cache_hit:
        latency_placeholder.metric("Pipeline latency (seconds)", f"{latency}", "-95% (cache)")
        compute_placeholder.metric("API compute saved", "₹0.12", "100% bypass")
    else:
        latency_placeholder.metric("Pipeline latency (seconds)", f"{latency}")
        compute_placeholder.metric("Tokens processed", "≈ 135", "Active AI call")


# ---------- Page configuration ----------

st.set_page_config(
    page_title="CivicIntel | Smart City Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Sidebar & Configuration ----------

st.sidebar.markdown("### System Configuration")
model_name = st.sidebar.selectbox(
    "Inference Engine",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Live Telemetry")
latency_placeholder = st.sidebar.empty()
compute_placeholder = st.sidebar.empty()

# Fixed Standard Light CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f5f5;
            color: #333333;
        }
        .gov-header {
            background-color: #003366;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 0 0 4px 4px;
            border-bottom: 4px solid #f2a900;
        }
        .gov-header-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.15rem;
        }
        .gov-header-subtitle {
            font-size: 0.9rem;
            opacity: 0.95;
        }
        .gov-section {
            background-color: #ffffff;
            padding: 1rem 1.25rem;
            border-radius: 4px;
            border: 1px solid #d0d0d0;
            margin-bottom: 1rem;
        }
        .gov-section-title {
            font-size: 1.0rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #003366;
        }
        .gov-muted-label {
            font-size: 0.85rem;
            color: #555555;
            margin-bottom: 0.25rem;
            font-weight: 500;
        }
        summary {
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------

st.markdown(
    """
    <div class="gov-header">
        <div class="gov-header-title">
            CivicIntel &nbsp;|&nbsp; Autonomous Grievance Routing AI
        </div>
        <div class="gov-header-subtitle">
            Unstructured reporting. Automated municipal dispatch.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  

# ---------- Main layout ----------

tab1, tab2 = st.tabs(
    ["📥 Citizen Grievance Submission", "📊 Municipal Processing & Dispatch"]
)

# ---------- Tab 1: Citizen Portal ----------

with tab1:
    st.markdown(
        '<div class="gov-section"><div class="gov-section-title">'
        'Agentic Grievance Registration'
        '</div>',
        unsafe_allow_html=True,
    )
    
    # --- REGIONAL CONTEXT TOOLBAR (ALL 28 STATES & 8 UTs) ---
    st.markdown('<div class="gov-muted-label">Regional Context (Simulated GPS/Profile Data)</div>', unsafe_allow_html=True)
    loc_col1, loc_col2 = st.columns(2)
    with loc_col1:
        states_and_uts = [
            "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", 
            "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", 
            "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", 
            "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", 
            "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", 
            "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", 
            "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
        ]
        selected_state = st.selectbox("State / Union Territory", states_and_uts, index=1)
    with loc_col2:
        selected_district = st.text_input("District / City", value="Kurnool")

    st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 1.5rem;'/>", unsafe_allow_html=True)
    
    st.markdown("Describe the issue in your own words. Our AI Agent will automatically classify the category, assess the severity, and route it to the correct municipal department.")

    st.markdown('<div class="gov-muted-label">Detailed description of the issue</div>', unsafe_allow_html=True)
    user_input = st.text_area(
        "Issue Description",
        label_visibility="collapsed",
        placeholder=(
            "Example: There is a large pothole near the main bus stand on NTR Circle which is causing traffic congestion..."
        ),
        height=140,
    )

    st.markdown('<div class="gov-muted-label">Attach visual evidence (optional)</div>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader(
        "Upload Evidence",
        label_visibility="collapsed",
        type=["jpg", "png", "jpeg"],
    )

    st.markdown("</div>", unsafe_allow_html=True)

    submit_col1, submit_col2 = st.columns([1, 5])
    with submit_col1:
        submit_clicked = st.button("Submit grievance")

    if submit_clicked:
        if user_input.strip():
            with st.spinner("AI Agent analyzing unstructured data and determining routing…"):
                full_report = user_input 

                start_time = time.time()
                raw_result = process_grievance(
                    full_report, 
                    state=selected_state, 
                    district=selected_district, 
                    image_file=uploaded_image, 
                    model_name=model_name
                )
                end_time = time.time()
                latency = round(end_time - start_time, 2)

                try:
                    data = json.loads(raw_result)

                    if "error" in data:
                        st.error(f"System error: {data['error']}")
                        latency_placeholder.metric("Pipeline latency (seconds)", f"{latency}")
                        compute_placeholder.metric("Tokens processed (approx.)", "N/A", "Error")
                        st.stop()

                    if data.get("category") == "Cache Hit":
                        st.warning(data.get("summary"))
                        log_pipeline_metrics(latency, is_cache_hit=True)
                    else:
                        st.success("Grievance has been registered and routed to the concerned department.")
                        st.session_state["latest_ticket"] = data
                        log_pipeline_metrics(latency, is_cache_hit=False)

                        st.markdown(
                            '<div class="gov-section"><div class="gov-section-title">'
                            'System classification'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                        col1, col2, col3 = st.columns(3)
                        col1.metric("Category", data.get("category", "N/A"))
                        col2.metric("Severity", data.get("severity", "N/A"))
                        col3.metric("Department", data.get("assigned_department", "N/A"))

                        st.markdown(
                            '<div class="gov-muted-label">Summary generated by the system</div>',
                            unsafe_allow_html=True,
                        )
                        st.write(data.get("summary", "N/A"))

                        st.markdown("### Citizen view")
                        citizen_msg = (
                            "Based on the details provided, the grievance has been recorded as a "
                            f"{data.get('severity', 'N/A').lower()} priority "
                            f"{data.get('category', 'issue').lower()} and forwarded to "
                            f"{data.get('assigned_department', 'the concerned department')} "
                            "for necessary action."
                        )
                        st.write(citizen_msg)

                        with st.expander("System technical details (for administrators)"):
                            st.code(raw_result, language="json")

                        location_query = data.get("location_query")
                        
                        if location_query:
                            st.markdown(f'<div class="gov-muted-label">Searching Map Database for: {location_query}...</div>', unsafe_allow_html=True)
                            lat, lon = get_real_coordinates(location_query)
                        else:
                            lat, lon = None, None

                        if lat is not None and lon is not None:
                            st.markdown(
                                '<div class="gov-section"><div class="gov-section-title">'
                                'Location on map (Database Verified)'
                                '</div>',
                                unsafe_allow_html=True,
                            )
                            map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
                            st.map(map_data, zoom=14)
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.caption("Location details were insufficient to mark a precise point on the map.")

                        st.markdown("</div>", unsafe_allow_html=True) 

                except json.JSONDecodeError:
                    st.error("Unable to read system response. Please try again after some time.")
        else:
            st.warning("Please enter a description of the issue before submitting.")


# ---------- Tab 2: Municipal view ----------

with tab2:
    st.markdown(
        '<div class="gov-section"><div class="gov-section-title">'
        'Work order and dispatch view'
        '</div>',
        unsafe_allow_html=True,
    )

    if "latest_ticket" in st.session_state:
        ticket = st.session_state["latest_ticket"]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**Latest grievance record (system view)**")
            st.json(ticket)

            st.markdown("**Work order summary (internal use)**")
            snapshot_df = pd.DataFrame(
                [
                    {
                        "Ticket ID": time.strftime("%Y%m%d-%H%M%S"),
                        "Category": ticket.get("category", "N/A"),
                        "Severity": ticket.get("severity", "N/A"),
                        "Department": ticket.get("assigned_department", "N/A"),
                    }
                ]
            )
            st.dataframe(snapshot_df, width="stretch")

        with col2:
            st.markdown("**Dispatch brief download**")

            formal_report = f"""SMART CITY INITIATIVE
Urban Local Body – Civic Grievance Management System

Dispatch Brief – Ticket {time.strftime('%Y%m%d-%H%M%S')}
--------------------------------------------------
Generation date and time : {time.strftime('%Y-%m-%d %H:%M:%S')}
Target agency            : {ticket.get('assigned_department', 'N/A')}
Security classification  : Official

1. Classification and criticality
   - Municipal domain : {ticket.get('category', 'N/A')}
   - Priority level   : {ticket.get('severity', 'N/A')}

2. System-generated summary
   {ticket.get('summary', 'N/A')}
   
3. Location Extracted
   {ticket.get('location_query', 'N/A')}

--------------------------------------------------
This document has been generated automatically by the CivicIntel
Management System for internal administrative use.
"""

            st.text(formal_report)

            st.download_button(
                label="Download dispatch brief (Markdown)",
                data=formal_report,
                file_name=f"dispatch_ticket_{time.strftime('%H%M%S')}.md",
                mime="text/markdown",
                width="stretch",
            )

            st.download_button(
                label="Download dispatch brief (Text)",
                data=formal_report,
                file_name=f"dispatch_ticket_{time.strftime('%H%M%S')}.txt",
                mime="text/plain",
                width="stretch",
            )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info(
            "No grievance has been processed in this session. "
            "Once a citizen submits a grievance, details will appear here for municipal staff."
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ---------- About section ----------

with st.expander("About this system"):
    st.markdown(
        """
        This portal is an autonomous civic grievance management system intended for demonstration purposes.

        It supports:
        - Natural language submission of grievances by citizens.
        - Automated categorisation, severity prioritisation, and departmental routing via AI Agent.
        - Real-time Geocoding utilizing OpenStreetMap Nominatim.
        - Internal work order snapshot and dispatch brief generation for municipal staff.
        """
    )