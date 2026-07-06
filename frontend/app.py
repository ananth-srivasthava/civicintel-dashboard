import streamlit as st
import sys
import os
import json
import time
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.ai_engine import process_grievance


# ---------- Utility functions ----------

def _safe_float(value):
    try:
        if value is None:
            return None
        if isinstance(value, str) and value.strip().lower() in ("", "null", "none"):
            return None
        return float(value)
    except Exception:
        return None


def log_pipeline_metrics(latency, is_cache_hit: bool):
    if is_cache_hit:
        latency_placeholder.metric("Pipeline latency (seconds)", f"{latency}", "-95% (cache)")
        compute_placeholder.metric("API compute saved (approx.)", "₹0.12", "100% bypass")
    else:
        latency_placeholder.metric("Pipeline latency (seconds)", f"{latency}")
        compute_placeholder.metric("Tokens processed (approx.)", "≈ 135", "Active AI call")


# ---------- Page configuration ----------

st.set_page_config(
    page_title="Civic Grievance Management Portal",
    page_icon="🛂",
    layout="wide",
)

# Simple “government portal” CSS (muted colors, card layout)
st.markdown(
    """
    <style>
        /* Overall background */
        .stApp {
            background-color: #f5f5f5;
        }

        /* Top header band */
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
            border: 1px solid #e0e0e0;
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
        }

        /* Make expander text look more "official" */
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
            Government of Andhra Pradesh &nbsp;|&nbsp; Urban Local Body – Civic Grievance Management
        </div>
        <div class="gov-header-subtitle">
            Online system for registration, classification, and routing of citizen grievances.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # small vertical spacing

# ---------- Sidebar (kept, but toned down) ----------

st.sidebar.markdown("### System Information")
latency_placeholder = st.sidebar.empty()
compute_placeholder = st.sidebar.empty()
st.sidebar.markdown("---")

st.sidebar.markdown("#### Deployment Settings")
env = st.sidebar.selectbox("Environment", ["Demo", "Staging", "Production"], index=0)
model_name = st.sidebar.selectbox(
    "Model route",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro"],
    index=0,
)

st.sidebar.progress(0.37, text="Approximate monthly quota used: 37%")
st.sidebar.caption(f"Current route: {model_name} &nbsp;|&nbsp; Environment: {env}")

# ---------- Main layout ----------

tab1, tab2 = st.tabs(
    ["Citizen Grievance Submission", "Municipal Processing & Dispatch"]
)

# ---------- Tab 1: Citizen Portal ----------

with tab1:
    st.markdown(
        '<div class="gov-section"><div class="gov-section-title">'
        'Grievance registration form'
        '</div>',
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="gov-muted-label">Type of issue</div>', unsafe_allow_html=True)
        issue_type = st.selectbox(
            "",
            [
                "Road hazard",
                "Garbage / sanitation",
                "Street lighting",
                "Water / sewage",
                "Public safety",
                "Other",
            ],
        )

        st.markdown('<div class="gov-muted-label">Urgency (as perceived by citizen)</div>', unsafe_allow_html=True)
        severity_hint = st.radio(
            "",
            ["Low", "Medium", "High"],
            index=1,
            horizontal=True,
        )

    with col_right:
        st.markdown('<div class="gov-muted-label">Nearest landmark or street</div>', unsafe_allow_html=True)
        landmark_hint = st.text_input(
            "",
            placeholder="e.g., Near NTR Circle, Kurnool",
        )

        st.markdown('<div class="gov-muted-label">Attach photograph (optional)</div>', unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "",
            type=["jpg", "png", "jpeg"],
        )

    st.markdown('<div class="gov-muted-label">Detailed description of the issue</div>', unsafe_allow_html=True)
    user_input = st.text_area(
        "",
        placeholder=(
            "Example: There is a large pothole near the main bus stand which is causing traffic congestion "
            "during peak hours and poses a risk to two-wheeler riders."
        ),
        height=140,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # close gov-section

    submit_col1, submit_col2 = st.columns([1, 5])
    with submit_col1:
        submit_clicked = st.button("Submit grievance")

    if submit_clicked:
        if user_input.strip():
            with st.spinner("Processing grievance and determining routing…"):
                full_report = (
                    f"[Environment: {env} | IssueType: {issue_type} | "
                    f"CitizenSeverity: {severity_hint} | Landmark: {landmark_hint}] {user_input}"
                )

                start_time = time.time()
                raw_result = process_grievance(
                    full_report, uploaded_image, model_name=model_name
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

                        # Summary and classification block
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

                        # Debug expander (kept but looks secondary)
                        with st.expander("System technical details (for administrators)"):
                            st.code(raw_result, language="json")

                        # Geospatial mapping (if available)
                        lat_raw = data.get("latitude")
                        lon_raw = data.get("longitude")

                        lat = _safe_float(lat_raw)
                        lon = _safe_float(lon_raw)

                        if lat is not None and lon is not None:
                            st.markdown(
                                '<div class="gov-section"><div class="gov-section-title">'
                                'Location on map (auto-detected)'
                                '</div>',
                                unsafe_allow_html=True,
                            )
                            map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
                            st.map(map_data, zoom=12)
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.caption("Location details were insufficient to mark a precise point on the map.")

                        st.markdown("</div>", unsafe_allow_html=True)  # close System classification block

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
            st.dataframe(snapshot_df, use_container_width=True)

            st.markdown("**City-level load (illustrative)**")
            fake_stats = pd.DataFrame(
                {
                    "Category": [
                        "Road hazard",
                        "Sanitation",
                        "Street lighting",
                        "Water / sewage",
                    ],
                    "Open tickets": [12, 7, 5, 3],
                }
            )
            st.bar_chart(
                fake_stats.set_index("Category"),
                use_container_width=True,
            )

        with col2:
            st.markdown("**Dispatch status**")
            st.metric("Ticket status", "Queued → Assigned")
            st.metric("Target resolution time (SLA)", "4 hours")

            st.markdown("**System routing timeline (illustrative)**")
            st.markdown(
                "- 0 min: Citizen submission received\n"
                "- < 1 sec: Automated categorisation and severity assessment\n"
                "- < 2 sec: Department routing and work order creation\n"
                "- < 5 sec: Dispatch brief generated"
            )

            st.markdown("**Dispatch brief download**")

            formal_report = f"""GOVERNMENT OF ANDHRA PRADESH
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

--------------------------------------------------
This document has been generated automatically by the Civic Grievance
Management System for internal administrative use.
"""

            st.text(formal_report)

            st.download_button(
                label="Download dispatch brief (Markdown)",
                data=formal_report,
                file_name=f"dispatch_ticket_{time.strftime('%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

            st.download_button(
                label="Download dispatch brief (Text)",
                data=formal_report,
                file_name=f"dispatch_ticket_{time.strftime('%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info(
            "No grievance has been processed in this session. "
            "Once a citizen submits a grievance, details will appear here for municipal staff."
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ---------- About section (kept but more neutral) ----------

with st.expander("About this system"):
    st.markdown(
        """
        This portal is a prototype civic grievance management system intended for demonstration purposes.

        It supports:
        - Online submission of grievances by citizens.
        - Automated categorisation, prioritisation and departmental routing.
        - Internal work order snapshot, dispatch brief generation and basic analytics for municipal staff.
        """
    )