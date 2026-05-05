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
if menu == "Reviewer Console":
    st.markdown('<div class="section-title"> Human Review & Decision Console</div>', unsafe_allow_html=True)

    st.markdown("### Pending Cases for Review")

    # Dummy review queue (replace later with API)
    review_cases = [
        {"id": 101, "id1": 1, "id2": 2, "confidence": 0.72, "status": "REVIEW"},
        {"id": 102, "id1": 3, "id2": 4, "confidence": 0.48, "status": "REVIEW"},
        {"id": 103, "id1": 5, "id2": 6, "confidence": 0.81, "status": "REVIEW"},
    ]

    selected_case = st.selectbox(
        "Select Case ID",
        [case["id"] for case in review_cases]
    )

    case_data = next(c for c in review_cases if c["id"] == selected_case)

    st.markdown("---")

    # CASE SUMMARY
    st.markdown("### Case Summary")
    col1, col2, col3 = st.columns(3)

    col1.metric("Record 1", case_data["id1"])
    col2.metric("Record 2", case_data["id2"])
    col3.metric("AI Confidence", f"{case_data['confidence']:.2f}")

    st.progress(case_data["confidence"])

    st.markdown("---")

    # FETCH MATCH DATA FROM API
    try:
        response = requests.get(
            f"{API_URL}/match?id1={case_data['id1']}&id2={case_data['id2']}"
        )

        if response.status_code == 200:
            data = response.json()
            explanation = data.get("explanation", {})

            # SIDE-BY-SIDE RECORD VIEW
            st.markdown("### Record Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Record 1")
                st.json({
                    "Name": "Ramesh Kumar",
                    "DOB": "1990-01-01",
                    "Address": "Delhi",
                    "Phone": "98XXXXXX12"
                })

            with col2:
                st.markdown("#### Record 2")
                st.json({
                    "Name": "Ramesh K.",
                    "DOB": "1990-01-01",
                    "Address": "New Delhi",
                    "Phone": "98XXXXXX12"
                })

            st.markdown("---")

            # AI EXPLANATION PANEL
            st.markdown("### AI Explanation")

            if isinstance(explanation, dict):
                for key, value in explanation.items():
                    st.markdown(f"**{key.capitalize()} Match:** {value}")
            else:
                st.write(explanation)

            st.markdown("---")

            # REVIEW ACTION PANEL
            st.markdown("### Reviewer Decision")

            decision = st.radio(
                "Select Final Decision",
                ["Approve Merge", "Reject Match", "Escalate"]
            )

            comments = st.text_area("Reviewer Comments")

            if st.button(" Submit Decision"):
                st.success("Decision submitted successfully!")

                st.markdown("### Audit Log Entry")
                st.write({
                    "case_id": selected_case,
                    "final_decision": decision,
                    "confidence": case_data["confidence"],
                    "reviewer_comments": comments
                })

        else:
            st.error("Failed to fetch match details")

    except Exception as e:
        st.error("Backend not running")
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
