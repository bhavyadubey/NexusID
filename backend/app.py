from fastapi import FastAPI
import pandas as pd
from matching import compute_similarity
from activity import classify_activity

app = FastAPI()

data = pd.read_csv("../data/sample_data.csv")

@app.get("/")
def home():
    return {"message": "NexusID API Running"}

@app.get("/match")
def match_records(id1: int, id2: int):
    # Dummy logic (replace later with ML)
    
    confidence = 0.87 if id1 != id2 else 1.0

    if confidence > 0.85:
        decision = "AUTO-MERGE"
    elif confidence > 0.5:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    explanation = {
        "name_match": "High",
        "dob_match": "Exact",
        "address_match": "Partial",
        "phone_match": "Exact"
    }

    return {
        "confidence": confidence,
        "decision": decision,
        "explanation": explanation
    }

@app.get("/activity/{id}")
def activity_status(id: int):
    record = data[data['id'] == id].iloc[0]
    status = classify_activity(record['last_activity_months'])

    return {
        "business": record['name'],
        "status": status,
        "last_activity_months": record['last_activity_months'],
        "explanation": f"No activity for {record['last_activity_months']} months"
    }

@app.get("/query")
def query(pincode: int):
    filtered = data[data['pincode'] == pincode]

    result = []
    for _, row in filtered.iterrows():
        status = classify_activity(row['last_activity_months'])
        if status == "Active" and row['last_activity_months'] > 12:
            result.append({
                "name": row['name'],
                "status": status,
                "issue": "No recent inspection"
            })

    return {"results": result}
