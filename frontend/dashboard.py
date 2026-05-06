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
# CUSTOM CSS
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
    [" UBID Matching", " Reviewer Console", " Activity Status", " Query Engine"]
)

# ---------------------------
# UBID MATCHING
# ---------------------------
if menu == " UBID Matching":

    st.markdown('<div class="section-title">Entity Matching & UBID Generation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        id1 = st.number_input("Record 1 ID", min_value=1, value=1)
    with col2:
        id2 = st.number_input("Record 2 ID", min_value=1, value=2)

    if st.button(" Run Matching"):
        st.session_state["run_match"] = True
        st.session_state["id1"] = id1
        st.session_state["id2"] = id2

    if st.session_state.get("run_match"):

        try:
            response = requests.get(
                f"{API_URL}/match",
                params={
                    "id1": st.session_state["id1"],
                    "id2": st.session_state["id2"]
                }
            )

            if response.status_code == 200:
                data = response.json()

                confidence = data.get("confidence", 0)
                decision = data.get("decision", "UNKNOWN")
                explanation = data.get("explanation", {})

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🔍 Matching Result")

                st.metric("Confidence Score", f"{confidence:.2f}")
                st.progress(int(confidence * 100))  # FIXED

                if decision == "AUTO-MERGE":
                    st.success(f"Decision: {decision}")
                elif decision == "REVIEW":
                    st.warning(f"Decision: {decision}")
                else:
                    st.error(f"Decision: {decision}")

                if decision == "AUTO-MERGE":
                    ubid = f"UBID-{st.session_state['id1']}{st.session_state['id2']}{int(confidence*100)}"
                    st.success(f" Generated UBID: {ubid}")

                st.divider()

                st.markdown("### AI Explanation Breakdown")

                colA, colB = st.columns(2)

                for i, (key, value) in enumerate(explanation.items()):
                    label = key.replace("_", " ").title()

                    if i % 2 == 0:
                        with colA:
                            st.markdown(f"**{label}**: {value}")
                    else:
                        with colB:
                            st.markdown(f"**{label}**: {value}")

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error("API Error")

        except Exception as e:
            st.error("Backend not running")
            st.code(str(e))

    if st.button(" Reset"):
        st.session_state["run_match"] = False


# ---------------------------
# REVIEWER CONSOLE
# ---------------------------
elif menu == " Reviewer Console":

    st.markdown('<div class="section-title">Human Review & Decision Console</div>', unsafe_allow_html=True)

    review_cases = [
        {"id": 201, "id1": 1, "id2": 2},
        {"id": 202, "id1": 3, "id2": 4},
        {"id": 203, "id1": 5, "id2": 6},
    ]

    selected_case = st.selectbox(
        " Select Case for Review",
        [case["id"] for case in review_cases]
    )

    case_data = next(c for c in review_cases if c["id"] == selected_case)

    try:
        response = requests.get(
            f"{API_URL}/match",
            params={"id1": case_data["id1"], "id2": case_data["id2"]}
        )

        if response.status_code == 200:
            data = response.json()

            confidence = data["confidence"]
            decision = data["decision"]
            explanation = data["explanation"]

            st.markdown("### Case Summary")

            col1, col2, col3 = st.columns(3)
            col1.metric("Record 1", case_data["id1"])
            col2.metric("Record 2", case_data["id2"])
            col3.metric("AI Confidence", f"{confidence:.2f}")

            st.progress(int(confidence * 100))  

            st.markdown("### Record Comparison")

            col1, col2 = st.columns(2)

            with col1:
                st.json({"Name": "Ramesh Kumar", "Address": "Delhi", "Phone": "98XXXXXX12"})

            with col2:
                st.json({"Name": "Ramesh K.", "Address": "New Delhi", "Phone": "98XXXXXX12"})

            st.markdown("### AI Explanation")

            for key, value in explanation.items():
                st.markdown(f"**{key.replace('_',' ').title()}**: {value}")

            st.markdown("### Reviewer Decision")

            final_decision = st.radio(
                "Select Final Decision",
                ["Approve Merge", "Reject Match", "Escalate"]
            )

            comments = st.text_area("Reviewer Comments")

            if st.button(" Submit Decision"):
                st.success("Decision submitted!")

                st.json({
                    "case_id": selected_case,
                    "ai_decision": decision,
                    "confidence": confidence,
                    "final_decision": final_decision,
                    "comments": comments
                })

        else:
            st.error("API Error")

    except Exception as e:
        st.error("Backend not running")
        st.code(str(e))


# ---------------------------
# ACTIVITY STATUS (READY)
# ---------------------------
elif menu == " Activity Status":

    st.markdown('<div class="section-title">Business Activity Intelligence</div>', unsafe_allow_html=True)

    record_id = st.number_input("Enter Business ID", min_value=1, value=1)

    if st.button("Check Activity"):
        try:
            response = requests.get(f"{API_URL}/activity/{record_id}")

            if response.status_code == 200:
                data = response.json()

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.subheader(data.get("business", "Unknown"))

                status = data.get("status", "Unknown")

                if status == "Active":
                    st.success(f"Status: {status}")
                elif status == "Dormant":
                    st.warning(f"Status: {status}")
                else:
                    st.error(f"Status: {status}")

                st.markdown("### Explanation")
                st.info(data.get("explanation", ""))

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error(f"API Error: {response.status_code}")

        except Exception as e:
            st.error("Backend not running")
            st.code(str(e))


# ---------------------------
# QUERY ENGINE (READY)
# ---------------------------
elif menu == " Query Engine":

    st.markdown('<div class="section-title">Business Intelligence Query Engine</div>', unsafe_allow_html=True)

    pincode = st.number_input("Enter Pincode", value=560001)

    if st.button("Run Query"):
        try:
            response = requests.get(
                f"{API_URL}/query",
                params={"pincode": pincode}
            )

            if response.status_code == 200:
                data = response.json()

                results = data.get("results", [])

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Query Results")

                if len(results) == 0:
                    st.info("No matching businesses found")
                else:
                    for r in results:
                        st.markdown(f"### {r['name']}")

                        status = r.get("status", "Unknown")

                        if status == "Active":
                            st.success(f"Status: {status}")
                        elif status == "Dormant":
                            st.warning(f"Status: {status}")
                        else:
                            st.error(f"Status: {status}")

                        st.markdown(f"**Issue:** {r.get('issue', 'N/A')}")
                        st.divider()

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error(f"API Error: {response.status_code}")

        except Exception as e:
            st.error("Backend not running")
            st.code(str(e))
