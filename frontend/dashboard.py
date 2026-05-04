import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NexusID Dashboard", layout="wide")

st.title("NexusID: Business Intelligence Dashboard")

menu = st.sidebar.selectbox(
    "Select Feature",
    ["UBID Matching", "Activity Status", "Query Engine"]
)

# -------------------------
# UBID MATCHING
# -------------------------
if menu == "UBID Matching":
    st.header(" Entity Matching & UBID Generation")

    id1 = st.number_input("Record 1 ID", min_value=1, value=1)
    id2 = st.number_input("Record 2 ID", min_value=1, value=2)

    if st.button("Match Records"):
        response = requests.get(f"{API_URL}/match?id1={id1}&id2={id2}")

        if response.status_code == 200:
            data = response.json()

            st.subheader(" Matching Result")
            st.write(f"**Confidence Score:** {data['confidence']}")
            st.write(f"**Decision:** {data['decision']}")

            st.subheader("🔍 Explanation")
            st.json(data["explanation"])

            if data["decision"] == "REVIEW":
                st.warning(" This case requires human review")

# -------------------------
# ACTIVITY STATUS
# -------------------------
elif menu == "Activity Status":
    st.header(" Business Activity Classification")

    record_id = st.number_input("Enter Business ID", min_value=1, value=1)

    if st.button("Check Status"):
        response = requests.get(f"{API_URL}/activity/{record_id}")

        if response.status_code == 200:
            data = response.json()

            st.subheader(f" {data['business']}")
            st.write(f"**Status:** {data['status']}")
            st.write(f"**Explanation:** {data['explanation']}")

            if data["status"] == "Dormant":
                st.warning(" Business is Dormant")
            elif data["status"] == "Closed":
                st.error(" Business is Closed")
            else:
                st.success(" Business is Active")

# -------------------------
# QUERY ENGINE
# -------------------------
elif menu == "Query Engine":
    st.header("🔍 Business Query Engine")

    pincode = st.number_input("Enter Pincode", value=560001)

    if st.button("Run Query"):
        response = requests.get(f"{API_URL}/query?pincode={pincode}")

        if response.status_code == 200:
            data = response.json()

            st.subheader(" Results")

            if len(data["results"]) == 0:
                st.info("No matching records found")
            else:
                for r in data["results"]:
                    st.write(f" {r['name']} - {r['status']}")
                    st.write(f" Issue: {r['issue']}")
                    st.divider()
