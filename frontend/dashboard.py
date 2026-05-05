import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="NexusID Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# CUSTOM CSS (KEY PART)
# ---------------------------
st.markdown("""
    <style>
        body {
            background-color: #F5F7FA;
        }
        .main-title {
            font-size: 32px;
            font-weight: 700;
            color: #0B3C5D;
        }
        .section-title {
            font-size: 22px;
            font-weight: 600;
            color: #0B3C5D;
            margin-top: 20px;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .success {
            color: #2ECC71;
            font-weight: bold;
        }
        .warning {
            color: #F39C12;
            font-weight: bold;
        }
        .error {
            color: #E74C3C;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown('<div class="main-title">🏛️ NexusID Governance Dashboard</div>', unsafe_allow_html=True)
st.caption("Unified Business Identifier & Activity Intelligence System")

st.divider()

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
menu = st.sidebar.radio(
    "Navigation",
    [" UBID Matching", " Activity Status", " Query Engine"]
)

# ---------------------------
# UBID MATCHING
# ---------------------------
if menu == "UBID Matching":
    st.markdown('<div class="section-title">Entity Matching & UBID Generation</div>', unsafe_allow_html=True)

    # INPUT SECTION
    st.markdown("### 🔎 Select Records to Match")

    col1, col2 = st.columns(2)
    with col1:
        id1 = st.number_input("Record 1 ID", min_value=1, value=1)
    with col2:
        id2 = st.number_input("Record 2 ID", min_value=1, value=2)

    st.markdown("---")

    # ACTION BUTTON
    if st.button(" Run AI Matching Engine"):

        with st.spinner("Running AI-powered entity resolution..."):

            try:
                response = requests.get(f"{API_URL}/match?id1={id1}&id2={id2}")

                if response.status_code == 200:
                    data = response.json()

                    confidence = float(data.get("confidence", 0))
                    decision = data.get("decision", "UNKNOWN")
                    explanation = data.get("explanation", {})

                    # RESULT CARD
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader(" Matching Result")

                    # CONFIDENCE SCORE VISUAL
                    st.markdown("#### Confidence Score")
                    st.progress(confidence)

                    if confidence >= 0.85:
                        st.success(f"High Confidence: {confidence:.2f}")
                    elif confidence >= 0.5:
                        st.warning(f"Medium Confidence: {confidence:.2f}")
                    else:
                        st.error(f"Low Confidence: {confidence:.2f}")

                    st.markdown("---")

                    # DECISION DISPLAY
                    st.markdown("#### AI Decision")

                    if decision == "AUTO-MERGE":
                        st.markdown(
                            f'<div style="background-color:#0f5132;padding:10px;border-radius:8px;color:white;"><b>{decision}</b> → Records automatically merged</div>',
                            unsafe_allow_html=True
                        )

                    elif decision == "REVIEW":
                        st.markdown(
                            f'<div style="background-color:#664d03;padding:10px;border-radius:8px;color:white;"><b>{decision}</b> → Requires manual verification</div>',
                            unsafe_allow_html=True
                        )
                        st.warning(" This case has been flagged for human review.")

                    else:
                        st.markdown(
                            f'<div style="background-color:#842029;padding:10px;border-radius:8px;color:white;"><b>{decision}</b> → Records do NOT match</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown("---")

                    # EXPLANATION SECTION
                    st.markdown("#### 🔍 Explainability (Why this decision?)")

                    if isinstance(explanation, dict):
                        for key, value in explanation.items():
                            st.markdown(f"**{key.capitalize()} Match:** {value}")
                    else:
                        st.write(explanation)

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error(" API Error: Unable to fetch results")

            except Exception as e:
                st.error(" Backend not running or connection failed")
                st.info(" Make sure FastAPI server is running on http://127.0.0.1:8000")
                st.code(str(e))

# ---------------------------
# ACTIVITY STATUS
# ---------------------------
elif menu == " Activity Status":
    st.markdown('<div class="section-title">Business Activity Intelligence</div>', unsafe_allow_html=True)

    record_id = st.number_input("Enter Business ID", min_value=1, value=1)

    if st.button("Check Activity"):
        response = requests.get(f"{API_URL}/activity/{record_id}")

        if response.status_code == 200:
            data = response.json()

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f" {data['business']}")

            status = data["status"]

            if status == "Active":
                st.markdown(f'<p class="success">Status: {status}</p>', unsafe_allow_html=True)
            elif status == "Dormant":
                st.markdown(f'<p class="warning">Status: {status}</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p class="error">Status: {status}</p>', unsafe_allow_html=True)

            st.write(f"**Explanation:** {data['explanation']}")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# QUERY ENGINE
# ---------------------------
elif menu == " Query Engine":
    st.markdown('<div class="section-title">Business Intelligence Query Engine</div>', unsafe_allow_html=True)

    pincode = st.number_input("Enter Pincode", value=560001)

    if st.button("Run Query"):
        response = requests.get(f"{API_URL}/query?pincode={pincode}")

        if response.status_code == 200:
            data = response.json()

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Query Results")

            if len(data["results"]) == 0:
                st.info("No matching records found")
            else:
                for r in data["results"]:
                    st.markdown(f"** {r['name']}**")
                    st.write(f"Status: {r['status']}")
                    st.markdown(f'<p class="warning">Issue: {r["issue"]}</p>', unsafe_allow_html=True)
                    st.divider()

            st.markdown('</div>', unsafe_allow_html=True)
