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
# CSS
# ---------------------------
st.markdown("""
<style>
body { background-color: #F4F6F9; }

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #0A2A43;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #0A2A43;
    border-left: 5px solid #1F4E79;
    padding-left: 10px;
    margin-top: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E1E5EA;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.badge {
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 600;
}

.badge-success { background:#E8F8F0; color:#1E8449; }
.badge-warning { background:#FEF5E7; color:#B9770E; }
.badge-danger { background:#FDEDEC; color:#C0392B; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown('<div class="main-title">🏛️ NexusID – National Business Identity System</div>', unsafe_allow_html=True)
st.caption("AI-powered Unified Business Identifier & Activity Intelligence Platform")

st.divider()

# ---------------------------
# SIDEBAR
# ---------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["UBID Matching", "Reviewer Console", "Activity Status", "Query Engine"]
)

# ---------------------------
# UBID MATCHING
# ---------------------------
if menu == "UBID Matching":

    st.markdown('<div class="section-title">Entity Matching & UBID Generation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        id1 = st.number_input("Record 1 ID", min_value=1, value=1)
    with col2:
        id2 = st.number_input("Record 2 ID", min_value=1, value=2)

    if st.button("Run Matching"):
        st.session_state["run_match"] = True
        st.session_state["id1"] = id1
        st.session_state["id2"] = id2

    if st.session_state.get("run_match"):

        try:
            with st.spinner("Processing..."):
                response = requests.get(
                    f"{API_URL}/match",
                    params={"id1": st.session_state["id1"], "id2": st.session_state["id2"]}
                )

            if response.status_code == 200:
                data = response.json()

                confidence = data.get("confidence", 0)
                decision = data.get("decision", "UNKNOWN")
                explanation = data.get("explanation", {})

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.subheader("🔍 Matching Result")
                st.metric("Confidence Score", f"{confidence:.2f}")
                st.progress(int(confidence * 100))

                # Decision Badge
                if decision == "AUTO-MERGE":
                    st.markdown('<span class="badge badge-success">AUTO-MERGE</span>', unsafe_allow_html=True)
                elif decision == "REVIEW":
                    st.markdown('<span class="badge badge-warning">REVIEW REQUIRED</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge badge-danger">REJECTED</span>', unsafe_allow_html=True)

                # UBID
                if decision == "AUTO-MERGE":
                    ubid = f"UBID-{st.session_state['id1']}{st.session_state['id2']}{int(confidence*100)}"
                    st.success(f"Generated UBID: {ubid}")

                st.divider()

                st.markdown("### AI Explanation Breakdown")

                for key, value in explanation.items():
                    st.markdown(f"**{key.replace('_',' ').title()}**: {value}")

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error("API Error")

        except Exception as e:
            st.error("Backend not running")
            st.code(str(e))

    if st.button("Reset"):
        st.session_state["run_match"] = False

# ---------------------------
# REVIEWER CONSOLE
# ---------------------------
elif menu == "Reviewer Console":

    st.markdown('<div class="section-title">Human Review & Decision Console</div>', unsafe_allow_html=True)

    review_cases = [
        {"id": 201, "id1": 1, "id2": 2},
        {"id": 202, "id1": 3, "id2": 4},
        {"id": 203, "id1": 5, "id2": 6},
    ]

    selected_case = st.selectbox("Select Case", [c["id"] for c in review_cases])
    case = next(c for c in review_cases if c["id"] == selected_case)

    try:
        response = requests.get(
            f"{API_URL}/match",
            params={"id1": case["id1"], "id2": case["id2"]}
        )

        if response.status_code == 200:
            data = response.json()

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown("### Case Summary")
            st.metric("Confidence", f"{data['confidence']:.2f}")
            st.progress(int(data["confidence"] * 100))

            st.markdown("### Record Comparison")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Record 1**")
                st.write("Name: Ramesh Kumar")
                st.write("City: Delhi")

            with col2:
                st.markdown("**Record 2**")
                st.write("Name: Ramesh K.")
                st.write("City: New Delhi")

            st.markdown("### AI Explanation")
            for k, v in data["explanation"].items():
                st.markdown(f"**{k.replace('_',' ').title()}**: {v}")

            st.markdown("### Final Decision")
            decision = st.radio("", ["Approve Merge", "Reject", "Escalate"])
            comments = st.text_area("Comments")

            if st.button("Submit Decision"):
                st.success("Decision submitted successfully")

            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("Backend not running")

# ---------------------------
# ACTIVITY STATUS
# ---------------------------
elif menu == "Activity Status":

    st.markdown('<div class="section-title">Business Activity Intelligence</div>', unsafe_allow_html=True)

    record_id = st.number_input("Enter Business ID", value=1)

    if st.button("Check Activity"):
        try:
            response = requests.get(f"{API_URL}/activity/{record_id}")

            if response.status_code == 200:
                data = response.json()

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.subheader(data.get("business", "Unknown"))

                status = data.get("status", "Unknown")

                if status == "Active":
                    st.success("Active")
                elif status == "Dormant":
                    st.warning("Dormant")
                else:
                    st.error("Closed")

                st.info(data.get("explanation", ""))

                st.markdown('</div>', unsafe_allow_html=True)

        except:
            st.error("Backend not running")

# ---------------------------
# QUERY ENGINE
# ---------------------------
elif menu == "Query Engine":

    st.markdown('<div class="section-title">Business Intelligence Query Engine</div>', unsafe_allow_html=True)

    pincode = st.number_input("Enter Pincode", value=560001)

    if st.button("Run Query"):
        try:
            response = requests.get(f"{API_URL}/query", params={"pincode": pincode})

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                st.markdown('<div class="card">', unsafe_allow_html=True)

                if not results:
                    st.info("No businesses found")
                else:
                    for r in results:
                        st.markdown(f"### {r['name']}")

                        if r["status"] == "Active":
                            st.success("Active")
                        elif r["status"] == "Dormant":
                            st.warning("Dormant")
                        else:
                            st.error("Closed")

                        st.markdown(f"**Issue:** {r['issue']}")
                        st.divider()

                st.markdown('</div>', unsafe_allow_html=True)

        except:
            st.error("Backend not running")
